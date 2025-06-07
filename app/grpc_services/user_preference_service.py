import grpc
from grpc.aio import server
from app.grpc_generated import user_preference_pb2_grpc, user_preference_pb2

class UserPreferenceService(user_preference_pb2_grpc.UserPreferenceServiceServicer):
    async def UpdatePreference(self, request, context):
        print(f"Received preference update: {request.user_id} - {request.preference_key} = {request.preference_value}")
        return user_preference_pb2.UserPreferenceResponse(
            message=f"Preference '{request.preference_key}' updated to '{request.preference_value}'"
        )

async def serve():
    grpc_server = server()
    user_preference_pb2_grpc.add_UserPreferenceServiceServicer_to_server(UserPreferenceService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50054')
    await grpc_server.start()
    print("gRPC UserPreferenceService running on port 50054")
    await grpc_server.wait_for_termination()
