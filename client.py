import asyncio
from datetime import datetime
import typing as ty

import click
import grpc

from activator_pb2_grpc import ActivatorStub
from activator_pb2 import ActivationStatus, Empty

def print_ActivationStatus(status: ActivationStatus):
    print("[{}][Client] Service Status is {}".format(datetime.now(), ActivationStatus.Status.Name(status.current_status)))

async def client(port: str):
    print("Hello, I am a client\n")
    await asyncio.sleep(1) # make sure the server can start
    async with grpc.aio.insecure_channel("localhost:" + port) as channel:
        client_stub = ActivatorStub(channel)

        print("Getting status")
        status = await client_stub.CurrentStatus(Empty())
        print_ActivationStatus(status)

        await asyncio.sleep(1)

        print("Toggling status")
        status = await client_stub.Toggle(Empty())
        print_ActivationStatus(status)

        await asyncio.sleep(1)

        print("Toggling status")
        status = await client_stub.Toggle(Empty())
        print_ActivationStatus(status)

        await asyncio.sleep(1)

        print("Streaming status")
        loop_counter = 0
        async for status in client_stub.StreamStatus(Empty()):
            loop_counter += 1
            print_ActivationStatus(status)
            # does not work!
            await client_stub.Toggle(Empty())

            if loop_counter == 5:
                break

        status = await client_stub.Toggle(Empty())
        print_ActivationStatus(status)


    print("\nGoodbye from the client")


@click.command()
@click.argument("port")
def main(port: str):
    asyncio.run(client(port))


if __name__ == "__main__":
    main()
