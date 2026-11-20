        +----------------- ESP32 -----------------+
        |                                         |
PIR  OUT|--> GPIO13        GPIO5  --> TRIG  HC-SR04
PIR  VCC|--> VIN           GPIO35 <--[div]--- ECHO
PIR  GND|--> GND           VIN    --> VCC
        |                  GND    --> GND
REED ---|--> GPIO27                             |
REED ---|--> GND                                |
        +-----------------------------------------+