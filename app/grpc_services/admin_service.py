from app.db import database
from app.models.user import users as user_table
from app.grpc_generated import admin_service_pb2, admin_service_pb2_grpc
import grpc

class AdminServiceServicer(admin_service_pb2_grpc.AdminServiceServicer):
    async def UpdateUserStatus(self, request, context):
        user_id = request.user_id
        new_status = request.new_status

        query = (
            user_table.update()
            .where(user_table.c.id == user_id)
            .values(status=new_status)
            .returning(user_table.c.id)
        )
        result = await database.fetch_one(query)
        if result:
            return admin_service_pb2.UserStatusResponse(message=f"User {user_id} status updated to {new_status}")
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return admin_service_pb2.UserStatusResponse(message="User not found")


async def serve():
    server = grpc.aio.server()
    admin_service_pb2_grpc.add_AdminServiceServicer_to_server(AdminServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("gRPC AdminService running on port 50051...")
    await server.wait_for_termination()
