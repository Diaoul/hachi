# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .const import FRAME_DELIMITER, ESCAPE, XON, XOFF
from .response import RESPONSE_MAP
import logging

__all__ = ['XBee', 'escape', 'escape_frame', 'unescape']
logger = logging.getLogger(__name__)


class XBee(object):
    """Parser for incoming XBee communications

    The :class:`XBee` parses data through its :meth:`feed` method.
    When a complete and valid response is found, the `response` attribute is set to
    the corresponding :class:`~hachi.response.XBeeResponse` and the callback is called.
    Any malformed response is silently discarded.

    :param function callback: callback method called with a
        :class:`~hachi.response.XBeeResponse` as first positional argument

    """
    def __init__(self, callback=None):
        self.callback = callback
        self.reset()

    def reset(self):
        """Reset the state of the parser"""
        #: Response
        self.response = None
        self.buffer = bytearray()
        self._escape_byte = False

    def feed(self, data):
        """Feed the parser with data

        :param data: byte(s) to add
        :type data: int or bytes or bytearray

        """
        if isinstance(data, str):  # python 2
            for c in data:
                self.feed(ord(c))
            return
        if isinstance(data, (bytearray, bytes)):
            for b in data:
                self.feed(b)
            return
        if data == FRAME_DELIMITER:
            if self.buffer and not self.response:
                logger.warning('New packet start before previous response is complete, discarding previous packet')
            self.reset()
            self.buffer.append(data)
            return
        if not self.buffer:  # don't start the party without our start byte
            logger.debug('Found byte 0x%x while waiting for frame delimiter, discarding byte', data)
            return
        if data == ESCAPE:  # prepare to unescape next byte
            self._escape_byte = True
            return
        if self._escape_byte:  # unescape data
            data = unescape(data)
            self._escape_byte = False

        # append data to the buffer
        self.buffer.append(data)

        # check if frame is complete and valid and try to extract a response from it
        if len(self.buffer) > 4 and len(self.buffer) - 4 == (self.buffer[1] << 8) + self.buffer[2]:
            logger.debug('Frame complete: %s', ' '.join('%02X' % byte for byte in self.buffer))
            # verify the checksum
            if sum(self.buffer[3:]) & 0xff != 0xff:
                logger.warning('Invalid checksum, discarding packet')
                self.reset()
                return
            # get the response
            if self.buffer[3] not in RESPONSE_MAP:
                logger.error('Unknown api id %02x, discarding packet', self.buffer[3])
                self.reset()
                return
            self.response = RESPONSE_MAP[self.buffer[3]](self.buffer)
            if self.callback is not None:
                self.callback(self.response)


def escape(byte):
    """Escape a byte

    :param int byte: the byte to escape
    :raise: ValueError if the byte is not a special byte
    :return: the escaped byte
    :rtype: int

    """
    if byte not in (FRAME_DELIMITER, ESCAPE, XON, XOFF):
        raise ValueError('Not a special byte')
    return byte ^ 0x20


def escape_frame(frame):
    """Escape a frame

    :param bytearray frame: the frame to escape, starting with :data:`~hachi.const.FRAME_DELIMITER`
    :raise: ValueError if the frame does not start with a :data:`~hachi.const.FRAME_DELIMITER`
    :return: the escaped frame
    :rtype: bytearray

    """
    if frame[0] != FRAME_DELIMITER:
        raise ValueError('Frame must start with the frame delimiter')
    escaped_frame = bytearray([FRAME_DELIMITER])
    for byte in frame[1:]:
        if byte in (FRAME_DELIMITER, ESCAPE, XON, XOFF):
            escaped_frame.append(ESCAPE)
            byte = escape(byte)
        escaped_frame.append(byte)
    return escaped_frame


def unescape(byte):
    """Unescape a byte

    :param int byte: the byte to unescape
    :raise: ValueError if the unescaped byte is not a special byte
    :return: the unescaped byte
    :rtype: int

    """
    result = 0x20 ^ byte
    if result not in (FRAME_DELIMITER, ESCAPE, XON, XOFF):
        raise ValueError('Unescape result is not a special byte')
    return  result
