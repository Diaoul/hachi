# -*- coding: utf-8 -*-

# Special bytes
#: Frame delimiter byte
FRAME_DELIMITER = 0x7e

#: Escape byte
ESCAPE = 0x7d

#: XON byte
XON = 0x11

#: XOFF byte
XOFF = 0x13


# API IDs for requests
#: API ID for :class:`~hachi.request.Tx64Request`
TX_64_REQUEST = 0x00

#: API ID for :class:`~hachi.request.Tx16Request`
TX_16_REQUEST = 0x01

#: API ID for :class:`~hachi.request.AtRequest`
AT_REQUEST = 0x08

#: API ID for :class:`~hachi.request.AtQueueRequest`
AT_QUEUE_REQUEST = 0x09

#: API ID for :class:`~hachi.request.ZBTxRequest`
ZB_TX_REQUEST = 0x10

#: API ID for :class:`~hachi.request.ZBExplicitTxRequest`
ZB_EXPLICIT_TX_REQUEST = 0x11

#: API ID for :class:`~hachi.request.RemoteAtRequest`
REMOTE_AT_REQUEST = 0x17


# API IDs for responses
#: API ID for :class:`~hachi.response.Rx64Response`
RX_64_RESPONSE = 0x80

#: API ID for :class:`~hachi.response.Rx16Response`
RX_16_RESPONSE = 0x81

#: API ID for :class:`~hachi.response.Rx64IoSampleResponse`
RX_64_IO_RESPONSE = 0x82

#: API ID for :class:`~hachi.response.Rx16IoSampleResponse`
RX_16_IO_RESPONSE = 0x83

#: API ID for :class:`~hachi.response.AtResponse`
AT_RESPONSE = 0x88

#: API ID for :class:`~hachi.response.TxStatusResponse`
TX_STATUS_RESPONSE = 0x89

#: API ID for :class:`~hachi.response.ModemStatusResponse`
MODEM_STATUS_RESPONSE = 0x8a

#: API ID for :class:`~hachi.response.ZBTxStatusResponse`
ZB_TX_STATUS_RESPONSE = 0x8b

#: API ID for :class:`~hachi.response.ZBRxResponse`
ZB_RX_RESPONSE = 0x90

#: API ID for :class:`~hachi.response.ZBExplicitRxResponse`
ZB_EXPLICIT_RX_RESPONSE = 0x91

#: API ID for :class:`~hachi.response.ZBIoSampleResponse`
ZB_IO_SAMPLE_RESPONSE = 0x92

#: API ID for :class:`~hachi.response.RemoteAtResponse`
REMOTE_AT_RESPONSE = 0x97


# Special frame ids
#: Frame id that disables status responses
FRAME_ID_NO_RESPONSE = 0x00


# Special addresses
#: Use 64-bit addressing 16-bit address. Applies to :class:`~hachi.request.Tx16Request`
ADDRESS_16_USE_64_BIT_ADDRESSING = 0xfffe

#: Broadcast 16-bit address
ADDRESS_16_BROADCAST = 0xffff

#: Coordinator 64-bit address
ADDRESS_64_COORDINATOR = 0x0000000000000000

#: Broadcast 64-bit address
ADDRESS_64_BROADCAST = 0x000000000000ffff

#: Unknown 64-bit address
ADDRESS_64_UNKNOWN = 0xffffffffffffffff


# Special broadcast radius
#: Maximum hops
BROADCAST_RADIUS_MAX_HOPS = 0x00


# Transmit options
#: Disable acknowledgement. Applies to :class:`~hachi.request.Tx64Request` and :class:`~hachi.request.Tx16Request`
TRANSMIT_OPTION_DISABLE_ACKNOWLEDGEMENT = 0x01

#: Send packet with broadcast pan id. Applies to :class:`~hachi.request.Tx64Request` and :class:`~hachi.request.Tx16Request`
TRANSMIT_OPTION_BROADCAST_PACKET = 0x04

#: Apply changes. Applies to :class:`~hachi.request.RemoteAtRequest`
TRANSMIT_OPTION_APPLY_CHANGES = 0x02

#: Disable retries and route repair. Applies to :class:`~hachi.request.ZBTxRequest` and :class:`~hachi.request.ZBExplicitTxRequest`
TRANSMIT_OPTION_DISABLE_RETRIES_AND_ROUTE_REPAIR = 0x01

#: Enable APS encryption. Applies to :class:`~hachi.request.ZBTxRequest` and :class:`~hachi.request.ZBExplicitTxRequest`
TRANSMIT_OPTION_ENABLE_APS_ENCRYPTION = 0x20

#: Use extended transmission timeout. Applies to :class:`~hachi.request.ZBTxRequest` and :class:`~hachi.request.ZBExplicitTxRequest`
TRANSMIT_OPTION_USE_EXTENDED_TRANSMISSION_TIMEOUT = 0x40


# Receive options
#: Address broadcast. Applies to :class:`~hachi.response.Rx64Response` and :class:`~hachi.response.Rx16Response`
RECEIVE_OPTION_ADDRESS_BROADCAST = 0x01

#: PAN broadcast. Applies to :class:`~hachi.response.Rx64Response` and :class:`~hachi.response.Rx16Response`
RECEIVE_OPTION_PAN_BROADCAST = 0x02

#: Packet acknowledged. Applies to :class:`~hachi.response.ZBRxResponse` and :class:`~hachi.response.ZBExplicitRxResponse`
RECEIVE_OPTION_PACKET_ACKNOWLEDGED = 0x01

#: Packet was a broadcast packet. Applies to :class:`~hachi.response.ZBRxResponse` and :class:`~hachi.response.ZBExplicitRxResponse`
RECEIVE_OPTION_PACKET_BROADCAST = 0x02

