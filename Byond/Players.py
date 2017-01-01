import urllib.parse
import ..config
import discord
import asyncio

class Players(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            command = "status"
            status = yield from self.get_server_info(command, self.loop)
            status = urllib.parse.parse_qs(status)
            playercount = status["players"][0]
            playerList = []
            for key in status:
                if "player" in key and not "players" in key:
                    playerList.append(status[key][0])
            playerList = sorted(playerList)
            playerMsg = "```\r\n"
            for player in playerList:
                playerMsg = playerMsg + player + "\r\n"
            playerMsg += "\r\nPlayers online: %s```" % playercount
            yield from self.client.send_message(self.message.author, playerMsg)
        except OSError:
            yield from self.client.send_message(self.message.author, "Server is offline.")