## 使用方法
# > python all_serial_info.py >> record.csv

import serial
import serial.tools.list_ports

plist = list(serial.tools.list_ports.comports())

print("obj", "device", "description", "hwid", "vid", "pid", "serial_number", "location", "manufacturer", "product", "interface", sep=',')
if len(plist) <= 0:
    print("The Serial port can't find!")
else:
    for obj in plist:
        print(obj, obj.device, obj.description, obj.hwid, obj.vid, obj.pid, obj.serial_number, obj.location, obj.manufacturer, obj.product, obj.interface, sep=',')
        