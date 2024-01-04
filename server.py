import logging
import asyncio
from collections import defaultdict

import grpc
import messagebroker_pb2
import messagebroker_pb2_grpc
import uuid

message_store = defaultdict(lambda: [])


class MessageBroker(messagebroker_pb2_grpc.MessageBrokerServicer):
    async def SendMessage(self, request, context):
        message = messagebroker_pb2.Message(
            id=str(uuid.uuid4()),
            topic=request.topic,
            content=request.content
        )

        message_store[request.topic.value].append(message)
        print(message_store)
        return message

    async def GetTopics(self, request, context):
        return messagebroker_pb2.Topics(topics=[messagebroker_pb2.Topic(value=key) for key in message_store.keys()])

    async def GetMessages(self, request, context):
        print("Store:", message_store[request.value])
        for item in message_store[request.value]:
            yield item


async def serve() -> None:
    server = grpc.aio.server()
    messagebroker_pb2_grpc.add_MessageBrokerServicer_to_server(MessageBroker(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())