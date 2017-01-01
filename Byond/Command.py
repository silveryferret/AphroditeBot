class Command(object):

    def __init__(self, client, loop, message):
        self.client = client
        self.loop = loop
        self.message = message
        
    def format_packet(msg):
        return b"\x00\x83" + struct.pack(">H", len(msg) + 6) + \
            b"\x00\x00\x00\x00\x00" + bytes(msg, "ascii") + b"\x00"

    def get_server_info(payload, loop):

        reader, writer = yield from asyncio.open_connection(config.host, config.gameport, loop=loop)
        packet = self.format_packet(payload)

        writer.write(packet)

        headerReceived = yield from reader.read(2)
        if headerReceived != b"\x00\x83":
            print("Unexpected packet.")

        packetLength = yield from reader.read(2)
        packetLength = int.from_bytes(packetLength, "big")
        received = yield from reader.read(packetLength)
        received = received[1:-1]
        received = received.decode("utf8")

        writer.close()
        return received


    @asyncio.coroutine
    def do_command(self):
        pass