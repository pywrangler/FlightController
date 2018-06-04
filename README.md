I wrote this software to control my wifi controlled RC airplane which uses the nodeMCU ESP8266 wifi capable microcontroller. The python script inside fcn2 reads the events from a joystick like stick position,thrust and button click events.

It feed this data into some equations to map them into appropriate servo positions (with trim and throw control) . Then these values (servo positions and thrust ) are sent through UDP to the ESP8266 which reads and sends corresponding PWM signals to the servos and the ESC of the brusless motor.

The flight controller automatically binds to the nodemcu.

lipo_alert.c is supposed to run on a arduino nano which will monitor the battery voltage levels and pull a digital pin high if one of the cells go low.
The ESP8266 will detect this and alert the pilot by sending back a message to the server.

dependencies: createap (to automatically create the wifi ap)

1.start flightap.py ( in terminal "python flightap.py")
2.set ap name and password in nodemcu code.
3.start fcn and esp8266 (make sure joystick is plugged in)

