#!/usr/bin/python3

import sys, serial, argparse

initPacket = [0xAA, 0x05, 0x14, 0x04, 0x38]

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--init-packet", help="generate intial packet before the given packet e.g.: \"AA 05 14 04 38\"", action="store_true")
parser.add_argument("-s", "--serial", help="send via serial interface", action="store_true")
parser.add_argument("-d", "--device", help="device to read from", default="/dev/ttyUSB0")
parser.add_argument("-b", "--baudrate", help="baudrate", default=19200, type=int)
parser.add_argument("inputs", nargs='*', help="data as hex strings e.g.: \"0xAA 0x07 0x14 0x01 0x00 0x00\" or \"AA 07 14 01 00 00\", multiple packets are supported")
args = parser.parse_args()

retOutput = []
if args.init_packet:
    retOutput += initPacket

inputs = args.inputs

for input in inputs:
    inputStr = input.split()
    inputValues = []
    for s in inputStr:
        inputValues.append(int(s, 16))
    print("Number of bytes:", len(inputValues))

    output = inputValues
    crc = sum(inputValues)
    crc = crc % 256
    crc = crc ^ 0xFF
    output.append(crc)
    retOutput += output

outputStr = ""
for o in retOutput:
    hexStr = "%0.2X" % o
    outputStr += hexStr
    outputStr += " " 

print("Hex data with CRC: \n\t" + outputStr)

if args.serial:
    print("Send data via", args.device, "baudrate:", args.baudrate)
    ser = serial.Serial(args.device, args.baudrate)   
    serialData = bytearray(retOutput)
    ser.write(serialData)
