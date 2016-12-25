import discord
import asyncio
import struct
import ast
import urllib.parse

host = "localhost"
port = 45678
gameport = 61926
token = "MjYxNDI2NDM1OTcxODc0ODE2.Cz4GvQ.nEJwFbd61MzZ_HXXldhAJgOyeiE"
ahelpID = "260863607661658112"
mainID = "260863628582977547"
triggerString = "!"

def format_packet(msg):
    return b"\x00\x83" + struct.pack(">H", len(msg) + 6) + \
    b"\x00\x00\x00\x00\x00" + bytes(msg, "ascii") + urllib.parse.urlunparse("&\"key\"=\"key\"") + b"\x00"

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

@asyncio.coroutine
def parse_dict(reader):

    decodedDict = reader.decode()
    return decodedDict

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
            status = yield from parse_dict(status)
            status = urllib.parse.parse_qs(status)
            version = status["version"][0]
            admins = status["admins"][0]
            playercount = status["players"][0]
            roundduration = status["roundduration"][0]
            stationtime = status["stationtime"][0]
            playerList = []
            for key in status:
                if "player" in key and not "players" in key:
                    playerList.append(status[key][0])
            statusMsg = "```Status: \r\n"
            statusMsg += "\r\n"
            statusMsg += "Admins online: %s\r\n" % admins
            statusMsg += "Round duration: %s\r\n" % roundduration
            statusMsg += "Station time: %s\r\n" % stationtime
            statusMsg += "\r\n"
            statusMsg += "Players:\r\n"
            statusMsg += "\r\n"            
            
            for player in playerList:
                statusMsg = statusMsg + player + "\r\n"
            statusMsg += "Players online: %s\r```" % playercount
            yield from self.client.send_message(self.message.channel, statusMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")
        
        
class Manifest(Command):

    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message
        
    @asyncio.coroutine
    def do_command(self):
        try:
            command = "manifest"
            manifest = yield from handle_outgoing(command, self.loop)
            manifest = yield from parse_dict(manifest)
            manifest = ast.literal_eval(manifest)
            manifestMsg = "```"
            for departments in manifest:
                if departments == "heads":
                    manifestMsg += "Command:\r\n"
                    for name in manifest[departments]:
                        position = manifest[departments][name]
                        manifestMsg += name + " - " + position + "\r\n"
                    manifestMsg += "\r\n"
                if departments == "sec":
                    manifestMsg += "Security:\r\n"
                    for name in manifest[departments]:
                        position = manifest[departments][name]
                        manifestMsg += name + " - " + position + "\r\n"
                    manifestMsg += "\r\n"
                if departments == "eng":
                    manifestMsg += "Engineering:\r\n"
                    for name in manifest[departments]:
                        position = manifest[departments][name]
                        manifestMsg += name + " - " + position + "\r\n"
                    manifestMsg += "\r\n"
                if departments == "med":
                    manifestMsg += "Medical:\r\n"
                    for name in manifest[departments]:
                        position = manifest[departments][name]
                        manifestMsg += name + " - " + position + "\r\n"
                    manifestMsg += "\r\n"
                if departments == "sci":
                    manifestMsg += "Science:\r\n"
                    for name in manifest[departments]:
                        position = manifest[departments][name]
                        manifestMsg += name + " - " + position + "\r\n"
                    manifestMsg += "\r\n"
                if departments == "car":
                    manifestMsg += "Cargo:\r\n"
                    for name in manifest[departments]:
                        position = manifest[departments][name]
                        manifestMsg += name + " - " + position + "\r\n"
                    manifestMsg += "\r\n"
                if departments == "civ":
                    manifestMsg += "Civilian:\r\n"
                    for name in manifest[departments]:
                        position = manifest[departments][name]
                    manifestMsg += "\r\n"
                if departments == "bots":
                    manifestMsg += "Silicon:\r\n"
                    for name in manifest[departments]:
                        position = manifest[departments][name]
                        manifestMsg += name + " - " + position + "\r\n"
            manifestMsg += "```"
                        
            yield from self.client.send_message(self.message.channel, manifestMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

class Revision(Command):

    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message
        
    def do_command(self):
        try:
            command = "revision"
            revision = yield from handle_outgoing(command, self.loop)
            revision = yield from parse_dict(revision)
            revision = urllib.parse.parse_qs(revision)
            print(revision)
            revisionMsg = "```"
            revisionMsg += "Date:                 " + revision['date'][0] + "\r\n"
            revisionMsg += "Revision:             " + revision['revision'][0] + "\r\n"
            revisionMsg += "Game ID:              " + revision['gameid'][0] + "\r\n"
            revisionMsg += "Dream Daemon version: " + revision['dd_version'][0] + "\r\n"
            revisionMsg += "Dream Maker version:  " + revision['dm_version'][0] + "\r\n"
            revisionMsg += "Branch:               " + revision['branch'][0] + "\r\n"
            revisionMsg += "```"
            print(revision)
            yield from self.client.send_message(self.message.channel, revisionMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")
            
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