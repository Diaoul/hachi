# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .compat import unpack
from .const import (RX_64_RESPONSE, RX_16_RESPONSE, RX_64_IO_RESPONSE,
    RX_16_IO_RESPONSE, AT_RESPONSE, TX_STATUS_RESPONSE, MODEM_STATUS_RESPONSE,
    ZB_TX_STATUS_RESPONSE, ZB_RX_RESPONSE, ZB_EXPLICIT_RX_RESPONSE,
    ZB_IO_SAMPLE_RESPONSE, REMOTE_AT_RESPONSE)

__all__ = ['XBeeResponse', 'Rx64Response', 'Rx16Response', 'Rx64IoSampleResponse', 'Rx16IoSampleResponse',
           'AtResponse', 'TxStatusResponse', 'ModemStatusResponse', 'ZBTxStatusResponse',
           'ZBRxResponse', 'ZBExplicitRxResponse', 'ZBIoSampleResponse', 'RemoteAtResponse',
           'RESPONSE_MAP', 'bitcount']


class XBeeResponse(object):
    """Base class for all XBee responses

    The :class:`XBeeResponse` is a wrapper around the underlying raw API frame.

    :param bytearray frame: unescaped raw API frame

    """
    api_id = None
    """API ID

    Subclasses must implement this and return the corresponding API ID

    """
    def __init__(self, frame):
        if frame[3] != self.api_id:
            raise ValueError('Frame with wrong API ID')
        #: Unescaped raw API frame
        self.frame = frame

    @property
    def length(self):
        """Length, on 2 bytes starting right after the :data:`~hachi.const.FRAME_DELIMITER` of the :attr:`frame`"""
        return unpack('>H', self.frame[1:3])[0]

    @property
    def id_data(self):
        """API ID-specific raw data, bytes between the :attr:`api_id` and the :attr:`checksum`

        Subclasses may provide properties to access API ID-specific data

        """
        return self.frame[4:-1]

    @property
    def checksum(self):
        """Checksum, last byte of the :attr:`frame`"""
        return self.frame[-1]

    def verify(self):
        """Check if the response has a valid :attr:`checksum`

        :return: `True` if the response has a valid :attr:`checksum`, `False` otherwise
        :rtype: bool

        """
        return sum(self.frame[3:]) & 0xff == 0xff

    def __len__(self):
        return self.length

    def __repr__(self):
        return '<%s(len=%d)>' % (self.__class__.__name__, self.length)


class Rx64Response(XBeeResponse):
    """Response to a :class:`~hachi.request.Tx64Request`

    Frame example: 7E 00 10 80 00 13 A2 00 40 52 2B AA 16 03 F1 2E AA BD C9 FB

    """
    api_id = RX_64_RESPONSE

    @property
    def source_address(self):
        """Source address, first 8 bytes of the :attr:`~XBeeResponse.id_data`"""
        return unpack('>Q', self.id_data[0:8])[0]

    @property
    def rssi(self):
        """RSSI, immediatly following the :attr:`source_address`"""
        return self.id_data[8]

    @property
    def options(self):
        """Options, immediatly following the :attr:`rssi`"""
        return self.id_data[9]

    @property
    def data(self):
        """Data, all bytes following the :attr:`options` until the end of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[10:]


class Rx16Response(XBeeResponse):
    """Response to a :class:`~hachi.request.Tx16Request`

    Frame example: 7E 00 0A 81 52 1A 23 01 12 33 85 A1 F2 91'

    """
    api_id = RX_16_RESPONSE

    @property
    def source_address(self):
        """Source address, first 2 bytes of the :attr:`~XBeeResponse.id_data`"""
        return unpack('>H', self.id_data[0:2])[0]

    @property
    def rssi(self):
        """RSSI, immediatly following the :attr:`source_address`"""
        return self.id_data[2]

    @property
    def options(self):
        """Options, immediatly following the :attr:`rssi`"""
        return self.id_data[3]

    @property
    def data(self):
        """Data, all bytes following the :attr:`options` until the end of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[4:]


