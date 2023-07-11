
import time
import re
import paramiko

#port = input("Enter serial port name (e.g. COM1 or /dev/ttyUSB0): ")'
ser = serial.Serial('COM4', 9600, timeout=1)
ser.write(b'\n')
output = ser.read(1000)
output_read = output.decode('ascii')
if output_read.endswith('>'):
    ser.write(b'enable\n')
    print('You have entered Privileged Executive mode')
elif output_read.endswith('(config)#'):
    ser.write(b'exit\n')
    print('You have exited from a configuration mode')
elif output_read.endswith('#'):
    pass
else:
    print("Something is wrong. Please manually check the switch.")
    ser.close()
    exit()
ser.write(b'show version | begin Model.Number\n')
time.sleep(1)
output = ser.read(1000)

model_number = None
serial_number = None

model_pattern = r"Model Number\s*:\s*(\S+)"
serial_pattern = r"System Serial Number\s*:\s*(\S+)"

match = re.search(model_pattern, output.decode('ascii'))
if match:
    model_number = match.group(1)

match = re.search(serial_pattern, output.decode('ascii'))
if match:
    serial_number = match.group(1)