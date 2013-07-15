# -*- coding: utf-8 -*-
from hachi.const import (TRANSMIT_OPTION_BROADCAST_PACKET, ADDRESS_16_BROADCAST,
    TRANSMIT_OPTION_DISABLE_ACKNOWLEDGEMENT, ADDRESS_16_USE_64_BIT_ADDRESSING,
    BROADCAST_RADIUS_MAX_HOPS, TRANSMIT_OPTION_APPLY_CHANGES, ADDRESS_64_COORDINATOR,
    FRAME_DELIMITER, ESCAPE, XON, XOFF)
from hachi.core import escape, escape_frame, unescape, XBee
from hachi.request import (Tx64Request, Tx16Request, AtRequest, AtQueueRequest,
    ZBTxRequest, RemoteAtRequest, ZBExplicitTxRequest)
from hachi.response import (RemoteAtResponse, Rx16Response, Rx64Response,
    ZBRxResponse, AtResponse, ModemStatusResponse, TxStatusResponse,
    ZBTxStatusResponse, ZBExplicitRxResponse, ZBIoSampleResponse,
    Rx16IoSampleResponse, Rx64IoSampleResponse, bitcount)
import unittest


class ResponseTestCase(unittest.TestCase):
    def test_XBeeResponse_wrong_api_id(self):
        frame = bytearray.fromhex('7E 00 0A 81 52 1A 23 01 12 33 85 A1 F2 91')
        with self.assertRaises(ValueError):
            Rx64Response(frame)

    def test_Rx64Response(self):
        frame = bytearray.fromhex('7E 00 10 80 00 13 A2 00 40 52 2B AA 16 03 F1 2E AA BD C9 FB')
        packet = Rx64Response(frame)
        self.assertTrue(packet.length == 16)
        self.assertTrue(packet.api_id == 0x80)
        self.assertTrue(packet.source_address == (0x00 << 8 * 7) + (0x13 << 8 * 6) + (0xa2 << 8 * 5) + (0x00 << 8 * 4) + (0x40 << 8 * 3) + (0x52 << 8 * 2) + (0x2b << 8) + 0xaa)
        self.assertTrue(packet.rssi == 0x16)
        self.assertTrue(packet.options == 0x03)
        self.assertTrue(packet.data[0] == 0xf1)
        self.assertTrue(packet.data[1] == 0x2e)
        self.assertTrue(packet.data[2] == 0xaa)
        self.assertTrue(packet.data[3] == 0xbd)
        self.assertTrue(packet.data[4] == 0xc9)
        self.assertTrue(packet.checksum == 0xfb)
        self.assertTrue(packet.verify())

    def test_Rx16Response(self):
        frame = bytearray.fromhex('7E 00 0A 81 52 1A 23 01 12 33 85 A1 F2 91')
        packet = Rx16Response(frame)
        self.assertTrue(packet.length == 10)
        self.assertTrue(packet.api_id == 0x81)
        self.assertTrue(packet.source_address == (0x52 << 8) + 0x1a)
        self.assertTrue(packet.rssi == 0x23)
        self.assertTrue(packet.options == 0x01)
        self.assertTrue(packet.data[0] == 0x12)
        self.assertTrue(packet.data[1] == 0x33)
        self.assertTrue(packet.data[2] == 0x85)
        self.assertTrue(packet.data[3] == 0xa1)
        self.assertTrue(packet.data[4] == 0xf2)
        self.assertTrue(packet.checksum == 0x91)
        self.assertTrue(packet.verify())

    def test_AtResponse(self):
        frame = bytearray.fromhex('7E 00 07 88 52 4D 59 00 00 00 7F')
        packet = AtResponse(frame)
        self.assertTrue(packet.length == 7)
        self.assertTrue(packet.api_id == 0x88)
        self.assertTrue(packet.frame_id == 0x52)
        self.assertTrue(packet.command == 'MY')
        self.assertTrue(packet.status == 0x00)
        self.assertTrue(packet.value[0] == 0x00)
        self.assertTrue(packet.value[1] == 0x00)
        self.assertTrue(packet.checksum == 0x7f)
        self.assertTrue(packet.verify())

    def test_ModemStatusResponse(self):
        frame = bytearray.fromhex('7E 00 02 8A 06 6F')
        packet = ModemStatusResponse(frame)
        self.assertTrue(packet.length == 2)
        self.assertTrue(packet.api_id == 0x8a)
        self.assertTrue(packet.status == 0x06)
        self.assertTrue(packet.checksum == 0x6f)
        self.assertTrue(packet.verify())

    def test_ZBRxResponse(self):
        frame = bytearray.fromhex('7E 00 12 90 00 00 13 A2 00 40 52 2B AA 7D 84 01 52 78 44 61 74 61 0D')
        packet = ZBRxResponse(frame)
        self.assertTrue(packet.length == 18)
        self.assertTrue(packet.api_id == 0x90)
        self.assertTrue(packet.frame_id == 0x00)
        self.assertTrue(packet.source_address_64 == (0x00 << 8 * 7) + (0x13 << 8 * 6) + (0xa2 << 8 * 5) + (0x00 << 8 * 4) + (0x40 << 8 * 3) + (0x52 << 8 * 2) + (0x2b << 8) + 0xaa)
        self.assertTrue(packet.source_address_16 == (0x7d << 8) + 0x84)
        self.assertTrue(packet.options == 0x01)
        self.assertTrue(packet.data[0] == 0x52)
        self.assertTrue(packet.data[1] == 0x78)
        self.assertTrue(packet.data[2] == 0x44)
        self.assertTrue(packet.data[3] == 0x61)
        self.assertTrue(packet.data[4] == 0x74)
        self.assertTrue(packet.data[5] == 0x61)
        self.assertTrue(packet.checksum == 0x0d)
        self.assertTrue(packet.verify())

    def test_RemoteAtResponse(self):
        frame = bytearray.fromhex('7E 00 13 97 55 00 13 A2 00 40 52 2B AA 7D 84 53 4C 00 40 52 2B AA F0')
        packet = RemoteAtResponse(frame)
        self.assertTrue(packet.length == 19)
        self.assertTrue(packet.api_id == 0x97)
        self.assertTrue(packet.frame_id == 0x55)
        self.assertTrue(packet.source_address_64 == (0x00 << 8 * 7) + (0x13 << 8 * 6) + (0xa2 << 8 * 5) + (0x00 << 8 * 4) + (0x40 << 8 * 3) + (0x52 << 8 * 2) + (0x2b << 8) + 0xaa)
        self.assertTrue(packet.source_address_16 == (0x7d << 8) + 0x84)
        self.assertTrue(packet.command == 'SL')
        self.assertTrue(packet.status == 0x00)
        self.assertTrue(packet.data[0] == 0x40)
        self.assertTrue(packet.data[1] == 0x52)
        self.assertTrue(packet.data[2] == 0x2b)
        self.assertTrue(packet.data[3] == 0xaa)
        self.assertTrue(packet.checksum == 0xf0)
        self.assertTrue(packet.verify())

    def test_TxStatusResponse(self):
        frame = bytearray.fromhex('7E 00 03 89 2A 74 D8')
        packet = TxStatusResponse(frame)
        self.assertTrue(packet.length == 3)
        self.assertTrue(packet.api_id == 0x89)
        self.assertTrue(packet.frame_id == 0x2a)
        self.assertTrue(packet.status == 0x74)
        self.assertTrue(packet.checksum == 0xd8)
        self.assertTrue(packet.verify())

    def test_ZBTxStatusResponse(self):
        frame = bytearray.fromhex('7E 00 07 8B 01 7D 84 00 00 01 71')
        packet = ZBTxStatusResponse(frame)
        self.assertTrue(packet.length == 7)
        self.assertTrue(packet.api_id == 0x8b)
        self.assertTrue(packet.frame_id == 0x01)
        self.assertTrue(packet.destination_address == (0x7d << 8) + 0x84)
        self.assertTrue(packet.retry_count == 0x00)
        self.assertTrue(packet.delivery_status == 0x00)
        self.assertTrue(packet.discovery_status == 0x01)
        self.assertTrue(packet.checksum == 0x71)
        self.assertTrue(packet.verify())

    def test_ZBExplicitRxResponse(self):
        frame = bytearray.fromhex('7E 00 18 91 00 13 A2 00 40 52 2B AA 7D 84 E0 E0 22 11 C1 05 02 52 78 44 61 74 61 52')
        packet = ZBExplicitRxResponse(frame)
        self.assertTrue(packet.length == 24)
        self.assertTrue(packet.api_id == 0x91)
        self.assertTrue(packet.source_address_64 == (0x00 << 8 * 7) + (0x13 << 8 * 6) + (0xa2 << 8 * 5) + (0x00 << 8 * 4) + (0x40 << 8 * 3) + (0x52 << 8 * 2) + (0x2b << 8) + 0xaa)
        self.assertTrue(packet.source_address_16 == (0x7d << 8) + 0x84)
        self.assertTrue(packet.source_endpoint == 0xe0)
        self.assertTrue(packet.destination_endpoint == 0xe0)
        self.assertTrue(packet.cluster_id == (0x22 << 8) + 0x11)
        self.assertTrue(packet.profile_id == (0xc1 << 8) + 0x05)
        self.assertTrue(packet.options == 0x02)
        self.assertTrue(packet.data[0] == 0x52)
        self.assertTrue(packet.data[1] == 0x78)
        self.assertTrue(packet.data[2] == 0x44)
        self.assertTrue(packet.data[3] == 0x61)
        self.assertTrue(packet.data[4] == 0x74)
        self.assertTrue(packet.data[5] == 0x61)
        self.assertTrue(packet.checksum == 0x52)
        self.assertTrue(packet.verify())

    def test_ZBIoSampleResponse(self):
        frame = bytearray.fromhex('7E 00 14 92 00 13 A2 00 40 52 2B AA 7D 84 01 01 00 1C 02 00 14 02 25 F5')
        packet = ZBIoSampleResponse(frame)
        self.assertTrue(packet.length == 20)
        self.assertTrue(packet.api_id == 0x92)
        self.assertTrue(packet.source_address_64 == (0x00 << 8 * 7) + (0x13 << 8 * 6) + (0xa2 << 8 * 5) + (0x00 << 8 * 4) + (0x40 << 8 * 3) + (0x52 << 8 * 2) + (0x2b << 8) + 0xaa)
        self.assertTrue(packet.source_address_16 == (0x7d << 8) + 0x84)
        self.assertTrue(packet.options == 0x01)
        self.assertTrue(packet.sample_count == 0x01)
        self.assertTrue(packet.digital_mask == (0x00 << 8) + 0x1c)
        self.assertTrue(packet.analog_mask == 0x02)
        self.assertTrue(packet.contains_digital == True)
        self.assertTrue(packet.contains_analog == True)
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12]:
            if i == 2:
                self.assertTrue(packet.is_digital_enabled(i) == True)
                self.assertTrue(packet.is_digital_on(i) == True)
            elif i == 3:
                self.assertTrue(packet.is_digital_enabled(i) == True)
                self.assertTrue(packet.is_digital_on(i) == False)
            elif i == 4:
                self.assertTrue(packet.is_digital_enabled(i) == True)
                self.assertTrue(packet.is_digital_on(i) == True)
            else:
                self.assertTrue(packet.is_digital_enabled(i) == False)
                with self.assertRaises(ValueError):
                    packet.is_digital_on(i)
        for i in range(4):
            if i == 1:
                self.assertTrue(packet.is_analog_enabled(i) == True)
                self.assertTrue(packet.get_analog(i) == 549)
            else:
                self.assertTrue(packet.is_analog_enabled(i) == False)
        self.assertTrue(packet.checksum == 0xf5)
        self.assertTrue(packet.verify())

    def test_Rx16IoSampleResponse(self):
        frame = bytearray.fromhex('7E 00 14 83 7D 84 23 01 02 14 88 00 80 00 8F 03 ED 00 08 02 4C 00 0C 58')
        packet = Rx16IoSampleResponse(frame)
        self.assertTrue(packet.length == 20)
        self.assertTrue(packet.api_id == 0x83)
        self.assertTrue(packet.source_address == (0x7d << 8) + 0x84)
        self.assertTrue(packet.rssi == 0x23)
        self.assertTrue(packet.options == 0x01)
        self.assertTrue(packet.sample_count == 0x02)
        self.assertTrue(packet.analog_mask == 0x14)
        self.assertTrue(packet.digital_mask == (0x00 << 8) + 0x88)
        self.assertTrue(packet.contains_analog == True)
        self.assertTrue(packet.contains_digital == True)
        for i in range(6):
            if i in [1, 3]:  # analog pins 1 and 3 enabled
                self.assertTrue(packet.is_analog_enabled(i) == True)
            else:
                self.assertTrue(packet.is_analog_enabled(i) == False)
        for i in range(9):
            if i in [3, 7]:  # digital pins 3 and 7 enabled
                self.assertTrue(packet.is_digital_enabled(i) == True)
            else:
                self.assertTrue(packet.is_digital_enabled(i) == False)
        for i in range(2):
            for j in range(9):
                # digital pins
                if j == 7:  # digital pin 7 is on during first sample only
                    if i == 0:
                        self.assertTrue(packet.is_digital_on(i, j) == True)
                    elif i == 1:
                        self.assertTrue(packet.is_digital_on(i, j) == False)
                elif j == 3:  # digital pin 3 is on during second sample only
                    if i == 1:
                        self.assertTrue(packet.is_digital_on(i, j) == True)
                    elif i == 0:
                        self.assertTrue(packet.is_digital_on(i, j) == False)
                else:
                    with self.assertRaises(ValueError):
                        packet.is_digital_on(i, j)
                # analog pins
                if j < 6:
                    if j == 1:  # analog pin 1 gives 143 and 588
                        if i == 0:
                            self.assertTrue(packet.get_analog(i, j) == 143)
                        elif i == 1:
                            self.assertTrue(packet.get_analog(i, j) == 588)
                    elif j == 3:  # analog pin 3 gives 1005 and 12
                        if i == 0:
                            self.assertTrue(packet.get_analog(i, j) == 1005)
                        elif i == 1:
                            self.assertTrue(packet.get_analog(i, j) == 12)
                    else:
                        with self.assertRaises(ValueError):
                            packet.get_analog(i, j)
        self.assertTrue(packet.checksum == 0x58)
        self.assertTrue(packet.verify())

    def test_Rx64IoSampleResponse(self):
        frame = bytearray.fromhex('7E 00 14 82 00 13 A2 00 40 52 2B AA 23 01 02 14 88 00 80 00 8F 03 ED 00 08 02 4C 00 0C 3E')
        packet = Rx64IoSampleResponse(frame)
        self.assertTrue(packet.length == 20)
        self.assertTrue(packet.api_id == 0x82)
        self.assertTrue(packet.source_address == (0x00 << 8 * 7) + (0x13 << 8 * 6) + (0xa2 << 8 * 5) + (0x00 << 8 * 4) + (0x40 << 8 * 3) + (0x52 << 8 * 2) + (0x2b << 8) + 0xaa)
        self.assertTrue(packet.rssi == 0x23)
        self.assertTrue(packet.options == 0x01)
        self.assertTrue(packet.sample_count == 0x02)
        self.assertTrue(packet.analog_mask == 0x14)
        self.assertTrue(packet.digital_mask == (0x00 << 8) + 0x88)
        self.assertTrue(packet.contains_analog == True)
        self.assertTrue(packet.contains_digital == True)
        for i in range(6):
            if i in [1, 3]:  # analog pins 1 and 3 enabled
                self.assertTrue(packet.is_analog_enabled(i) == True)
            else:
                self.assertTrue(packet.is_analog_enabled(i) == False)
        for i in range(9):
            if i in [3, 7]:  # digital pins 3 and 7 enabled
                self.assertTrue(packet.is_digital_enabled(i) == True)
            else:
                self.assertTrue(packet.is_digital_enabled(i) == False)
        for i in range(2):
            for j in range(9):
                # digital pins
                if j == 7:  # digital pin 7 is on during first sample only
                    if i == 0:
                        self.assertTrue(packet.is_digital_on(i, j) == True)
                    elif i == 1:
                        self.assertTrue(packet.is_digital_on(i, j) == False)
                elif j == 3:  # digital pin 3 is on during second sample only
                    if i == 1:
                        self.assertTrue(packet.is_digital_on(i, j) == True)
                    elif i == 0:
                        self.assertTrue(packet.is_digital_on(i, j) == False)
                else:
                    with self.assertRaises(ValueError):
                        packet.is_digital_on(i, j)
                # analog pins
                if j < 6:
                    if j == 1:  # analog pin 1 gives 143 and 588
                        if i == 0:
                            self.assertTrue(packet.get_analog(i, j) == 143)
                        elif i == 1:
                            self.assertTrue(packet.get_analog(i, j) == 588)
                    elif j == 3:  # analog pin 3 gives 1005 and 12
                        if i == 0:
                            self.assertTrue(packet.get_analog(i, j) == 1005)
                        elif i == 1:
                            self.assertTrue(packet.get_analog(i, j) == 12)
                    else:
                        with self.assertRaises(ValueError):
                            packet.get_analog(i, j)
        self.assertTrue(packet.checksum == 0x3e)
        self.assertTrue(packet.verify())

    def test_bitcount(self):
        self.assertTrue(bitcount(0b00100110) == 3)
        self.assertTrue(bitcount(0b10001) == 2)