class Rx64IoSampleResponse(XBeeResponse):
    """IO sample response using 64-bits addressing

    Frame example: 7E 00 14 82 00 13 A2 00 40 52 2B AA 23 01 02 14 88 00 80 00 8F 03 ED 00 08 02 4C 00 0C 3E

    """
    api_id = RX_64_IO_RESPONSE

    @property
    def source_address(self):
        """Source address, first 8 bytes of the :attr:`~XBeeResponse.id_data`"""
        return unpack('>Q', self.id_data[0:8])[0]

    @property
    def rssi(self):
        """RSSI, immediatly following the :attr:`source_address`"""
        return self.id_data[8]

    @property
    def options(self):
        """Options, immediatly following the :attr:`rssi`"""
        return self.id_data[9]

    @property
    def sample_count(self):
        """Sample count, immediatly following the :attr:`options`"""
        return self.id_data[10]

    @property
    def analog_mask(self):
        """Analog mask, immediatly following the :attr:`sample_count`

        It is the whole byte of which first and last bit are set to 0 because
        useless in this context. Second bit (right to left) tells if analog
        channel 0 (A0) is enabled (bit to 1) or disabled (bit to 0), third bit is
        for A1 and so on until seventh bit which is for A5

        """
        return self.id_data[11] & 0x3e

    @property
    def digital_mask(self):
        """Digital mask, on 2 bytes including the :attr:`analog_mask` byte

        It is the whole first byte (right to left) and the second one of which all
        bits except the first one are set to 0 because useless in this context. First
        bit (right to left) tells if digital channel 0 (D0) is enabled (bit to 1) or
        disabled (bit to 0), second bit is for D1 and so on until ninth bit which is
        for D8

        """
        return unpack('>H', self.id_data[11:13])[0] & 0x01ff

    @property
    def contains_analog(self):
        """`True` if at least one analog channel is enabled, `False` otherwise"""
        return self.analog_mask > 0

    @property
    def contains_digital(self):
        """`True` if at least one digital channel is enabled, `False` otherwise"""
        return self.digital_mask > 0

    def is_analog_enabled(self, pin):
        """Tells if a given analog pin is enabled or not

        :param int pin: analog pin number
        :return: `True` if the given analog pin is enabled, `False` otherwise
        :rtype: boolean

        """
        return (self.analog_mask >> pin + 1) & 1 == 1

    def is_digital_enabled(self, pin):
        """Tells if a given digital pin is enabled or not

        :param int pin: digital pin number
        :return: `True` if the given digital pin is enabled, `False` otherwise
        :rtype: boolean

        """
        return (self.digital_mask >> pin) & 1 == 1

    def is_digital_on(self, index, pin):
        """Tells if a given digital pin is on or not in a sample

        :param int index: index of the sample
        :param int pin: digital pin number
        :return: `True` if the given digital pin is on in the sample, `False` otherwise
        :rtype: boolean

        """
        if not self.is_digital_enabled(pin):
            raise ValueError('Digital pin %d is not enabled' % pin)
        offset = index * 2
        if self.contains_analog:
            offset += index * 2 * bitcount(self.analog_mask)
        sample = unpack('>H', self.id_data[13 + offset:15 + offset])[0]
        return (sample >> pin) & 1 == 1

    def get_analog(self, index, pin):
        """Gives the analog value of a pin in a sample

        :param int index: index of the sample
        :param int pin: analog pin number
        :return: analog pin value
        :rtype: int

        """
        if not self.is_analog_enabled(pin):
            raise ValueError('Analog pin %d is not enabled' % pin)
        offset = index * 2 * bitcount(self.analog_mask)
        if self.contains_digital:
            offset += 2 + index * 2
        for i in range(pin):
            if self.is_analog_enabled(i):
                offset += 2
        return unpack('>H', self.id_data[13 + offset:15 + offset])[0]


