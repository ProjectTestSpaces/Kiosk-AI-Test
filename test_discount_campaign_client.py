import grpc
import asyncio
from app.grpc_generated import discount_campaign_pb2, discount_campaign_pb2_grpc

async def run():
    async with grpc.aio.insecure_channel('localhost:50055') as channel:
        stub = discount_campaign_pb2_grpc.DiscountCampaignServiceStub(channel)
        response = await stub.SyncCampaign(discount_campaign_pb2.CampaignSyncRequest(
            campaign_id="c123",
            shop_id="s789",
            campaign_name="New Year Blast",
            discount_type="percentage",
            discount_value=20.0,
            start_date="2025-12-25",
            end_date="2025-12-31",
            status="active"
        ))
        print("gRPC Response:", response.message)

if __name__ == "__main__":
    asyncio.run(run())
