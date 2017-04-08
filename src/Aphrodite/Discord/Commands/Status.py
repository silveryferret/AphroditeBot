import ..config
import urllib.parse
import discord
import asyncio

# note for later: think about puting urllib.parse junk into Command.py

class Status(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            command = "status"
            status = yield from self.get_server_info(command, self.loop)
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
            statusMsg += "Players online: %s\r\n```" % playercount
            yield from self.client.send_message(self.message.channel, statusMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")