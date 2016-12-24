import discord
import asyncio

triggerString = "!"
"""
@asyncio.coroutine
def handle_outgoing(payload, loop):

    
    reader, writer = yield from asyncio.open_connection(host, gameport, loop=loop)
    packet = format_packet(payload)
    
    writer.write(packet)
    
    headerReceived = yield from reader.read(2)
    if headerReceived != b"\x00\x83":
        print("Unexpected packet.")
        
    packetLength = yield from reader.read(2)
    packetLength = int.from_bytes(packetLength, "big")
    received = yield from reader.read(packetLength)
    received = received[1:-1]
    
    writer.close()
    return received
"""

@asyncio.coroutine
def handle_outgoing(payload, loop):

    print("Entering handle_outgoing")
    
    reader, writer = yield from asyncio.open_connection(host, gameport, loop=loop)
    print("Connection opened.")    
    
    packet = formatpacket(payload)
    print("Packet formatted.")    
    
    writer.write(bytes(payload, "ascii"))
    print("Packet sent.")
    
    received = yield from reader.read(-1)
    print("Packet received.")
    
    print(received)
    
    print("Closing socket.")
    writer.close()
    print("Socket closed.")
    
def get_command(messageobj):

    i = messageobj.content.strip(triggerString)
    command = i.split(" ")[0]
    print(command)
    if len(i.split(" ")) >= 2:
        parameter = i.split(" ")[1]
        print (parameter)
        if len(i.split(" ", maxsplit=2)) >= 3:
            cmdMsg = i.split(" ", maxsplit=2)[2]
            print (cmdMsg)
            
    return command

class Command(object):
    
    def __init__(self, client, loop, message):
        client = self.client
        loop = self.loop
        message = self.message
        
    @asyncio.coroutine
    def do_command(self):
        yield from self.client.send_message(self.message.channel, "Doing command: %s" % self.message.content.split(" ")[0])
        command = get_command(self.message)
        output = handle_outgoing(command, loop)
        print(output)

class Ping(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message
    
class Players(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

class Status(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

class Manifest(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

class Revision(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

class Laws(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

class Info(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

class AdminMsg(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

class Notes(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

class Age(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message
        
class Help(Command):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message
        
class InvalidCommand(Command):

    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message