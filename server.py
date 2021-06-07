from asyncio.subprocess import Process
import asyncio
import click
import typing as ty
from datetime import datetime

import grpc
from activator_pb2 import ActivationStatus, Empty
from activator_pb2_grpc import ( ActivatorServicer, add_ActivatorServicer_to_server)

def log(msg: str):
    print("[{}][Server] {}".format(datetime.now(), msg))

class ActivatorService(ActivatorServicer):

    process: ty.Optional[Process] = None

    async def Toggle(self, _, context):
        log("RPC Toggle()")
        if self.process is None:
            self.process = await asyncio.create_subprocess_exec("./sleep_4ever")
            return ActivationStatus(current_status=ActivationStatus.Status.ACTIVE)
        else:
            self.process.terminate()
            self.process = None
            return ActivationStatus(current_status=ActivationStatus.Status.INACTIVE)

    async def CurrentStatus(self, _, context):
        log("RPC CurrentStatus()")
        if self.process is None:
            return ActivationStatus(current_status=ActivationStatus.Status.INACTIVE)
        elif self.process.returncode is None:
            return ActivationStatus(current_status=ActivationStatus.Status.INACTIVE)
        else:
            return ActivationStatus(current_status=ActivationStatus.Status.ACTIVE)

    async def StreamStatus(self, _, context):
        log("RPC StreamStatus()")
        while True:
            yield await self.CurrentStatus(Empty(), context)
            log("RPC StreamStatus served()")
            await asyncio.sleep(1)

async def async_server(port: str):
    print("Hello, I am a server")
    server = grpc.aio.server()
    add_ActivatorServicer_to_server(ActivatorService(), server)
    server.add_insecure_port("localhost:" + port)
    await server.start()
    await server.wait_for_termination()

@click.command()
@click.argument("port")
def main(port: str):
    asyncio.run(async_server(port))

if __name__ == "__main__":
    main()
