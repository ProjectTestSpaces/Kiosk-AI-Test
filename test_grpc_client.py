import grpc
from app.grpc_generated import admin_service_pb2,admin_service_pb2_grpc

async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = admin_service_pb2_grpc.AdminServiceStub(channel)
        response = await stub.UpdateUserStatus(admin_service_pb2.UserStatusRequest(
            user_id="333e4567-e89b-12d3-a456-426614174000", new_status="banned"
        ))
        print("Response from gRPC server:", response.message)

if __name__ == '__main__':
    import asyncio
    asyncio.run(run())
