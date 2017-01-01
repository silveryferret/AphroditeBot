class Age(Command):

    @asyncio.coroutine
    def do_command(self):
        try:
            commandtup = get_command(self.message)
            command = "?age=" + commandtup[1]
            command += ";key=" + config.commskey
            age = yield from self.get_server_info(command, self.loop)
            if age == "Ckey not found":
                yield from self.client.send_message(self.message.channel, age)
            else:
                yield from self.client.send_message(self.message.channel, "Account is %s days old." % age)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")