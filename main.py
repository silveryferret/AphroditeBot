import discord
import asyncio
import Aphrodite/Aphrodite
import config
import ast

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)

ourBot = Aphrodite.Aphrodite()

def admin_message(message):

    if "@here" in message:
        message = message.strip("@here ")
    if message.startswith("Request for Help") \
        or message.startswith("Reply") \
        or message.endswith("no more admins online.") \
        or message.partition("PM")[1] == "PM" \
        or message == "Round has started with no admins online.":
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
    if  "Round has started with no admins online." in queuedMsg \
        or queuedMsg.endswith("no more admins online.") \
        or "All admins AFK" in queuedMsg:
        queuedMsg = "@here " + queuedMsg
    if admin_message(queuedMsg):
        yield from ourBot.send_message(ourBot.get_channel(config.ahelpID), queuedMsg)
    else:
        yield from ourBot.send_message(ourBot.get_channel(config.mainID), queuedMsg)

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