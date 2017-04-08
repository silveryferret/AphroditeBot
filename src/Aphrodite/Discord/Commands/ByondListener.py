import asyncio
import discord
import ast

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
def server_to_queue(reader, writer):

    data = yield from reader.read(-1)
    message = data.decode()
    cleanMessage = " ".join(ast.literal_eval(message))

    loop.create_task(queue.put(cleanMessage))

@asyncio.coroutine
def queue_to_discord():

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