#!/bin/bash

# Get the script's name
SCRIPT_NAME="$(basename "$0")"

# Get the PID of the current script
SCRIPT_PID="$$"

# Kill all existing instances of the script except for the current one
for pid in $(pgrep -f $SCRIPT_NAME); do
    if [ $pid != $SCRIPT_PID ]; then
        kill -9 $pid
    fi
done

while true; do
    AUDIO_STREAMS=$(pactl list sink-inputs | grep 'state: RUNNING')

    if [[ -z $AUDIO_STREAMS ]]; then
        # Suspend PulseAudio if not already suspended
        pactl list sinks | grep -q "Suspended: yes" || pactl suspend-sink @DEFAULT_SINK@ 1
    else
        # Resume PulseAudio if not already running
        pactl list sinks | grep -q "Suspended: no" || pactl suspend-sink @DEFAULT_SINK@ 0
    fi

    sleep 1
done
