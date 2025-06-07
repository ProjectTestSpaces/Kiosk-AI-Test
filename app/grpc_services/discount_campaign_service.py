import grpc
from concurrent import futures
from app.grpc_generated import discount_campaign_pb2_grpc, discount_campaign_pb2

class DiscountCampaignService(discount_campaign_pb2_grpc.DiscountCampaignServiceServicer):
    async def SyncCampaign(self, request, context):
        print(f"[gRPC] Synced campaign: {request.campaign_id}")
        return discount_campaign_pb2.CampaignSyncResponse(
            message=f"Discount campaign {request.campaign_id} synced successfully"
        )

async def serve():
    server = grpc.aio.server()
    discount_campaign_pb2_grpc.add_DiscountCampaignServiceServicer_to_server(
        DiscountCampaignService(), server
    )
    server.add_insecure_port('[::]:50055')
    print("gRPC DiscountCampaignService running on port 50055...")
    await server.start()
    await server.wait_for_termination()
