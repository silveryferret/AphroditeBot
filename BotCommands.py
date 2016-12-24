import discord
import asyncio
import struct
import ast
import urllib.parse

host = "visiblebulge.space"
port = 45678
gameport = 8000
token = "MjYxNDI2NDM1OTcxODc0ODE2.Cz4GvQ.nEJwFbd61MzZ_HXXldhAJgOyeiE"
ahelpID = "260863607661658112"
mainID = "260863628582977547"
triggerString = "!"

def format_packet(msg):
    return b"\x00\x83" + struct.pack(">H", len(msg) + 6) + \
    b"\x00\x00\x00\x00\x00" + bytes(msg, "ascii") + b"\x00"

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

def get_command(messageObj):

    i = messageObj.content.strip(triggerString)
    command = i.split(" ")[0]
    if len(i.split(" ")) >= 2:
        parameter = i.split(" ")[1]
        if len(i.split(" ", maxsplit=2)) >= 3:
            cmdMsg = i.split(" ", maxsplit=2)[2]

    return command
    
def parse_status(queryString):

    statusDict = urllib.parse.parse_qs(queryString)
    for key in statusDict:
        if "version" in key:
            version = statusDict[key]
        if "mode" in key:
            gamemode = statusDict[key]
        if "players" in key:
            playercount = statusDict[key]
        if "admins" in key:
            admincount = statusDict[key]
        if "player" in key:
            playerList += statusDict[key]
        if "stationtime" in key:
            stationTime = statusDict[key]
        if "roundduration" in key:
            roundDuration = statusDict[key]

class Command(object):
    
    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

    @asyncio.coroutine
    def do_command(self):
        yield from self.client.send_message(self.message.channel, "Doing command: %s" % self.message.content.split(" ")[0])
        command = get_command(self.message)
        output = yield from handle_outgoing(command, self.loop)
        output = output.decode()
        print(output)

class Ping(Command):

    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

    @asyncio.coroutine
    def do_command(self):
        try:
            command = get_command(self.message)
            yield from handle_outgoing(command, self.loop)
            yield from self.client.send_message(self.message.channel, "Server is online.")
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

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

class DoNothing(Command):

    @asyncio.coroutine
    def do_command(self):
        pass