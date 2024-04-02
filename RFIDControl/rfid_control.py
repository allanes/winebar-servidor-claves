from evdev import InputDevice, categorize, ecodes, list_devices

# Function to capture RFID card data
def capture_rfid_data(reader_path):
    reader = InputDevice(reader_path)
    print(f"Capturing RFID card data from reader: {reader_path}")
    
    while True:
        for event in reader.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                card_number = categorize(event).keycode[len("KEY_"):]
                print(f"RFID card detected on reader {reader_path}: {card_number}")

# List available USB input devices
devices = [InputDevice(path) for path in list_devices()]
devices = [device for device in devices if device.name.find('RFID') >= 0 and device.name.find('Keyboard') >= 0]
print("Available USB input devices:")
for index, device in enumerate(devices, start=1):
    print(f"{index}. {device.name} phys {device.phys}")

# Prompt the user to select RFID card readers
reader_paths = []
while True:
    choice = input("Enter the number of an RFID card reader (or press Enter to finish): ")
    if choice == "":
        break
    try:
        index = int(choice) - 1
        if 0 <= index < len(devices):
            reader_paths.append(devices[index].path)
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Start capturing RFID card data from selected readers
import threading
for reader_path in reader_paths:
    threading.Thread(target=capture_rfid_data, args=(reader_path,)).start()