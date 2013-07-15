.. hachi documentation master file, created by
   sphinx-quickstart on Fri Jul  5 13:54:46 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Hachi
======
Release v\ |version|

Hachi is a Python library to interact with XBees.

Serial implementation
---------------------
Read :class:`~hachi.response.XBeeResponse`::

    >>> import hachi
    >>> from hachi.serial import XBeeSerial
    >>> x = XBeeSerial('/dev/ttyUSB0')
    >>> x.read_response()
    <ZBIoSampleResponse(len=18)>

Send :class:`~hachi.request.XBeeRequest`::

    >>> request = hachi.AtRequest('ID', 0xff)
    >>> x.send(request)
    >>> response = x.read_response()
    >>> response
    <AtResponse(len=xx)>
    >>> response.status == hachi.COMMAND_STATUS_OK
    True

Twisted implementation
----------------------
Use the :class:`~hachi.twisted.XBeeProtocol`::

    >>> import hachi
    >>> from hachi.twisted import XBeeProtocol
    >>> from twisted.internet import reactor
    >>> from twisted.internet.serialport import SerialPort
    >>> class TestXBee(XBeeProtocol):
    ...     def responseReceived(self, response):
    ...         print(response)
    ...
    >>> serial = SerialPort(TestXBee(), '/dev/ttyUSB0', reactor, baudrate=9600)
    >>> reactor.run()
    <ZBIoSampleResponse(len=18)>
    <ZBIoSampleResponse(len=18)>
    <ZBIoSampleResponse(len=18)>


API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api/core
   api/response
   api/request
   api/const
   api/exceptions
   api/serial
   api/twisted
