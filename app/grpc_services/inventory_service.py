import grpc
from concurrent import futures
from app.grpc_generated import inventory_service_pb2_grpc, inventory_service_pb2

class InventoryService(inventory_service_pb2_grpc.InventoryServiceServicer):
    def UpdateInventory(self, request, context):
        product_id = request.product_id
        quantity = request.quantity
        action = request.action

        print(f"Inventory update received: {product_id} - {action} {quantity}")
        
        return inventory_service_pb2.InventoryUpdateResponse(
            message=f"Inventory for {product_id} {action}ed by {quantity}"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_service_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("gRPC InventoryService running on port 50052...")
    server.wait_for_termination()
