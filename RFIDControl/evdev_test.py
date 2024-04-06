from evdev import InputDevice, list_devices

devices = [InputDevice(path) for path in list_devices()]
print("Available input devices:")
for device in devices:
    if device.name.find('RFID') == -1:
        continue
    print("-------------------------")
    print("Device Name:", device.name)
    print("Device Path:", device.path)
    print("Device Phys:", device.phys)
    print("Device Unique ID:", device.uniq)
    # print("Device Bus:", device.bus)
    # print("Device Vendor ID:", device.vendor)
    # print("Device Product ID:", device.product)
    print("Device Version ID:", device.version)
    print("Device Capabilities:")
    for capability in device.capabilities(verbose=True):
        print("  -", capability)
    print("-------------------------")