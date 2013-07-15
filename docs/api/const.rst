Constants
=========
.. module:: hachi.const

Special bytes
-------------
.. autodata:: FRAME_DELIMITER
.. autodata:: ESCAPE
.. autodata:: XON
.. autodata:: XOFF


API IDs
-------
.. _request_api_ids:

Request API IDs
~~~~~~~~~~~~~~~
.. autodata:: TX_64_REQUEST
.. autodata:: TX_16_REQUEST
.. autodata:: AT_REQUEST
.. autodata:: AT_QUEUE_REQUEST
.. autodata:: ZB_TX_REQUEST
.. autodata:: ZB_EXPLICIT_TX_REQUEST
.. autodata:: REMOTE_AT_REQUEST

.. _response_api_ids:

Response API IDs
~~~~~~~~~~~~~~~~
.. autodata:: RX_64_RESPONSE
.. autodata:: RX_16_RESPONSE
.. autodata:: RX_64_IO_RESPONSE
.. autodata:: RX_16_IO_RESPONSE
.. autodata:: AT_RESPONSE
.. autodata:: TX_STATUS_RESPONSE
.. autodata:: MODEM_STATUS_RESPONSE
.. autodata:: ZB_TX_STATUS_RESPONSE
.. autodata:: ZB_RX_RESPONSE
.. autodata:: ZB_EXPLICIT_RX_RESPONSE
.. autodata:: ZB_IO_SAMPLE_RESPONSE
.. autodata:: REMOTE_AT_RESPONSE


Special frame ids
-----------------
.. autodata:: FRAME_ID_NO_RESPONSE


Special addresses
-----------------
.. autodata:: ADDRESS_16_USE_64_BIT_ADDRESSING
.. autodata:: ADDRESS_16_BROADCAST
.. autodata:: ADDRESS_64_COORDINATOR
.. autodata:: ADDRESS_64_BROADCAST
.. autodata:: ADDRESS_64_UNKNOWN


Special broadcast radius
------------------------
.. autodata:: BROADCAST_RADIUS_MAX_HOPS


Transmit options
----------------
.. autodata:: TRANSMIT_OPTION_DISABLE_ACKNOWLEDGEMENT
.. autodata:: TRANSMIT_OPTION_BROADCAST_PACKET
.. autodata:: TRANSMIT_OPTION_APPLY_CHANGES
.. autodata:: TRANSMIT_OPTION_DISABLE_RETRIES_AND_ROUTE_REPAIR
.. autodata:: TRANSMIT_OPTION_ENABLE_APS_ENCRYPTION
.. autodata:: TRANSMIT_OPTION_USE_EXTENDED_TRANSMISSION_TIMEOUT


Receive options
---------------
.. autodata:: RECEIVE_OPTION_ADDRESS_BROADCAST

.. autodata:: RECEIVE_OPTION_PAN_BROADCAST
.. autodata:: RECEIVE_OPTION_PACKET_ACKNOWLEDGED
.. autodata:: RECEIVE_OPTION_PACKET_BROADCAST
.. autodata:: RECEIVE_OPTION_PACKET_ENCRYPTED_WITH_APS
.. autodata:: RECEIVE_OPTION_PACKET_FROM_END_DEVICE


Transmit statuses
-----------------
.. autodata:: STATUS_SUCCESS
.. autodata:: STATUS_MAC_ACK_FAILURE
.. autodata:: STATUS_CCA_FAILURE
.. autodata:: STATUS_PURGED
.. autodata:: STATUS_INVALID_DESTINATION_ENDPOINT
.. autodata:: STATUS_NETWORK_ACK_FAILURE
.. autodata:: STATUS_NOT_JOINED_TO_NETWORK
.. autodata:: STATUS_SELF_ADDRESSED
.. autodata:: STATUS_ADDRESS_NOT_FOUND
.. autodata:: STATUS_ROUTE_NOT_FOUND
.. autodata:: STATUS_NEIGHBOR_FAILURE
.. autodata:: STATUS_INVALID_BINDING_TABLE_INDEX
.. autodata:: STATUS_RESOURCE_ERROR
.. autodata:: STATUS_ATTEMPTED_BROADCAST_WITH_APS
.. autodata:: STATUS_ATTEMPTED_UNICAST_APS
.. autodata:: STATUS_RESOURCE_ERROR_2
.. autodata:: STATUS_DATA_PAYLOAD_TOO_LARGE
.. autodata:: STATUS_INDIRECT_MESSAGE_UNREQUESTED


Discovery statuses
------------------
.. autodata:: DISCOVERY_STATUS_NO_OVERHEAD
.. autodata:: DISCOVERY_STATUS_ADDRESS
.. autodata:: DISCOVERY_STATUS_ROUTE
.. autodata:: DISCOVERY_STATUS_ADDRESS_AND_ROUTE
.. autodata:: DISCOVERY_STATUS_EXTENDED_TIMEOUT


Command statuses
----------------
.. autodata:: COMMAND_STATUS_OK
.. autodata:: COMMAND_STATUS_ERROR
.. autodata:: COMMAND_STATUS_INVALID_COMMAND
.. autodata:: COMMAND_STATUS_INVALID_PARAMETER
.. autodata:: COMMAND_STATUS_NO_RESPONSE


Modem statuses
--------------
.. autodata:: MODEM_STATUS_HARDWARE_RESET
.. autodata:: MODEM_STATUS_WATCHDOG_TIMER_RESET
.. autodata:: MODEM_STATUS_ASSOCIATED
.. autodata:: MODEM_STATUS_DISASSOCIATED
.. autodata:: MODEM_STATUS_SYNCHRONIZATION_LOST
.. autodata:: MODEM_STATUS_COORDINATOR_REALIGNMENT
.. autodata:: MODEM_STATUS_COORDINATOR_STARTED
.. autodata:: MODEM_STATUS_NETWORK_SECURITY_KEY_UPDATED
.. autodata:: MODEM_STATUS_VOLTAGE_SUPPLY_LIMIT_EXCEEDED
.. autodata:: MODEM_STATUS_MODEM_CONFIGURATION_CHANGED_WHILE_JOINING
.. autodata:: MODEM_STATUS_STACK_ERROR_MIN
