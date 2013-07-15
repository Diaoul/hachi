# -*- coding: utf-8 -*-
from .const import (FRAME_DELIMITER, TRANSMIT_OPTION_APPLY_CHANGES, TX_64_REQUEST,
    TX_16_REQUEST, AT_REQUEST, AT_QUEUE_REQUEST, ZB_TX_REQUEST,
    ZB_EXPLICIT_TX_REQUEST, REMOTE_AT_REQUEST)
import struct
from hachi.const import ADDRESS_64_COORDINATOR, ADDRESS_16_USE_64_BIT_ADDRESSING,\
    BROADCAST_RADIUS_MAX_HOPS

__all__ = ['XBeeRequest', 'Tx64Request', 'Tx16Request', 'AtRequest', 'AtQueueRequest',
           'ZBTxRequest', 'ZBExplicitTxRequest', 'RemoteAtRequest', 'REQUEST_MAP']


#: Frame id used by default. It is non-zero to trigger a status response
FRAME_ID_DEFAULT = 0x01

#: Transmit option used by default.
TRANSMIT_OPTION_DEFAULT = 0x00


class XBeeRequest(object):
    """Base class for all XBee requests

    The :class:`XBeeRequest` provides helpers to access to the raw API frame.
    Unless specified, the type of attributes is :class:`int`.

    """
    api_id = None
    """API ID

    Subclasses must implement this and return the corresponding API ID

    """

    @property
    def length(self):
        """Computed length"""
        return 1 + len(self.id_data)

    @property
    def id_data(self):
        """API ID-specific raw data, bytes between the :attr:`api_id` and the :attr:`checksum`

        Subclasses must implement this

        :type: bytearray
        """
        raise NotImplementedError

    @property
    def checksum(self):
        """Computed checksum"""
        return 0xff ^ (self.api_id + sum(self.id_data)) & 0xff

    @property
    def frame(self):
        """Computed frame"""
        frame = bytearray()
        frame.append(FRAME_DELIMITER)
        frame.append((self.length >> 8) & 0xff)
        frame.append(self.length & 0xff)
        frame.append(self.api_id)
        frame.extend(self.id_data)
        frame.append(self.checksum)
        return frame

    def __len__(self):
        return self.length

    def __repr__(self):
        return '<%s(len=%d)>' % (self.__class__.__name__, self.length)


class Tx64Request(XBeeRequest):
    """Tx Request using 64-bit addressing"""
    api_id = TX_64_REQUEST

    def __init__(self, data, destination_address=ADDRESS_64_COORDINATOR, options=TRANSMIT_OPTION_DEFAULT, frame_id=FRAME_ID_DEFAULT):
        #: Frame id
        self.frame_id = frame_id

        #: 64-bit destination address
        self.destination_address = destination_address

        #: Options
        self.options = options

        self.data = data
        """Data

        :type: bytearray or bytes

        """

    @property
    def id_data(self):
        api_data = bytearray()
        api_data.append(self.frame_id)
        api_data.extend(struct.pack('>Q', self.destination_address))
        api_data.append(self.options)
        api_data.extend(self.data)
        return api_data


class Tx16Request(XBeeRequest):
    """Tx Request using 16-bit addressing"""
    api_id = TX_16_REQUEST

    def __init__(self, data, destination_address, options=TRANSMIT_OPTION_DEFAULT, frame_id=FRAME_ID_DEFAULT):
        #: Frame id
        self.frame_id = frame_id

        #: 16-bit destination address
        self.destination_address = destination_address

        #: Options
        self.options = options

        self.data = data
        """Data

        :type: bytearray or bytes

        """

    @property
    def id_data(self):
        api_data = bytearray()
        api_data.append(self.frame_id)
        api_data.extend(struct.pack('>H', self.destination_address))
        api_data.append(self.options)
        api_data.extend(self.data)
        return api_data


class AtRequest(XBeeRequest):
    """At Request"""
    api_id = AT_REQUEST

    def __init__(self, command, parameter=None, frame_id=FRAME_ID_DEFAULT):
        #: Frame id
        self.frame_id = frame_id

        self.command = command
        """Command

        :type: str

        """

        self.parameter = parameter
        """Parameter value

        Set to `None` to query the register

        :type: None or bytearray or bytes

        """

    @property
    def id_data(self):
        api_data = bytearray()
        api_data.append(self.frame_id)
        api_data.extend(self.command)
        if self.parameter is not None:
            api_data.extend(self.parameter)
        return api_data


