"""
Configuration settings.
Only edit this file when changing ports or balance settings.
"""

import serial

# -------------------------------
# Serial Settings
# -------------------------------

SERIAL_PORT = "COM3"
BAUD_RATE = 9600
DATA_BITS = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOP_BITS = serial.STOPBITS_ONE
TIMEOUT = 1