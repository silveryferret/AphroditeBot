import discord
import asyncio
import struct
import ast
import urllib.parse
import config

def format_packet(msg):
    return b"\x00\x83" + struct.pack(">H", len(msg) + 6) + \
    b"\x00\x00\x00\x00\x00" + bytes(msg, "ascii") + b"\x00"

def handle_outgoing(payload, loop):

    reader, writer = yield from asyncio.open_connection(config.host, config.gameport, loop=loop)
    packet = format_packet(payload)

    writer.write(packet)

    headerReceived = yield from reader.read(2)
    if headerReceived != b"\x00\x83":
        print("Unexpected packet.")

    packetLength = yield from reader.read(2)
    packetLength = int.from_bytes(packetLength, "big")
    received = yield from reader.read(packetLength)
    received = received[1:-1]
    received = received.decode("utf8")

    writer.close()
    return received

def get_command(messageObj):

    commandstring = ""
    parameter = ""
    cmdMsg = ""

    i = messageObj.content.strip(config.triggerString)
    commandstring = i.split(" ")[0]
    if len(i.split(" ")) >= 2:
        parameter = i.split(" ")[1]
        if len(i.split(" ", maxsplit=2)) >= 3:
            cmdMsg = i.split(" ", maxsplit=2)[2]
    command = (commandstring, parameter, cmdMsg)
    return command

def has_perms(user):
    for i in user.roles:
        if str(i) in config.perm_roles:
            perm = True
        else:
            perm = False
    print(perm)
    print(config.perm_roles)
    return perm

class Command(object):

    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message

    @asyncio.coroutine
    def do_command(self):
        pass

