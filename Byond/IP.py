from . import config
import discord
import asyncio

class IP(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            commandtup = get_command(self.message)
            command = "?ip=" + commandtup[1]
            command += ";key=" + config.commskey
            ip = yield from self.get_server_info(command, self.loop)
            yield from self.client.send_message(self.message.channel, ip)            
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")