import asyncio
import importlib
import json

class Packet:
    def __init__(self, type, sender, size, message):
        self.type = type
        self.sender = sender
        self.size = size
        self.message = message


class HASCore:
    def __init__(self, port=8888, ip='127.0.0.1'):
        self.loop = asyncio.get_event_loop()
        self.coro = asyncio.start_server(self.handle_messages, ip, port, loop=self.loop)
        self.server = self.loop.run_until_complete(self.coro)

    async def handle_messages(self, reader, writer):
        message = await reader.read()

        packet = self.parse_packet(message)

        msg_json = json.loads(packet.message)

        addr = writer.get_extra_info('peername')
        print("Received from %r:\n %r" % (addr, msg_json))

        test = importlib.import_module('home_automation_system.rules.test_rules')

        ruleset = test.get_ruleset()

        await ruleset.run_rules(msg_json["data"], **msg_json["rules"])

        print("Close the client socket")
        writer.close()

    async def send_packet(self, message, ip, port):
        response = self.loop.run_until_complete(self._send(message, ip, port))

        return response, len(response)

    async def _send(self, message, ip, port):
        reader, writer = await asyncio.open_connection(ip, port)

        writer.write(message)
        writer.write_eof()

        response = await reader.read()
        return response

    def parse_packet(self, message):
        type = message[0:3]
        sender = message[4:7]
        size = message[8:11]

        message = message[12: size + 12]

        packet = Packet(type, sender, size, message)

        return packet


def startup():
    has = HASCore()
    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(has.server.sockets[0].getsockname()))
    try:
        has.loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    has.server.close()
    has.loop.run_until_complete(has.server.wait_closed())
    has.loop.close()


if __name__ == "__main__":
    startup()
