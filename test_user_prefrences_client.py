# import grpc
# from app.grpc_generated import user_preference_pb2_grpc, user_preference_pb2
# import asyncio

# async def run():
#     async with grpc.aio.insecure_channel('localhost:50052') as channel:
#         stub = user_preference_pb2_grpc.UserPreferenceServiceStub(channel)
#         response = await stub.UpdatePreference(user_preference_pb2._USERPREFERENCEREQUEST(
#             user_id="user-1234",
#             preference_key="favorite_category",
#             preference_value="electronics"
#         ))
#         print("gRPC Response:", response.message)

# if __name__ == "__main__":
#     asyncio.run(run())

import grpc
from app.grpc_generated import user_preference_pb2_grpc, user_preference_pb2
import asyncio

async def run():
    async with grpc.aio.insecure_channel('localhost:50053') as channel:
        stub = user_preference_pb2_grpc.UserPreferenceServiceStub(channel)
        response = await stub.UpdatePreference(user_preference_pb2.UserPreferenceRequest(
            user_id="user-1234",
            preference_key="favorite_category",
            preference_value="electronics"
        ))
        print("gRPC Response:", response.message)

if __name__ == "__main__":
    asyncio.run(run())

