#!/bin/sh

# Create FIFOs to send input to the server
mkfifo stdin stdout stderr

# Keep input FIFO alive
sleep infinity > stdin &

# Start the server
./scripts/run.py < stdin > stdout 2> stderr &
SERVER_PID=$!

# Redirect server output to shell
cat < stdout &
cat < stderr >&2 &

# Gracefully handle signals
cleanup() {
    echo "Cleaning up!"
    echo "save-all" > stdin
    echo "stop" > stdin
    wait $SERVER_PID
}
trap "cleanup" SIGTERM SIGINT

# Redirect shell input to server
cat > stdin

# If cat terminated, we must not be running interactively.
wait $SERVER_PID
