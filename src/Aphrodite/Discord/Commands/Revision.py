import asyncio
import discord
import urllib.parse

class Revision(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            command = "revision"
            revision = yield from self.get_server_info(command, self.loop)
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