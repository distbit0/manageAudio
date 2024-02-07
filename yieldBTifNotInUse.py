import os
import subprocess
import time

def run_command(command):
    """Executes a shell command and returns its output along with any errors."""
    try:
        completed_process = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return completed_process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None

def main():
    script_name = os.path.basename(__file__)
    script_pid = os.getpid()
    print(f"Script Name: {script_name}, Script PID: {script_pid}")

    # Kill all existing instances of the script except for the current one
    pids = run_command(f"pgrep -f {script_name}")
    if pids:
        pids = pids.split('\n')
        for pid in pids:
            if pid and int(pid) != script_pid:
                print(f"Killing process with PID: {pid}")
                run_command(f"kill -9 {pid}")

    while True:
        audio_streams = run_command("pactl list sink-inputs | grep 'state: RUNNING'")
        print(f"Audio Streams: {audio_streams}")

        if not audio_streams:
            # Suspend PulseAudio if not already suspended
            is_suspended = run_command("pactl list sinks | grep -q 'Suspended: yes'")
            if not is_suspended:
                print("Suspending PulseAudio")
                run_command("pactl suspend-sink @DEFAULT_SINK@ 1")
        else:
            # Resume PulseAudio if not already running
            is_running = run_command("pactl list sinks | grep -q 'Suspended: no'")
            if not is_running:
                print("Resuming PulseAudio")
                run_command("pactl suspend-sink @DEFAULT_SINK@ 0")

        time.sleep(1)

if __name__ == "__main__":
    main()
