import grpc
from concurrent import futures
import asyncio
from grpc_reflection.v1alpha import reflection
from app.grpc_generated import session_service_pb2_grpc, session_service_pb2

class SessionService(session_service_pb2_grpc.SessionServiceServicer):
    async def SyncSession(self, request, context):
        print(f"Session sync received: {request.user_id} | {request.session_event} @ {request.timestamp}")
        # Here you could update the DB or cache
        return session_service_pb2.SessionSyncResponse(message="Session synced successfully")

async def serve():
    server = grpc.aio.server()
    session_service_pb2_grpc.add_SessionServiceServicer_to_server(SessionService(), server)
    server.add_insecure_port("[::]:50053")
    await server.start()
    print("Session gRPC Service running on port 50053...")
    await server.wait_for_termination()