class AtQueueRequest(XBeeRequest):
    """At Queue Request"""
    api_id = AT_QUEUE_REQUEST

    def __init__(self, command, parameter=None, frame_id=FRAME_ID_DEFAULT):
        #: Frame id
        self.frame_id = frame_id

        self.command = command
        """Command

        :type: str

        """

        self.parameter = parameter
        """Parameter value

        Set to `None` to query the register

        :type: None or bytearray or bytes

        """

    @property
    def id_data(self):
        api_data = bytearray()
        api_data.append(self.frame_id)
        api_data.extend(self.command)
        if self.parameter is not None:
            api_data.extend(self.parameter)
        return api_data


class ZBTxRequest(XBeeRequest):
    """ZB Tx Request"""
    def __init__(self, data, destination_address_64=ADDRESS_64_COORDINATOR, destination_address_16=ADDRESS_16_USE_64_BIT_ADDRESSING,
                 broadcast_radius=BROADCAST_RADIUS_MAX_HOPS, options=TRANSMIT_OPTION_DEFAULT, frame_id=FRAME_ID_DEFAULT):
        #: Frame id
        self.frame_id = frame_id

        #: 64-bit destination address
        self.destination_address_64 = destination_address_64

        #: 16-bit destination address
        self.destination_address_16 = destination_address_16

        #: Broadcast radius
        self.broadcast_radius = broadcast_radius

        #: Options
        self.options = options

        self.data = data
        """Data

        :type: bytearray or bytes

        """

    @property
    def api_id(self):
        return ZB_TX_REQUEST

    @property
    def id_data(self):
        api_data = bytearray()
        api_data.append(self.frame_id)
        api_data.extend(struct.pack('>Q', self.destination_address_64))
        api_data.extend(struct.pack('>H', self.destination_address_16))
        api_data.append(self.broadcast_radius)
        api_data.append(self.options)
        api_data.extend(self.data)
        return api_data


class ZBExplicitTxRequest(XBeeRequest):
    """ZB Explicit Tx Request"""
    api_id = ZB_EXPLICIT_TX_REQUEST

    def __init__(self, data, destination_address_64, source_endpoint, destination_endpoint, cluster_id, profile_id,
                 destination_address_16=ADDRESS_16_USE_64_BIT_ADDRESSING, broadcast_radius=BROADCAST_RADIUS_MAX_HOPS,
                 options=TRANSMIT_OPTION_DEFAULT, frame_id=FRAME_ID_DEFAULT):
        #: Frame id
        self.frame_id = frame_id

        #: 64-bit destination address
        self.destination_address_64 = destination_address_64

        #: 16-bit destination address
        self.destination_address_16 = destination_address_16

        #: Source endpoint
        self.source_endpoint = source_endpoint

        #: Destination endpoint
        self.destination_endpoint = destination_endpoint

        #: Cluster id
        self.cluster_id = cluster_id

        #: Profile id
        self.profile_id = profile_id

        #: Broadcast radius
        self.broadcast_radius = broadcast_radius

        #: Options
        self.options = options

        self.data = data
        """Data

        :type: bytearray or bytes

        """

    @property
    def id_data(self):
        api_data = bytearray()
        api_data.append(self.frame_id)
        api_data.extend(struct.pack('>Q', self.destination_address_64))
        api_data.extend(struct.pack('>H', self.destination_address_16))
        api_data.append(self.source_endpoint)
        api_data.append(self.destination_endpoint)
        api_data.extend(struct.pack('>H', self.cluster_id))
        api_data.extend(struct.pack('>H', self.profile_id))
        api_data.append(self.broadcast_radius)
        api_data.append(self.options)
        api_data.extend(self.data)
        return api_data


class RemoteAtRequest(XBeeRequest):
    """Remote At Request"""
    api_id = REMOTE_AT_REQUEST

    def __init__(self, command, destination_address_64, parameter=None, destination_address_16=ADDRESS_16_USE_64_BIT_ADDRESSING,
                 options=TRANSMIT_OPTION_APPLY_CHANGES, frame_id=FRAME_ID_DEFAULT):
        #: Frame id
        self.frame_id = frame_id

        #: 64-bit destination address
        self.destination_address_64 = destination_address_64

        #: 16-bit destination address
        self.destination_address_16 = destination_address_16

        #: Options
        self.options = options

        self.command = command
        """Command

        :type: str

        """

        self.parameter = parameter
        """Parameter value

        Set to `None` to query the register

        :type: None or bytearray or bytes

        """

    @property
    def id_data(self):
        api_data = bytearray()
        api_data.append(self.frame_id)
        api_data.extend(struct.pack('>Q', self.destination_address_64))
        api_data.extend(struct.pack('>H', self.destination_address_16))
        api_data.append(self.options)
        api_data.extend(self.command)
        if self.parameter is not None:
            api_data.extend(self.parameter)
        return api_data

REQUEST_MAP = {c.api_id: c for c in (Tx64Request, Tx16Request, AtRequest, AtQueueRequest, ZBTxRequest, ZBExplicitTxRequest, RemoteAtRequest)}
