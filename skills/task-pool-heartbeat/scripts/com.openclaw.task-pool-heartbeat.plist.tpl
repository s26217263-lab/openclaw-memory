<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>__LAUNCH_LABEL__</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>__PROJECT_ROOT__/scripts/task_pool_heartbeat.sh</string>
  </array>
  <key>StartInterval</key>
  <integer>300</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>__PROJECT_ROOT__/logs/task_pool_heartbeat.launchd.log</string>
  <key>StandardErrorPath</key>
  <string>__PROJECT_ROOT__/logs/task_pool_heartbeat.launchd.err.log</string>
</dict>
</plist>
