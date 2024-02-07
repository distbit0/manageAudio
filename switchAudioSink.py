import os


def execute_command(command):
    print(command)
    os.system(command)

def get_sinks():
    execute_command("pactl list sinks short > tmp_sinks.txt")
    sinks = []
    with open("tmp_sinks.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        sink_id, name = line.split()[0], line.split()[1]
        sinks.append({"id": sink_id, "name": name})
    os.remove("tmp_sinks.txt")
    return sinks


def get_default_sink():
    execute_command("pactl info > tmp_info.txt")
    with open("tmp_info.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        if "Default Sink: " in line:
            os.remove("tmp_info.txt")
            return line.split(": ")[1].strip()
    os.remove("tmp_info.txt")


def set_default_sink(sink_name):
    execute_command(f"pactl set-default-sink {sink_name}")


def main():
    sinks = get_sinks()
    default_sink = get_default_sink()

    bluetooth_sink = None
    speaker_sink = None

    for sink in sinks:
        if "bluez" in sink["name"]:
            bluetooth_sink = sink["name"]
        else:
            speaker_sink = sink["name"]

    if default_sink == bluetooth_sink:
        set_default_sink(speaker_sink)
        print("Switched to Speaker.")
    else:
        set_default_sink(bluetooth_sink)
        print("Switched to Bluetooth.")


if __name__ == "__main__":
    main()
