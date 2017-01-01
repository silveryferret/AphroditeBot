import discord
import asyncio
import ..config

class Help(Command):

    @asyncio.coroutine
    def do_command(self):

        prepend = config.triggerString

        helpMsg = ""
        helpMsg += "```Aphrodite Bot Commands:\r\n"
        helpMsg += prepend + "ping                 - checks if server is up\r\n"
        helpMsg += prepend + "status               - status, including round duration, station time,\r\n"
        helpMsg += "\tplayers online\r\n"
        helpMsg += prepend + "players              - PMs you a message of all players on server\r\n"
        helpMsg += prepend + "manifest             - PMs you a message of the in round crew manifest\r\n"
        helpMsg += prepend + "revision             - shows current server revision\r\n"
        if self.message.channel.id == config.ahelpID:
            helpMsg += prepend + "info <ckey>          - shows detailed information about ckey\r\n"
            helpMsg += prepend + "msg <ckey> <message> - adminhelps from discord to game\r\n"
            helpMsg += prepend + "notes <ckey>         - get player notes of ckey\r\n"
            helpMsg += prepend + "age <ckey>           - shows player age of ckey\r\n"
            helpMsg += prepend + "ip <ckey>            - shows IP of ckey"
        helpMsg += "```"
        yield from self.client.send_message(self.message.channel, helpMsg)