class RequestTestCase(unittest.TestCase):
    def test_Tx64Request(self):
        request = Tx64Request(bytearray([0x88, 0x66]))
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 0D 00 01 00 00 00 00 00 00 00 00 00 88 66 10'))
        self.assertTrue(request.length == 13)
        self.assertTrue(request.checksum == 0x10)
        request = Tx64Request(bytearray([0x12, 0x34, 0x56]), 0x112233445566, TRANSMIT_OPTION_BROADCAST_PACKET, 0x23)
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 0E 00 23 00 00 11 22 33 44 55 66 04 12 34 56 D7'))
        self.assertTrue(request.length == 14)
        self.assertTrue(request.checksum == 0xd7)

    def test_Tx16Request(self):
        request = Tx16Request(bytearray([0x88, 0x66]), 0x1234)
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 07 01 01 12 34 00 88 66 C9'))
        self.assertTrue(request.length == 7)
        self.assertTrue(request.checksum == 0xc9)
        request = Tx16Request(bytearray([0x12, 0x34, 0x56]), ADDRESS_16_BROADCAST, TRANSMIT_OPTION_DISABLE_ACKNOWLEDGEMENT, 0x42)
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 08 01 42 FF FF 01 12 34 56 21'))
        self.assertTrue(request.length == 8)
        self.assertTrue(request.checksum == 0x21)

    def test_AtRequest(self):
        request = AtRequest('SP')
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 04 08 01 53 50 53'))
        self.assertTrue(request.length == 4)
        self.assertTrue(request.checksum == 0x53)
        request = AtRequest('SP', bytearray([0x07, 0xd0]))
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 06 08 01 53 50 07 D0 7C'))
        self.assertTrue(request.length == 6)
        self.assertTrue(request.checksum == 0x7c)

    def test_AtQueueRequest(self):
        request = AtQueueRequest('SP')
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 04 09 01 53 50 52'))
        self.assertTrue(request.length == 4)
        self.assertTrue(request.checksum == 0x52)
        request = AtQueueRequest('SP', bytearray([0x07, 0xd0]))
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 06 09 01 53 50 07 D0 7B'))
        self.assertTrue(request.length == 6)
        self.assertTrue(request.checksum == 0x7b)

    def test_ZBTxRequest(self):
        request = ZBTxRequest(bytearray([0x88, 0x66]))
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 10 10 01 00 00 00 00 00 00 00 00 FF FE 00 00 88 66 03'))
        self.assertTrue(request.length == 16)
        self.assertTrue(request.checksum == 0x03)
        request = ZBTxRequest(bytearray([0x54, 0x78, 0x44, 0x61, 0x74, 0x61, 0x30, 0x41]), 0x13a200400a0127, ADDRESS_16_USE_64_BIT_ADDRESSING,
                              BROADCAST_RADIUS_MAX_HOPS, 0x00, 0x01)
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 16 10 01 00 13 A2 00 40 0A 01 27 FF FE 00 00 54 78 44 61 74 61 30 41 13'))
        self.assertTrue(request.length == 22)
        self.assertTrue(request.checksum == 0x13)

    def test_ZBExplicitTxRequest(self):
        request = ZBExplicitTxRequest(bytearray([0x54, 0x78, 0x44, 0x61, 0x74, 0x61]), ADDRESS_64_COORDINATOR, 0xa0, 0xa1, 0x1554, 0xc105,
                                      ADDRESS_16_USE_64_BIT_ADDRESSING, BROADCAST_RADIUS_MAX_HOPS, 0x00, 0x01)
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 1A 11 01 00 00 00 00 00 00 00 00 FF FE A0 A1 15 54 C1 05 00 00 54 78 44 61 74 61 3A'))
        self.assertTrue(request.length == 26)
        self.assertTrue(request.checksum == 0x3a)

    def test_RemoteAtRequest(self):
        request = RemoteAtRequest('SP', 0x112233445566)
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 0F 17 01 00 00 11 22 33 44 55 66 FF FE 02 53 50 E0'))
        self.assertTrue(request.length == 15)
        self.assertTrue(request.checksum == 0xe0)
        request = RemoteAtRequest('BH', 0x0013a20040401122, bytearray([0x01]), ADDRESS_16_USE_64_BIT_ADDRESSING, TRANSMIT_OPTION_APPLY_CHANGES, 0x01)
        self.assertTrue(request.frame == bytearray.fromhex('7E 00 10 17 01 00 13 A2 00 40 40 11 22 FF FE 02 42 48 01 F5'))
        self.assertTrue(request.length == 16)
        self.assertTrue(request.checksum == 0xf5)


