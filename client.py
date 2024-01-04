from __future__ import print_function

import logging
import asyncio

import grpc
import messagebroker_pb2
import messagebroker_pb2_grpc


async def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = messagebroker_pb2_grpc.MessageBrokerStub(channel)

        # Send a new message
        topic = messagebroker_pb2.Topic(value="new_topic")
        message = await stub.SendMessage(
            messagebroker_pb2.RawMessage(content="new_content",
                                         topic=topic)
        )
        print(message)

        # Collect topics
        topics = await stub.GetTopics(
            messagebroker_pb2.Empty()
        )
        print(topics)

        # Collect messages
        topic = messagebroker_pb2.Topic(value="new_topic")
        async for message in stub.GetMessages(topic):
            print("Got message: ", message)

if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())
