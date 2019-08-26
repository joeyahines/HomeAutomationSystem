import unittest
import asyncio
import json


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    message = "111111119999" + message
    print(f'Send: {message!r}')
    writer.write(message.encode())

    print('Close the connection')
    writer.close()


class MessageTest(unittest.TestCase):
    def test_message_recv(self):
        json_msg = {"data": {"test": "123"}, "rules": {"Test": "yes"}}
        loop = asyncio.get_event_loop()

        loop.run_until_complete(tcp_echo_client(json.dumps(json_msg)))

        loop.close()


