#!/bin/sh
set -eu

echo '== OpenClaw gateway =='
openclaw gateway status || true

echo
echo '== OpenClaw browser =='
openclaw browser status || true

echo
echo '== Open tabs =='
openclaw browser tabs || true

echo
echo 'Next steps:'
echo '1. Run: openclaw browser start'
echo '2. Open and log into Jimeng in the OpenClaw browser.'
echo '3. Keep the Jimeng image-generation page visible before attempting manual/semi-auto submission.'
