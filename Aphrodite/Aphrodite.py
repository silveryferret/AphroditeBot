import asyncio
import discord
from . import Command
from .. import config
from ..Byond import AdminMsg
from ..Byond import Age
from ..Byond import Info
from ..Byond import IP
from ..Byond import Manifest
from ..Byond import Notes
from ..Byond import Ping
from ..Byond import Players
from ..Byond import Revision
from ..Byond import Status


class Aphrodite(discord.Client):

    def get_command(self, messageObj):

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

    def has_perms(self, user):
        for i in user.roles:
            if str(i) in config.perm_roles:
                return True
            else:
                perm = False
        return perm

    @asyncio.coroutine
    def parse_command(self, message, client, loop):

        command = self.get_command(message)

        if message.content.startswith(config.triggerString) == False:
            return Command.Command(client, loop, message)

        if command[0] == "ping":
            return Ping.Ping(client, loop, message)
        elif command[0] == "status":
            return Status.Status(client, loop, message)
        elif command[0] == "players":
            return Players.Players(client, loop, message)
        elif command[0] == "manifest":
            return Manifest.Manifest(client, loop, message)
        elif command[0] == "revision":
            return Revision.Revision(client, loop, message)
        elif command[0] == "info":
            if self.has_perms(message.author):
                return Info.Info(client, loop, message)
            else:
                return Command.Command(client, loop, message)
        elif command[0] == "msg":
            if self.has_perms(message.author):
                return AdminMsg.AdminMsg(client, loop, message)
            else:
                return Command.Command(client, loop, message)
        elif command[0] == "notes":
            if self.has_perms(message.author):
                return Notes.Notes(client, loop, message)
            else:
                return Command.Command(client, loop, message)
        elif command[0] == "age":
            if self.has_perms(message.author):
                return Age.Age(client, loop, message)
            else:
                return Command.Command(client, loop, message)
        elif command[0] == "ip":
            if self.has_perms(message.author):
                return IP.IP(client, loop, message)
            else:
                return Command.Command(client, loop, message)
        elif command[0] == "help":
            return Help.Help(client, loop, message)
        else:
            return Command.Command(client, loop, message)


    @asyncio.coroutine
    def on_ready(self):
        print("Bot is ready.")

    @asyncio.coroutine
    def on_message(self, message):

        author = message.author

        if author.id == self.user.id:
            return

        cmd = yield from self.parse_command(message, self, loop)
        yield from cmd.do_command()