#!/bin/bash

while true; do
    AUDIO_STREAMS=$(pacmd list-sink-inputs | grep 'state: RUNNING')

    if [[ -z $AUDIO_STREAMS ]]; then
        # Suspend PulseAudio if not already suspended
        pactl list sinks | grep -q "Suspended: yes" || pactl suspend-sink @DEFAULT_SINK@ 1
    else
        # Resume PulseAudio if not already running
        pactl list sinks | grep -q "Suspended: no" || pactl suspend-sink @DEFAULT_SINK@ 0
    fi

    sleep 1
done