class Rx16IoSampleResponse(XBeeResponse):
    """IO sample response using 16-bits addressing

    Frame example: 7E 00 14 83 7D 84 23 01 02 14 88 00 80 00 8F 03 ED 00 08 02 4C 00 0C 58

    """
    api_id = RX_16_IO_RESPONSE

    @property
    def source_address(self):
        """Source address, first 2 bytes of the :attr:`~XBeeResponse.id_data`"""
        return unpack('>H', self.id_data[0:2])[0]

    @property
    def rssi(self):
        """RSSI, immediatly following the :attr:`source_address`"""
        return self.id_data[2]

    @property
    def options(self):
        """Options, immediatly following the :attr:`rssi`"""
        return self.id_data[3]

    @property
    def sample_count(self):
        """Sample count, immediatly following the :attr:`options`"""
        return self.id_data[4]

    @property
    def analog_mask(self):
        """Analog mask, immediatly following the :attr:`sample_count`

        It is the whole byte of which first and last bit are set to 0 because
        useless in this context. Second bit (right to left) tells if analog
        channel 0 (A0) is enabled (bit to 1) or disabled (bit to 0), third bit is
        for A1 and so on until seventh bit which is for A5

        """
        return self.id_data[5] & 0x3e

    @property
    def digital_mask(self):
        """Digital mask, on 2 bytes including the :attr:`analog_mask` byte

        It is the whole first byte (right to left) and the second one of which all
        bits except the first one are set to 0 because useless in this context. First
        bit (right to left) tells if digital channel 0 (D0) is enabled (bit to 1) or
        disabled (bit to 0), second bit is for D1 and so on until ninth bit which is
        for D8

        """
        return unpack('>H', self.id_data[5:7])[0] & 0x01ff

    @property
    def contains_analog(self):
        """`True` if at least one analog channel is enabled, `False` otherwise"""
        return self.analog_mask > 0

    @property
    def contains_digital(self):
        """`True` if at least one digital channel is enabled, `False` otherwise"""
        return self.digital_mask > 0

    def is_analog_enabled(self, pin):
        """Tells if a given analog pin is enabled or not

        :param int pin: analog pin number
        :return: `True` if the given analog pin is enabled, `False` otherwise
        :rtype: boolean

        """
        return (self.analog_mask >> pin + 1) & 1 == 1

    def is_digital_enabled(self, pin):
        """Tells if a given digital pin is enabled or not

        :param int pin: digital pin number
        :return: `True` if the given digital pin is enabled, `False` otherwise
        :rtype: boolean

        """
        return (self.digital_mask >> pin) & 1 == 1

    def is_digital_on(self, index, pin):
        """Tells if a given digital pin is on or not in a sample

        :param int index: index of the sample
        :param int pin: digital pin number
        :return: `True` if the given digital pin is on in the sample, `False` otherwise
        :rtype: boolean

        """
        if not self.is_digital_enabled(pin):
            raise ValueError('Digital pin %d is not enabled' % pin)
        offset = index * 2
        if self.contains_analog:
            offset += index * 2 * bitcount(self.analog_mask)
        sample = unpack('>H', self.id_data[7 + offset:9 + offset])[0]
        return (sample >> pin) & 1 == 1

    def get_analog(self, index, pin):
        """Gives the analog value of a pin in a sample

        :param int index: index of the sample
        :param int pin: analog pin number
        :return: analog pin value
        :rtype: int

        """
        if not self.is_analog_enabled(pin):
            raise ValueError('Analog pin %d is not enabled' % pin)
        offset = index * 2 * bitcount(self.analog_mask)
        if self.contains_digital:
            offset += 2 + index * 2
        for i in range(pin):
            if self.is_analog_enabled(i):
                offset += 2
        return unpack('>H', self.id_data[7 + offset:9 + offset])[0]


class AtResponse(XBeeResponse):
    """Response to a :class:`~hachi.request.AtRequest`

    Frame example: 7E 00 07 88 52 4D 59 00 00 00 7F

    """
    api_id = AT_RESPONSE

    @property
    def frame_id(self):
        """Frame Id, first byte of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[0]

    @property
    def command(self):
        """Command, on 2 bytes immediately following the :attr:`frame_id`"""
        return bytes(self.id_data[1:3])

    @property
    def status(self):
        """Status, immediately following the :attr:`command`"""
        return self.id_data[3]

    @property
    def value(self):
        """Value, all bytes following the :attr:`status` until the end of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[4:]


class TxStatusResponse(XBeeResponse):
    """Status response emitted by the module after a :class:`~hachi.request.Tx64Request` or a :class:`~hachi.request.Tx16Request`

    Frame example: 7E 00 03 89 2A 74 D8

    """
    api_id = TX_STATUS_RESPONSE

    @property
    def frame_id(self):
        """Frame Id, first byte of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[0]

    @property
    def status(self):
        """Status, immediately following the :attr:`frame_id`"""
        return self.id_data[1]


class ModemStatusResponse(XBeeResponse):
    """Modem status response

    Frame example: 7E 00 02 8A 06 6F

    """
    api_id = MODEM_STATUS_RESPONSE

    @property
    def status(self):
        """Status, first byte of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[0]


