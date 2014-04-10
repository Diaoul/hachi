# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .core import XBee, escape_frame
from .exceptions import Timeout
from serial import Serial


__all__ = ['XBeeSerial']


class XBeeSerial(XBee):
    """:class:`~hachi.core.XBee` parser serial implementation with pySerial

    .. _pySerial's documentation: http://pyserial.sourceforge.net/

    :param port: serial port name or number. See `pySerial's documentation`_ for more details
    :type port: str or int
    :param int baudrate: serial baudrate. See `pySerial's documentation`_ for more details

    """
    def __init__(self, port, baudrate=9600):
        super(XBeeSerial, self).__init__()
        self.serial = Serial(port, baudrate)

    def read_response(self, timeout=None):
        """Read response from serial

        :param timeout: timeout in seconds. See `pySerial's documentation`_ for more details
        :type timeout: None or int or float
        :raise: :class:`~hachi.exceptions.Timeout` when timeout is exceeded


        """
        self.reset()
        self.serial.timeout = timeout
        while self.response is None:
            char = self.serial.read()
            if not char:
                raise Timeout
            self.feed(ord(char))
        return self.response

    def send(self, request):
        """Send a :class:`~hachi.request.XBeeRequest` through serial

        :param request: the request to send
        :type request: :class:`~hachi.request.XBeeRequest`

        """
        self.serial.write(escape_frame(request.frame))

    def close(self):
        """Close the serial port"""
        self.serial.close()
