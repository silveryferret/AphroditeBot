from . import config
import discord
import asyncio

class Ping(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            command = get_command(self.message)[0]
            yield from self.get_server_info(command, self.loop)
            yield from self.client.send_message(self.message.channel, "Server is online.")
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")