class ZBTxStatusResponse(XBeeResponse):
    """Status response emitted by the module after a :class:`~hachi.request.ZBTxRequest` or a :class:`~hachi.request.ZBExplicitTxRequest`

    Frame example: 7E 00 07 8B 01 7D 84 00 00 01 71

    """
    api_id = ZB_TX_STATUS_RESPONSE

    @property
    def frame_id(self):
        """Frame Id, first byte of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[0]

    @property
    def destination_address(self):
        """Destination address, on 2 bytes immediately following the :attr:`frame_id`"""
        return unpack('>H', self.id_data[1:3])[0]

    @property
    def retry_count(self):
        """Retry count, immediately following the :attr:`destination_address`"""
        return self.id_data[3]

    @property
    def delivery_status(self):
        """Delivery status, immediately following the :attr:`retry_count`"""
        return self.id_data[4]

    @property
    def discovery_status(self):
        """Discovery status, immediately following the :attr:`delivery_status`"""
        return self.id_data[5]


class ZBRxResponse(XBeeResponse):
    """Response to a :class:`~hachi.request.ZBTxRequest`

    Frame example: 7E 00 12 90 00 13 A2 00 40 52 2B AA 7D 84 01 52 78 44 61 74 61 0D

    """
    api_id = ZB_RX_RESPONSE

    @property
    def source_address_64(self):
        """64-bits source address, first 8 bytes of the :attr:`~XBeeResponse.id_data`"""
        return unpack('>Q', self.id_data[0:8])[0]

    @property
    def source_address_16(self):
        """16-bits source address, on 2 bytes immediately following the :attr:`source_address_64`"""
        return unpack('>H', self.id_data[8:10])[0]

    @property
    def options(self):
        """Options, immediately following the :attr:`source_address_16`"""
        return self.id_data[10]

    @property
    def data(self):
        """Data, all bytes following the :attr:`options` until the end of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[11:]


