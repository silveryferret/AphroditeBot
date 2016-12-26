import discord
import asyncio
import BotCommands
import config

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)

def has_perms(user):
    for i in user.roles:
        print(i)
        if str(i) in config.perm_roles:
            perm = True
        else:
            perm = False
    print(perm)
    print(config.perm_roles)
    return perm

@asyncio.coroutine
def parse_command(message, client, loop):

    command = BotCommands.get_command(message)

    if message.content.startswith(config.triggerString) == False:
        return BotCommands.Command(client, loop, message)

    if command[0] == "ping":
        return BotCommands.Ping(client, loop, message)
    elif command[0] == "status":
        return BotCommands.Status(client, loop, message)
    elif command[0] == "manifest":
        return BotCommands.Manifest(client, loop, message)
    elif command[0] == "revision":
        return BotCommands.Revision(client, loop, message)
    elif command[0] == "info":
        if has_perms(message.author) == True:
            return BotCommands.Info(client, loop, message)
        else:
            return BotCommands.Command(client, loop, message)
    elif command[0] == "msg":
        if has_perms(message.author):
            return BotCommands.AdminMsg(client, loop, message)
        else:
            return BotCommands.Command(client, loop, message)
    elif command[0] == "notes":
        if has_perms(message.author):
            return BotCommands.Notes(client, loop, message)
        else:
            return BotCommands.Command(client, loop, message)
    elif command[0] == "age":
        if has_perms(message.author):
            return BotCommands.Age(client, loop, message)
        else:
            return BotCommands.Command(client, loop, message)
    elif command[0] == "help":
        return BotCommands.Help(client, loop, message)
    else:
        return BotCommands.Command(client, loop, message)

class Aphrodite(discord.Client):

    @asyncio.coroutine
    def on_ready(self):
        print("Bot is ready.")

    @asyncio.coroutine
    def on_message(self, message):

        author = message.author

        if author.id == self.user.id:
            return

        cmd = yield from parse_command(message, self, loop)
        yield from cmd.do_command()

ourBot = Aphrodite()

def admin_message(message):
    if message.startswith("Request for Help") or message.startswith("Reply") or message.endswith("no more admins online."):
        return True

@asyncio.coroutine
def handle_incoming(reader, writer):

    data = yield from reader.read(-1)
    message = data.decode()
    cleanMessage = " ".join(ast.literal_eval(message))

    loop.create_task(queue.put(cleanMessage))

@asyncio.coroutine
def handle_queue():

    queuedMsg = yield from queue.get()
    loop.create_task(handle_queue())
    if admin_message(queuedMsg):
        yield from ourBot.send_message(ourBot.get_channel(ahelpID), queuedMsg)
    else:
        yield from ourBot.send_message(ourBot.get_channel(mainID), queuedMsg)

def main():

    serverCoro = asyncio.start_server(handle_incoming, config.host, config.port, loop=loop)
    server = loop.run_until_complete(serverCoro)

    try:
        loop.create_task(ourBot.start(config.token))
        loop.create_task(handle_queue())
        loop.run_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()