class XBeeTestCase(unittest.TestCase):
    def setUp(self):
        self.xbee = XBee(self.callback)
        self.responses = []

    def callback(self, response):
        self.responses.append(response)

    def test_feed_no_escape(self):
        self.xbee.feed(b'~\x00\x03\x89*t\xd8')
        self.assertTrue(len(self.responses) == 1)
        self.assertTrue(isinstance(self.responses[0], TxStatusResponse))
        self.assertTrue(isinstance(self.xbee.response, TxStatusResponse))
        self.assertTrue(len(self.xbee.buffer) == 7)  # no special byte

    def test_feed_escape(self):
        frame = bytearray.fromhex('7E 00 12 92 00 7D 33 A2 00 40 A0 96 7D 5E 0F 25 41 01 00 00 01 02 80 CB')
        for b in frame:
            self.xbee.feed(b)
        self.assertTrue(len(self.responses) == 1)
        self.assertTrue(isinstance(self.responses[0], ZBIoSampleResponse))
        self.assertTrue(isinstance(self.xbee.response, ZBIoSampleResponse))
        self.assertTrue(len(self.xbee.buffer) == 22)  # 2 special bytes

    def test_feed_incomplete(self):
        frame = bytearray.fromhex('7E 00 03 89 2A')
        for b in frame:
            self.xbee.feed(b)
        self.assertTrue(len(self.responses) == 0)
        self.assertTrue(self.xbee.response is None)
        self.assertTrue(len(self.xbee.buffer) == 5)  # 2 special bytes

    def test_feed_invalid_checksum(self):
        frame = bytearray.fromhex('7E 00 03 89 2A 74 DD')
        for b in frame:
            self.xbee.feed(b)
        self.assertTrue(len(self.responses) == 0)
        self.assertTrue(self.xbee.response is None)
        self.assertTrue(len(self.xbee.buffer) == 0)

    def test_feed_multiple(self):
        self.xbee.feed(bytearray.fromhex('7E 00 03 89 2A 74 D8 7E 00 12 92 00 7D 33 A2 00 40 A0 96 7D 5E 0F 25 41 01 00 00 01 02 80 CB'))
        self.assertTrue(len(self.responses) == 2)
        self.assertTrue(isinstance(self.responses[0], TxStatusResponse))
        self.assertTrue(isinstance(self.responses[1], ZBIoSampleResponse))
        self.assertTrue(isinstance(self.xbee.response, ZBIoSampleResponse))
        self.assertTrue(len(self.xbee.buffer) == 22)

    def test_escape(self):
        for special_byte in (FRAME_DELIMITER, ESCAPE, XON, XOFF):
            self.assertTrue(0x20 ^ escape(special_byte) == special_byte)
        with self.assertRaises(ValueError):
            escape(0x01)

    def test_escape_frame(self):
        frame = bytearray.fromhex('7E 00 03 89 2A 74 D8 7E 00 12 92 00 7D 33 A2 00 40 A0 96 7D 5E 0F 25 41 01 00 00 01 02 80 CB')
        escaped_frame = escape_frame(frame)
        self.assertTrue(escaped_frame == bytearray.fromhex('7E 00 03 89 2A 74 D8 7D 5E 00 12 92 00 7D 5D 33 A2 00 40 A0 96 7D 5D 5E 0F 25 41 01 00 00 01 02 80 CB'))

    def test_escape_frame_bad_frame(self):
        frame = bytearray.fromhex('00 03 89 2A')
        with self.assertRaises(ValueError):
            escape_frame(frame)

    def test_unescape(self):
        for special_byte in (FRAME_DELIMITER, ESCAPE, XON, XOFF):
            self.assertTrue(unescape(special_byte ^ 0x20) == special_byte)
        with self.assertRaises(ValueError):
            unescape(0x01)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ResponseTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RequestTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(XBeeTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
