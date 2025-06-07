import grpc
from app.grpc_generated import inventory_service_pb2_grpc, inventory_service_pb2

async def run():
    async with grpc.aio.insecure_channel('localhost:50052') as channel:
        stub = inventory_service_pb2_grpc.InventoryServiceStub(channel)
        response = await stub.UpdateInventory(inventory_service_pb2.InventoryUpdateRequest(
            product_id="12345", quantity=10, action="add"
        ))
        print("gRPC Response:", response.message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