class ZBExplicitRxResponse(XBeeResponse):
    """Response to a :class:`~hachi.request.ZBExplicitTxRequest`

    Frame example: 7E 00 18 91 00 13 A2 00 40 52 2B AA 7D 84 E0 E0 22 11 C1 05 02 52 78 44 61 74 61 52

    """
    api_id = ZB_EXPLICIT_RX_RESPONSE

    @property
    def source_address_64(self):
        """64-bits source address, first 8 bytes of the :attr:`~XBeeResponse.id_data`"""
        return unpack('>Q', self.id_data[0:8])[0]

    @property
    def source_address_16(self):
        """16-bits source address, on 2 bytes immediately following the :attr:`source_address_64`"""
        return unpack('>H', self.id_data[8:10])[0]

    @property
    def source_endpoint(self):
        """Source endpoint, immediately following the :attr:`source_address_16`"""
        return self.id_data[10]

    @property
    def destination_endpoint(self):
        """Destination endpoint, immediately following the :attr:`source_endpoint`"""
        return self.id_data[11]

    @property
    def cluster_id(self):
        """Cluster id, on 2 bytes immediately following the :attr:`destination_endpoint`"""
        return unpack('>H', self.id_data[12:14])[0]

    @property
    def profile_id(self):
        """Profile id, on 2 bytes immediately following the :attr:`cluster_id`"""
        return unpack('>H', self.id_data[14:16])[0]

    @property
    def options(self):
        """Options, immediately following the :attr:`profile_id`"""
        return self.id_data[16]

    @property
    def data(self):
        """Data, all bytes following the :attr:`options` until the end of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[17:]


class ZBIoSampleResponse(XBeeResponse):
    """IO sample response

    Frame example: 7E 00 14 92 00 13 A2 00 40 52 2B AA 7D 84 01 01 00 1C 02 00 14 02 25 F5

    """
    api_id = ZB_IO_SAMPLE_RESPONSE

    @property
    def source_address_64(self):
        """64-bits source address, first 8 bytes of the :attr:`~XBeeResponse.id_data`"""
        return unpack('>Q', self.id_data[0:8])[0]

    @property
    def source_address_16(self):
        """16-bits source address, on 2 bytes immediately following the :attr:`source_address_64`"""
        return unpack('>H', self.id_data[8:10])[0]

    @property
    def options(self):
        """Options, immediately following the :attr:`source_address_16`"""
        return self.id_data[10]

    @property
    def sample_count(self):
        """Sample count, immediately following the :attr:`options`"""
        return self.id_data[11]

    @property
    def digital_mask(self):
        """Digital mask, on 2 bytes, immediately following the :attr:`sample_count`"""
        return unpack('>H', self.id_data[12:14])[0] & 0x3cff

    @property
    def analog_mask(self):
        """Analog mask, immediately following the :attr:`digital_mask`"""
        return self.id_data[14] & 0x8f

    @property
    def contains_digital(self):
        """`True` if at least one digital channel is enabled, `False` otherwise"""
        return self.digital_mask > 0

    @property
    def contains_analog(self):
        """`True` if at least one analog channel is enabled, `False` otherwise"""
        return self.analog_mask > 0

    def is_digital_enabled(self, pin):
        """Tells if a given digital pin is enabled or not

        :param int pin: digital pin number
        :return: `True` if the given digital pin is enabled, `False` otherwise
        :rtype: boolean

        """
        return (self.digital_mask >> pin) & 1 == 1

    def is_analog_enabled(self, pin):
        """Tells if a given analog pin is enabled or not

        :param int pin: analog pin number
        :return: `True` if the given analog pin is enabled, `False` otherwise
        :rtype: boolean

        """
        return (self.analog_mask >> pin) & 1 == 1

    def is_digital_on(self, pin):
        """Tells if a given digital pin is on or not

        :param int pin: digital pin number
        :return: `True` if the given digital pin is on, `False` otherwise
        :rtype: boolean

        """
        if not self.is_digital_enabled(pin):
            raise ValueError('Digital pin %d is not enabled' % pin)
        sample = unpack('>H', self.id_data[15:17])[0]
        return (sample >> pin) & 1 == 1

    def get_analog(self, pin):
        """Gives the analog value of a pin

        :param int pin: analog pin number
        :return: analog pin value
        :rtype: int

        """
        if not self.is_analog_enabled(pin):
            raise ValueError('Analog pin %d is not enabled' % pin)
        offset = 0
        if self.contains_digital:
            offset += 2
        for i in range(pin):
            if self.is_analog_enabled(i):
                offset += 2
        return unpack('>H', self.id_data[15 + offset:17 + offset])[0]


class RemoteAtResponse(XBeeResponse):
    """Response to a :class:`~hachi.request.RemoteAtRequest`

    Frame example: 7E 00 13 97 55 00 13 A2 00 40 52 2B AA 7D 84 53 4C 00 40 52 2B AA F0

    """
    api_id = REMOTE_AT_RESPONSE

    @property
    def frame_id(self):
        """Frame Id, first byte of the :attr:`~XBeeResponse.id_data`"""
        return self.id_data[0]

    @property
    def source_address_64(self):
        """64-bits source address, on 8 bytes immediately following the :attr:`frame_id`"""
        return unpack('>Q', self.id_data[1:9])[0]

    @property
    def source_address_16(self):
        """16-bits source address, on 2 bytes immediately following the :attr:`source_address_64`"""
        return unpack('>H', self.id_data[9:11])[0]

    @property
    def command(self):
        """Command, on two bytes immediately following the :attr:`source_address_16`"""
        return bytes(self.id_data[11:13])

    @property
    def status(self):
        """Status, immediately following the :attr:`command`"""
        return self.id_data[13]

    @property
    def data(self):
        """Data, all bytes following the :attr:`status` until the end of the :attr:`~XBeeResponse.id_data` if any
        `None` otherwise

        """
        if len(self) < 16:
            return None
        return self.id_data[14:]

RESPONSE_MAP = {c.api_id: c for c in (Rx64Response, Rx16Response, Rx64IoSampleResponse, Rx16IoSampleResponse, AtResponse,
                                      TxStatusResponse, ModemStatusResponse, ZBTxStatusResponse, ZBRxResponse, ZBExplicitRxResponse,
                                      ZBIoSampleResponse, RemoteAtResponse)}


def bitcount(number):
    """Count the number of bits to 1 in a number

    For example::

        >>> bitcount(0b10110010)
        4
        >>> bitcount(0b0100)
        1

    :param int number: number on which to count the positive bits
    :return: the number of positive bits
    :rtype: int

    """
    count = 0
    while number:
        count += number & 1
        number >>= 1
    return count
