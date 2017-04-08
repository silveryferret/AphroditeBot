import asyncio
import discord
from . import config

class AdminMsg(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            commandtup = get_command(self.message)
            author = self.message.author
            command = "?adminmsg=" + commandtup[1]
            command += ";msg=" + commandtup[2]
            command += ";key=" + config.commskey
            command += ";sender=" + author.name
            confirmation = yield from self.get_server_info(command, self.loop)
            yield from self.client.send_message(self.message.channel, confirmation)            
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")