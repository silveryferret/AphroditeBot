import ..config
import asyncio
import discord

class Notes(Command):

    def parse(self, qs):
        qs = qs.replace("%26%2334%3b", '"')
        qs = qs.replace("%26%2339%3b", '"')
        qs = qs.replace("%26amp%3b", "&")
        qs = qs.replace("%26%2339;", "'")
        qs = qs.replace("%0d", "\r")
        qs = qs.replace("%0a", "\n")
        qs = qs.replace("%28", "(")
        qs = qs.replace("%29", ")")
        qs = qs.replace("%2b", "+")
        qs = qs.replace("%2c", ",")
        qs = qs.replace("%2f", "/")
        qs = qs.replace("%3a", ":")
        qs = qs.replace("%3b", ";")
        qs = qs.replace("%3f", "?")
        qs = qs.replace("%5b", "[")
        qs = qs.replace("%5d", "]")
        qs = qs.replace("+", " ")
        return qs

    def format_for_sending(self, message):
        message = "```" + message + "```"
        return message

    @asyncio.coroutine
    def send(self, qs):
        message = self.parse(qs)
        if len(message) >= 1994:
            fmtmessage = self.format_for_sending(message[:1994])
            yield from self.client.send_message(self.message.channel, fmtmessage)
            message = message[1994:]
            yield from self.send(message)
        else:
            message = "```" + message + "```"
            yield from self.client.send_message(self.message.channel, message)

    @asyncio.coroutine
    def do_command(self):
        try:
            commandtup = get_command(self.message)
            command = "?notes=" + commandtup[1]
            command += ";key=" + config.commskey
            qs = yield from self.get_server_info(command, self.loop)
            yield from self.send(qs)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")