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
    received = yield from reader.read(2048)
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

@asyncio.coroutine
def parse_status(reader):

   # packetLength = reader.read(2)
    #print(packetLength)
    #packetLength = int.from_bytes(packetLength, "big")
    #print(packetLength)
    #queryString = yield from reader.read(packetLength)
    #print(queryString)
    #queryString = queryString[1:-1]
    #print(queryString)
    decodedDict = reader.decode()
    statusDict = urllib.parse.parse_qs(decodedDict)
    print(statusDict)
    return statusDict

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
        #output = output.decode()
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
        
    @asyncio.coroutine
    def do_command(self):
        try:
            command = "status"
            status = yield from handle_outgoing(command, self.loop)
            status = yield from parse_status(status)
            yield from self.client.send_message(self.message.channel, "Players online: %s" % status["players"][0])
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

class Status(Command):

    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message
        
    @asyncio.coroutine
    def do_command(self):
        try:
            command = "status"
            status = yield from handle_outgoing(command, self.loop)
            status = yield from parse_status(status)
            version = status["version"][0]
            admins = status["admins"][0]
            playercount = status["players"][0]
            roundduration = status["roundduration"][0]
            stationtime = status["stationtime"][0]
            playerList = []
            for key in status:
                if "player" in key and not "players" in key:
                    print(key)
                    playerList += status[key][0]
            print(playerList)
            statusMsg = "Status: \r\n"
            statusMsg += "\r\n"
            statusMsg += "Players online: %s\r" % playercount
            statusMsg += "Admins online: %s\r\n" % admins
            statusMsg += "Round duration: %s\r\n" % roundduration
            statusMsg += "Station time: %s\r\n" % stationtime
            statusMsg += "\r\n"
            statusMsg += "Players:\r\n"
            statusMsg += "\r\n"            
            
            for player in playerList:
                print(player)
                statusMsg = statusMsg + player + "\r\n"
            print(statusMsg)
            yield from self.client.send_message(self.message.channel, statusMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")
        
        
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