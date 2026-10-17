# Append this block to the user's labwc autostart, preserving existing commands.
# A new user autostart must also run /etc/xdg/labwc/autostart in the background.
# BEGIN ProMichAiCam1 display
systemctl --user import-environment WAYLAND_DISPLAY DISPLAY XDG_SESSION_TYPE
systemctl --user start ai-camera-display.service
# END ProMichAiCam1 display
