#!/usr/bin/env python3
"""Local IMX500 object detection preview, viewed through an SSH forward."""
import json
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import cv2
from picamera2 import Picamera2
from picamera2.devices import IMX500

MODEL = '/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk'
condition = threading.Condition()
frame = None
sequence = 0
state = dict(ready=False, error=None, fps=0, frames=0, inference_frames=0,
             detections=[], camera='Sony IMX500', model=Path(MODEL).name)

PAGE = '''<!doctype html><html lang="cs"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ProMichAiCam1 — AI kamera</title><style>
body{margin:0;background:#101820;color:#e8f0f5;font:16px system-ui,sans-serif}
main{max-width:1100px;margin:auto;padding:24px}h1{font-size:26px;margin:0 0 8px}
p{color:#b8cad5}img{width:100%;background:#050a0e;border-radius:12px;min-height:180px}
#status{padding:12px 0}#objects{display:flex;gap:8px;flex-wrap:wrap}
.tag{background:#203948;padding:8px 12px;border-radius:8px}
</style><main><h1>ProMichAiCam1 · AI kamera</h1>
<p>Sony IMX500 · detekce objektů · náhled přes SSH tunel</p>
<div id="status">Čekám na načtení kamery a modelu…</div>
<img src="/stream.mjpg" alt="Živý obraz s detekcí objektů">
<h2>Rozpoznané objekty</h2><div id="objects"></div>
<p>Jména osob zatím nerozpoznáváme. Obraz se neukládá.</p></main>
<script>
const names={person:'Člověk',car:'Auto',dog:'Pes',cat:'Kočka',bird:'Pták',
bicycle:'Jízdní kolo',motorcycle:'Motocykl',bus:'Autobus',truck:'Nákladní auto',
chair:'Židle',bottle:'Láhev',cup:'Hrnek','cell phone':'Telefon',tv:'Televize',
laptop:'Notebook',book:'Kniha'};
async function update(){try{const s=await(await fetch('/status',{cache:'no-store'})).json();
document.querySelector('#status').textContent=s.error?'Chyba: '+s.error:
s.ready?`Živě · ${s.fps.toFixed(1)} snímků/s · ${s.inference_frames} výsledků AI`:
'Načítám firmware a model do kamery. První spuštění může trvat několik minut…';
const list=document.querySelector('#objects');list.replaceChildren();
for(const d of s.detections){const e=document.createElement('span');e.className='tag';
e.textContent=`${names[d.label]||d.label} · ${Math.round(d.confidence*100)} %`;list.append(e)}
if(!s.detections.length)list.textContent='Žádný objekt nad prahem jistoty 55 %.';
}catch(e){document.querySelector('#status').textContent='Spojení se obnovuje…'}}
setInterval(update,1000);update();</script></html>'''


def camera_worker():
    global frame, sequence
    camera = None
    try:
        imx = IMX500(MODEL)
        intrinsic = imx.network_intrinsics
        if intrinsic is None or intrinsic.task != 'object detection':
            raise RuntimeError('Model neobsahuje konfiguraci detekce objektů')
        intrinsic.update_with_defaults()
        labels = intrinsic.labels
        if not labels:
            raise RuntimeError('Model neobsahuje seznam kategorií')
        if intrinsic.ignore_dash_labels:
            labels = [label for label in labels if label and label != '-']
        camera = Picamera2(imx.camera_num)
        config = camera.create_preview_configuration(
            main={'size': (960, 720), 'format': 'RGB888'},
            controls={'FrameRate': 15}, buffer_count=6)
        camera.configure(config)
        camera.start(show_preview=False)
        if intrinsic.preserve_aspect_ratio:
            imx.set_auto_aspect_ratio()
        previous = []
        last_ai_time = 0
        start = time.monotonic()
        count = 0
        print('Camera started; waiting for inference', flush=True)
        while True:
            request = camera.capture_request()
            try:
                metadata = request.get_metadata()
                image = request.make_array('main').copy()
                tensors = imx.get_outputs(metadata, add_batch=True)
                if tensors is not None:
                    boxes, scores, classes = tensors[0][0], tensors[1][0], tensors[2][0]
                    if intrinsic.bbox_normalization:
                        boxes = boxes / imx.get_input_size()[1]
                    if intrinsic.bbox_order == 'xy':
                        boxes = boxes[:, [1, 0, 3, 2]]
                    previous = []
                    for box, score, category in zip(boxes, scores, classes):
                        category = int(category)
                        if float(score) < 0.55 or not 0 <= category < len(labels):
                            continue
                        rect = imx.convert_inference_coords(box, metadata, camera)
                        previous.append(dict(label=labels[category], confidence=round(float(score), 3),
                                             box=[int(v) for v in rect]))
                    last_ai_time = time.monotonic()
                    with condition:
                        state['inference_frames'] += 1
                detections = previous if time.monotonic() - last_ai_time < 1.5 else []
                for item in detections:
                    x, y, w, h = item['box']
                    cv2.rectangle(image, (x, y), (x+w, y+h), (60, 230, 100), 2)
                    text = f"{item['label']} {item['confidence']:.0%}"
                    cv2.putText(image, text, (max(x, 0), max(y-7, 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 0), 4)
                    cv2.putText(image, text, (max(x, 0), max(y-7, 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (60, 230, 100), 2)
                ok, encoded = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if not ok:
                    raise RuntimeError('JPEG encoder failed')
                count += 1
                with condition:
                    frame = encoded.tobytes()
                    sequence += 1
                    state.update(ready=True, frames=count, fps=round(count/(time.monotonic()-start), 2),
                                 detections=detections, last_frame=time.time())
                    condition.notify_all()
            finally:
                request.release()
    except Exception as exc:
        traceback.print_exc()
        with condition:
            state.update(ready=False, error=str(exc))
            condition.notify_all()
    finally:
        if camera:
            camera.close()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if self.path not in ('/status', '/snapshot.jpg'):
            super().log_message(fmt, *args)

    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            last = -1
            try:
                while True:
                    with condition:
                        condition.wait_for(lambda: sequence != last or state['error'], timeout=10)
                        if state['error']:
                            return
                        if frame is None or sequence == last:
                            continue
                        image, last = frame, sequence
                    self.wfile.write(b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: '+
                                     str(len(image)).encode()+b'\r\n\r\n'+image+b'\r\n')
            except (BrokenPipeError, ConnectionResetError):
                pass
            return
        with condition:
            if self.path == '/status':
                content, mime = json.dumps(state).encode(), 'application/json'
            elif self.path == '/snapshot.jpg' and frame:
                content, mime = frame, 'image/jpeg'
            elif self.path == '/':
                content, mime = PAGE.encode(), 'text/html; charset=utf-8'
            else:
                self.send_error(404)
                return
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    threading.Thread(target=camera_worker, daemon=True).start()
    print('Preview listening on 127.0.0.1:8080', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8080), Handler).serve_forever()
