#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Oriëntatie op TI

Voorbeeld voor communicatie met Raspberry Pi Pico. Flash `main.py` in de folder serial/pico/
naar de Raspberry Pi Pico en start dit bestand op je laptop/PC.

(c) 2022 Hogeschool Utrecht,
Hagen Patzke (hagen.patzke@hu.nl) en
Tijmen Muller (tijmen.muller@hu.nl)
"""

from serial.tools import list_ports
import serial


def read_serial(port):
    """Read data from serial port and return as string."""
    line = port.read(1000)
    return line.decode()


# First manually select the serial port that connects to the Pico
serial_ports = list_ports.comports()

print("[INFO] Serial ports found:")
for i, port in enumerate(serial_ports):
    print(str(i) + ". " + str(port.device))

pico_port_index = int(input("Which port is the Raspberry Pi Pico connected to? "))
pico_port = serial_ports[pico_port_index].device

# Open a connection to the Pico
with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    if serial_port.isOpen():
        print("[INFO] Using serial port", serial_port.name)
    else:
        print("[INFO] Opening serial port", serial_port.name, "...")
        serial_port.open()

    try:
        # Request user input
        commands = ['off', 'on', 'exit']
        while True:
            choice = input("Command? [" + ", ".join(commands) + "] ")

            if choice == 'off':
                # Turn led off by sending a '0'
                data = "0\r"
                serial_port.write(data.encode())
                pico_output = read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + pico_output)
            elif choice == 'on':
                # Turn led on by sending a '1'
                data = "1\r"
                serial_port.write(data.encode())
                pico_output = read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + pico_output)
            elif choice == 'exit':
                # Exit user input loop
                break
            else:
                print("[WARN] Unknown command.")

    except KeyboardInterrupt:
        print("[INFO] Ctrl+C detected. Terminating.")
    finally:
        # Close connection to Pico
        serial_port.close()
        print("[INFO] Serial port closed. Bye.")