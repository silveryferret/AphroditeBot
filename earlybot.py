import discord
import asyncio
import struct
import ast

host = "localhost"
port = 4213
gameport = 61926
token = "MjYxNDI2NDM1OTcxODc0ODE2.Cz4GvQ.nEJwFbd61MzZ_HXXldhAJgOyeiE"
ahelpID = "260863607661658112"
mainID = "260863628582977547"

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)

class Aphrodite(discord.Client):
    
    @asyncio.coroutine
    def on_message(self, message):
    
        author = message.author
        if message.content.startswith("!q"):
            yield from self.send_message(message.channel, "See ya, %s!" % author)
            yield from self.logout()
            loop.stop()
            
        elif message.content.startswith("!status"):
            yield from handle_outgoing("status", loop)
            
ourBot = Aphrodite()

def formatpacket(msg):
    return b"\x00\x83" + struct.pack(">H", len(msg) + 6) + \
    b"\x00\x00\x00\x00\x00" + bytes(msg, "ascii") + b"\x00"
    
@asyncio.coroutine
def handle_outgoing(payload, loop):

    print("Entering handle_outgoing")
    reader, writer = yield from asyncio.open_connection(host, gameport, loop=loop)
    print("Connection opened.")    
    packet = formatpacket(payload)
    print("Packet formatted.")    
    writer.write(bytes(payload, "ascii"))
    print("Packet sent.")
    received = yield from reader.read(-1)
    print("Packet received.")
    print(received)
    print("Closing socket.")
    writer.close()
    print("Socket closed.")
    

@asyncio.coroutine
def handle_incoming(reader, writer):

    data = yield from reader.read(-1)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    cleanMessage = " ".join(ast.literal_eval(message))

    loop.create_task(queue.put(cleanMessage))
    
    writer.write(data)
    yield from writer.drain()
    
    print("Close the client socket")
    
@asyncio.coroutine
def handle_queue():
    
    queuedMsg = yield from queue.get()
    loop.create_task(handle_queue())
    if queuedMsg.startswith("Request for Help") or queuedMsg.startswith("Reply"):
        yield from ourBot.send_message(ourBot.get_channel(ahelpID), queuedMsg)
    else:
        yield from ourBot.send_message(ourBot.get_channel(mainID), queuedMsg)
    
def main():
 
    serverCoro = asyncio.start_server(handle_incoming, host, port, loop=loop)
    server = loop.run_until_complete(serverCoro)

    print("Serving on {}".format(server.sockets[0].getsockname()))
    try:
        loop.create_task(ourBot.start(token))
        loop.create_task(handle_queue())
        loop.run_forever()
    except KeyboardInterrupt:
        pass

"""
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
"""
    
if __name__ == "__main__":
    main()