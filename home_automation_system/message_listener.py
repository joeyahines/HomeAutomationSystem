import asyncio
import importlib
import json


async def handle_messages(reader, writer):
    type = (await reader.readexactly(4)).decode()
    sender = (await reader.readexactly(4)).decode()
    size = int((await reader.readexactly(4)).decode())

    message = (await reader.read(size)).decode()

    msg_json = json.loads(message)

    addr = writer.get_extra_info('peername')
    print("Received from %r:\n %r" % (addr, msg_json))

    test = importlib.import_module('home_automation_system.rules.test_rules')

    ruleset = test.get_ruleset()

    await ruleset.run_rules(msg_json["data"], **msg_json["rules"])

    print("Close the client socket")
    writer.close()


def startup():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_messages, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    startup()