class Ping(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            command = get_command(self.message)[0]
            yield from handle_outgoing(command, self.loop)
            yield from self.client.send_message(self.message.channel, "Server is online.")
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

class Status(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            command = "status"
            status = yield from handle_outgoing(command, self.loop)
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
            statusMsg = "```Admins online: %s\r\n" % admins
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

    def fill_departments(self, manifest, departments, departmentName, manifestMsg):
        manifestMsg += departmentName
        for name in departments:
            position = departments[name]
            manifestMsg += name + " - " + position + "\r\n"
        return manifestMsg

    @asyncio.coroutine
    def do_command(self):
        try:
            command = "manifest"
            manifest = yield from handle_outgoing(command, self.loop)
            manifest = ast.literal_eval(manifest)
            manifestMsg = "```"
            try:
                manifestMsg = self.fill_departments(manifest, manifest["heads"], "Command:\r\n", manifestMsg)
                manifestMsg += "\r\n"
            except KeyError:
                pass
            try:
                manifestMsg = self.fill_departments(manifest, manifest["sec"], "Security:\r\n", manifestMsg)
                manifestMsg += "\r\n"
            except KeyError:
                pass
            try:
                manifestMsg = self.fill_departments(manifest, manifest["eng"], "Engineering:\r\n", manifestMsg)
                manifestMsg += "\r\n"
            except KeyError:
                pass
            try:
                manifestMsg = self.fill_departments(manifest, manifest["med"], "Medical:\r\n", manifestMsg)
                manifestMsg += "\r\n"
            except KeyError:
                pass
            try:
                manifestMsg = self.fill_departments(manifest, manifest["sci"], "Science:\r\n", manifestMsg)
                manifestMsg += "\r\n"
            except KeyError:
                pass
            try:
                manifestMsg = self.fill_departments(manifest, manifest["car"], "Cargo:\r\n", manifestMsg)
                manifestMsg += "\r\n"
            except KeyError:
                pass
            try:
                manifestMsg = self.fill_departments(manifest, manifest["civ"], "Civilian:\r\n", manifestMsg)
                manifestMsg += "\r\n"
            except KeyError:
                pass
            try:
                manifestMsg = self.fill_departments(manifest, manifest["bots"], "Silicon:\r\n", manifestMsg)
                manifestMsg += "```"
            except KeyError:
                pass
            if manifestMsg == "``````":
                manifestMsg = "No crew found."
            manifestMsg += "```"
            yield from self.client.send_message(self.message.channel, manifestMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

class Revision(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            command = "revision"
            revision = yield from handle_outgoing(command, self.loop)
            revision = urllib.parse.parse_qs(revision)
            revisionMsg = "```"
            revisionMsg += "Date:                 " + revision['date'][0] + "\r\n"
            revisionMsg += "Revision:             " + revision['revision'][0] + "\r\n"
            revisionMsg += "Game ID:              " + revision['gameid'][0] + "\r\n"
            revisionMsg += "Dream Daemon version: " + revision['dd_version'][0] + "\r\n"
            revisionMsg += "Dream Maker version:  " + revision['dm_version'][0] + "\r\n"
            revisionMsg += "Branch:               " + revision['branch'][0] + "\r\n"
            revisionMsg += "```"
            yield from self.client.send_message(self.message.channel, revisionMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

class Info(Command):
        
    def parse_damage(self, damage):
        dam = urllib.parse.parse_qs(damage)
        damtup = (dam["oxy"][0], dam["tox"][0], dam["fire"][0], dam["brute"][0], dam["clone"][0], dam["brain"][0])
        return damtup

    @asyncio.coroutine
    def do_command(self):
        try:
            commandtup = get_command(self.message)
            command = "?info=" + commandtup[1]
            command += ";key=" + config.commskey
            info = yield from handle_outgoing(command, self.loop)
            if info == "No matches":
                yield from self.client.send_message(self.message.channel, "No matches.")
            else:
                info = urllib.parse.parse_qs(info)
                area = info["area"][0]
                info["area"][0] = area.replace("%ff", "")
                infoMsg = "```"
                infoMsg += "Key:           " + info["key"][0] + "\r\n"
                infoMsg += "Name:          " + info["name"][0] + "\r\n"
                infoMsg += "Species:       " + info["species"][0] + "\r\n"
                infoMsg += "Gender:        " + info["gender"][0] + "\r\n"
                infoMsg += "Role:          " + info["role"][0] + "\r\n"
                infoMsg += "Location:      " + info["loc"][0] + "\r\n"
                infoMsg += "Turf:          " + info["turf"][0] + "\r\n"
                infoMsg += "Area:          " + info["area"][0] + "\r\n"
                infoMsg += "Antag:         " + info["antag"][0] + "\r\n"
                infoMsg += "Has been rev?: "  
                if int(info["hasbeenrev"][0]):
                    infoMsg += "Yes" + "\r\n"
                else:
                    infoMsg += "No" + "\r\n"
                infoMsg += "Mob type:      " + info["type"][0] + "\r\n"
                damages = self.parse_damage(info["damage"][0])
                infoMsg += "Damage:        " + "\r\n"
                infoMsg += "--Oxy:   " + damages[0] + "\r\n"
                infoMsg += "--Tox:   " + damages[1] + "\r\n"
                infoMsg += "--Fire:  " + damages[2] + "\r\n"
                infoMsg += "--Brute: " + damages[3] + "\r\n"
                infoMsg += "--Clone: " + damages[4] + "\r\n"
                infoMsg += "--Brain: " + damages[5]
                infoMsg += "```"
                yield from self.client.send_message(self.message.channel, infoMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

class AdminMsg(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            commandtup = get_command(self.message)
            author = self.message.author
            command = "?adminmsg=" + commandtup[1]
            command += ";msg=" + commandtup[2]
            command += ";key=" + config.commskey
            command += ";sender=" + author.nick
            confirmation = yield from handle_outgoing(command, self.loop)
            yield from self.client.send_message(self.message.channel, confirmation)            
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

class Notes(Command):

    def parse(self, qs):
        qs = qs.strip("+")
        qs = qs.replace("+", " ")
        qs = qs.replace("%0d", "\r")
        qs = qs.replace("%0a", "\n")
        qs = qs.replace("%28", "(")
        qs = qs.replace("%29", ")")
        qs = qs.replace("%2c", ",")
        return qs

    @asyncio.coroutine
    def do_command(self):
        try:
            commandtup = get_command(self.message)
            command = "?notes=" + commandtup[1]
            command += ";key=" + config.commskey
            qs = yield from handle_outgoing(command, self.loop)
            confirmation = self.parse(qs)
            confirmation = "```" + confirmation + "```"
            yield from self.client.send_message(self.message.channel, confirmation)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

class Age(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            commandtup = get_command(self.message)
            command = "?age=" + commandtup[1]
            command += ";key=" + config.commskey
            age = yield from handle_outgoing(command, self.loop)
            print(age)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")

class Help(Command):

    @asyncio.coroutine
    def do_command(self):
    
        prepend = config.triggerString
        
        helpMsg = ""
        helpMsg += "```Aphrodite Bot Commands:\r\n"
        helpMsg += prepend + "ping                 - checks if server is up\r\n"
        helpMsg += prepend + "status               - status, including round duration, station time, players online\r\n"
        helpMsg += prepend + "manifest             - shows in round crew manifest\r\n"
        if self.message.channel.id == config.ahelpID:
            helpMsg += prepend + "info <ckey>          - shows detailed information about ckey\r\n"
            helpMsg += prepend + "msg <ckey> <message> - adminhelps from discord to game\r\n"
            helpMsg += prepend + "notes <ckey>         - get player notes of ckey\r\n"
            helpMsg += prepend + "age <ckey>           - shows player age of ckey\r\n"
        helpMsg += "```"
        yield from self.client.send_message(self.message.channel, helpMsg)