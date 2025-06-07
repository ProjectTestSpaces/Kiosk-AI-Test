import grpc
from app.grpc_generated import session_service_pb2, session_service_pb2_grpc
import asyncio

async def run():
    async with grpc.aio.insecure_channel('localhost:50053') as channel:
        stub = session_service_pb2_grpc.SessionServiceStub(channel)
        response = await stub.SyncSession(session_service_pb2.SessionSyncRequest(
            user_id="123e4567-e89b-12d3-a456-426614174000",
            session_event="login",
            timestamp="2025-06-04T10:00:00"
        ))
        print("Response:", response.message)

if __name__ == "__main__":
    asyncio.run(run())
