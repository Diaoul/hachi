# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .core import XBee
from twisted.internet.protocol import Protocol


__all__ = ['XBeeProtocol']


class XBeeProtocol(XBee, Protocol):
    """:class:`~hachi.core.XBee` parser twisted implementation"""
    def __init__(self):
        super(XBeeProtocol, self).__init__(self.responseReceived)

    def dataReceived(self, data):
        self.feed(data)

    def responseReceived(self, response):
        """Callback called whenever a :class:`~hachi.response.XBeeResponse` is received

        Subclasses must implement this

        :param response: the received response
        :type response: :class:`~hachi.response.XBeeResponse`

        """
        raise NotImplementedError
