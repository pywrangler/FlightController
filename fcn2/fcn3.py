# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import os, struct, array
from fcntl import ioctl
import socket



# def getIP():
#     foundflag = False
#     espMAC = "2c:3a:e8:43:81:66"
#     hostlist = os.popen("arp -a").read().split()
#     macind = 3
#     while(foundflag == False):
#         for macind in range(3,len(hostlist),7):
#             if(hostlist[macind] == espMAC):
#                 foundflag = True
#                 espIP = str(hostlist[macind-2]).strip()
#                 espIP = espIP[1:len(espIP)-1] #removing leading and trailing parantheses
#                 APif = hostlist[macind+3]
#                 print "espIP is",espIP
#                 print "Interface name: ",APif
espPort = 4210
espIP = "192.168.12.231"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
espMAC = "2c:3a:e8:43:81:66"
hostlist = os.popen("arp -a").read().split()
macind = 3
foundflag = True
while(foundflag == False):
    for macind in range(3,len(hostlist),7):
        if(hostlist[macind] == espMAC):
            foundflag = True
            espIP = str(hostlist[macind-2])
            espIP = espIP[1:len(espIP)-1] #removing leading and trailing parantheses
            APif = hostlist[macind+3]
            print "espIP is ",espIP
            print "Interface name: ",APif
# Iterate over the joystick devices.
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))

axis_states = {}
button_states = {}

# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'throttle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',


    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []

# Open the joystick device.
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')

# Get the device name.
#buf = bytearray(63)
buf = array.array('c', ['\0'] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tostring()
print('Device name: %s' % js_name)

# Get number of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]

# Get the axis map.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

# Get the button map.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
    btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
    button_map.append(btn_name)
    button_states[btn_name] = 0

print '%d axes found: %s' % (num_axes, ', '.join(axis_map))
print '%d buttons found: %s' % (num_buttons, ', '.join(button_map))

s1 = 0
s2 = 0
base = 0
diff = 0
fsp = 0
cd = ''
Lutrw = 90  #left  throw
Rutrw = 90 #right  throw
Ltr = 0  #left elevon trim
Rtr = 0 #right elevon trim
rfsp = 70 #throttle cache for throttle boost
indUP = False
inddow = False
#-------------------------------------------------------------------------
# Main event loop

#sock.bind((espIP,4210))
while True:

    evbuf = jsdev.read(8)
    if evbuf:
        time, val, type, num = struct.unpack('IhBB', evbuf)
        if(type == 2):  #type 2 means stick movement or throt wheel
            if(num == 0):
                diff = val
            elif(num == 1):
                base = val
            else:
                fsp = ((32768-val) * 110 / 65596)+56
        else:
            if(num==1 ):
                if(val == 1):
                    rfsp = fsp
                    fsp = 130 #servowrite(160) means full throttle
                else:
                    fsp = rfsp
            elif (num == 3 and val ==1):
                if(indUP == True):
                    Ltr +=3
                elif (inddow == True):
                    Ltr -=3
                else:
                    Ltr -=3
                    Rtr+=3
            elif (num == 4 and val ==1 ):
                if(indUP == True):
                    Rtr +=3
                elif (inddow == True):
                    Rtr -=3
                else:
                    Rtr -=3
                    Ltr+=3
            elif (num == 5 ):
                if(val == 1):
                    indUP = True
                else:
                    indUP = False
            elif (num == 6 ):
                if(val == 1):
                    inddow = True
                else:
                    inddow = False

        s1 =max(min(((((max(min(32760, (diff-base) ), -32760))/32760.0)+1)*Lutrw)+Ltr,180),0)
        s2 = max(min(((((max(min(32760, (diff+base) ), -32760))/32760.0)+1)*Rutrw)+Rtr,180),0)
        cd = ('%03d' % s1)+('%03d' % s2)+('%03d' % fsp)
        print cd
        sock.sendto( cd, (espIP, espPort))
