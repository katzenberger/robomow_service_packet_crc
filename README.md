# Robomow service packet CRC calculator tool
This tool is a helper for reverse engeneering Robomow's service UART protocol.
It can calculate CRC value for a packet and send it via UART.
Multiple packets are supported in one command.
## About Robomow's service protocol
### Packet structure
```
0xAA - premable
0x55 - length included preamble, length, payload and crc
.
.
.
0xA2 - crc
```
### CRC calculation
Sum all bytes and bitvise invert the result.
```
crc = sum(allBytes)
crc = crc % 256
crc = crc ^ 0xFF
```
## Usage
```
./robomow_service_packet_crc.py -b 9600 -d /dev/ttyACM0 -s "aa 55 14 01 00 42 42 00 00 00 02 00 00 00 03 03 11 12 03 03 00 00 00 00 00 00 00 00 00 00 00 00 16 00 00 00 00 00 00 00 00 00 15 00 15 00 00 00 00 64 fb 00 15 00 25 a8 00 02 00 00 00 1d 00 00 01 38 00 00 00 11 00 00 00 00 00 00 00 5d 00 1e 02 04 29 00" "aa 0b 14 0b 00 00 00 00 00 39" "AA 0B 14 0B 00 00 00 00 00 35"
```
Three input packages (without CRC):
```
"aa 55 14 01 00 42 42 00 00 00 02 00 00 00 03 03 11 12 03 03 00 00 00 00 00 00 00 00 00 00 00 00 16 00 00 00 00 00 00 00 00 00 15 00 15 00 00 00 00 64 fb 00 15 00 25 a8 00 02 00 00 00 1d 00 00 01 38 00 00 00 11 00 00 00 00 00 00 00 5d 00 1e 02 04 29 00"

"aa 0b 14 0b 00 00 00 00 00 39"

"AA 0B 14 0B 00 00 00 00 00 35"
```
Results (with CRC):
```
AA 05 14 04 38 AA 55 14 01 00 42 42 00 00 00 02 00 00 00 03 03 11 12 03 03 00 00 00 00 00 00 00 00 00 00 00 00 16 00 00 00 00 00 00 00 00 00 15 00 15 00 00 00 00 64 FB 00 15 00 25 A8 00 02 00 00 00 1D 00 00 01 38 00 00 00 11 00 00 00 00 00 00 00 5D 00 1E 02 04 29 00 A2

AA 0B 14 0B 00 00 00 00 00 39 F2

AA 0B 14 0B 00 00 00 00 00 35 F6
```
## Additional info
In some cases the RM toolkit expect an initial packet before the service packet. It is a fix packet and the script can send it before the given packet.
Use `-i` argument to send fix `AA 05 14 04 38` packet before all given packets.