#: Packet encrypted with APS encryption. Applies to :class:`~hachi.response.ZBRxResponse` and :class:`~hachi.response.ZBExplicitRxResponse`
RECEIVE_OPTION_PACKET_ENCRYPTED_WITH_APS = 0x20

#: Packet was sent from an end device (if known). Applies to :class:`~hachi.response.ZBRxResponse` and :class:`~hachi.response.ZBExplicitRxResponse`
RECEIVE_OPTION_PACKET_FROM_END_DEVICE = 0x40


# Transmit statuses
#: Success. Applies to :class:`~hachi.response.TxStatusResponse` and :class:`~hachi.response.ZBTxStatusResponse`
STATUS_SUCCESS = 0x00

#: MAC ACK failure. Applies to :class:`~hachi.response.TxStatusResponse` and :class:`~hachi.response.ZBTxStatusResponse`
STATUS_MAC_ACK_FAILURE = 0x01

#: CCA failure. Applies to :class:`~hachi.response.TxStatusResponse` and :class:`~hachi.response.ZBTxStatusResponse`
STATUS_CCA_FAILURE = 0x02

#: Purged. Applies to :class:`~hachi.response.TxStatusResponse`
STATUS_PURGED = 0x03

#: Invalid destination endpoint. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_INVALID_DESTINATION_ENDPOINT = 0x15

#: Network ACK failure. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_NETWORK_ACK_FAILURE = 0x21

#: Not joined to network. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_NOT_JOINED_TO_NETWORK = 0x22

#: Self-addressed. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_SELF_ADDRESSED = 0x23

#: Address not found. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_ADDRESS_NOT_FOUND = 0x24

#: Route not found. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_ROUTE_NOT_FOUND = 0x25

#: Broadcast source failed to hear a neighbor relay relay the message. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_NEIGHBOR_FAILURE = 0x26

#: Invalid binding table index. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_INVALID_BINDING_TABLE_INDEX = 0x2b

#: Resource error lack of free buffers, timers, etc. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_RESOURCE_ERROR = 0x2c

#: Attempted broadcast with APS transmission. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_ATTEMPTED_BROADCAST_WITH_APS = 0x2d

#: Attempted unicast with APS transmission but EE=0. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_ATTEMPTED_UNICAST_APS = 0x2e

#: Resource error lack of free buffers, timers, etc. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_RESOURCE_ERROR_2 = 0x32

#: Data payload too large. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_DATA_PAYLOAD_TOO_LARGE = 0x74

#: Indirect message unrequested. Applies to :class:`~hachi.response.ZBTxStatusResponse`
STATUS_INDIRECT_MESSAGE_UNREQUESTED = 0x75


# Discovery statuses
#: No overhead discovery. Applies to :class:`~hachi.response.ZBTxStatusResponse`
DISCOVERY_STATUS_NO_OVERHEAD = 0x00

#: Address discovery. Applies to :class:`~hachi.response.ZBTxStatusResponse`
DISCOVERY_STATUS_ADDRESS = 0x01

#: Route discovery. Applies to :class:`~hachi.response.ZBTxStatusResponse`
DISCOVERY_STATUS_ROUTE = 0x02

#: Address and route discovery. Applies to :class:`~hachi.response.ZBTxStatusResponse`
DISCOVERY_STATUS_ADDRESS_AND_ROUTE = 0x03

#: Extended timeout discovery. Applies to :class:`~hachi.response.ZBTxStatusResponse`
DISCOVERY_STATUS_EXTENDED_TIMEOUT = 0x40


# Command statuses
#: OK. Applies to :class:`~hachi.response.AtResponse` and :class:`~hachi.response.RemoteAtResponse`
COMMAND_STATUS_OK = 0x00

#: Error. Applies to :class:`~hachi.response.AtResponse` and :class:`~hachi.response.RemoteAtResponse`
COMMAND_STATUS_ERROR = 0x01

#: Invalid command. Applies to :class:`~hachi.response.AtResponse` and :class:`~hachi.response.RemoteAtResponse`
COMMAND_STATUS_INVALID_COMMAND = 0x02

#: Invalid parameter. Applies to :class:`~hachi.response.AtResponse` and :class:`~hachi.response.RemoteAtResponse`
COMMAND_STATUS_INVALID_PARAMETER = 0x03

#: No response. Applies to :class:`~hachi.response.RemoteAtResponse`
COMMAND_STATUS_NO_RESPONSE = 0x04


# Modem statuses
#: Hardware reset
MODEM_STATUS_HARDWARE_RESET = 0x00

#: Watchdog timer reset
MODEM_STATUS_WATCHDOG_TIMER_RESET = 0x01

#: Associated
MODEM_STATUS_ASSOCIATED = 0x02

#: Disassociated
MODEM_STATUS_DISASSOCIATED = 0x03

#: Synchronization lost
MODEM_STATUS_SYNCHRONIZATION_LOST = 0x04

#: Coordinator realignment
MODEM_STATUS_COORDINATOR_REALIGNMENT = 0x05

#: Coordinator started
MODEM_STATUS_COORDINATOR_STARTED = 0x06

#: Network security key updated
MODEM_STATUS_NETWORK_SECURITY_KEY_UPDATED = 0x07

#: Voltage supply limit exceeded
MODEM_STATUS_VOLTAGE_SUPPLY_LIMIT_EXCEEDED = 0x0d

#: Modem configuration changed while join in progress
MODEM_STATUS_MODEM_CONFIGURATION_CHANGED_WHILE_JOINING = 0x11

#: Stack error minimum
MODEM_STATUS_STACK_ERROR_MIN = 0x80
