# import os
# import asyncio
# from contextlib import asynccontextmanager

# from fastapi import FastAPI
# from app.api import auth, admin, shop_admin
# from app.db import database
# from app.middleware.logging import AdminLoggingMiddleware
# from app.middleware.validation import AdminJWTMiddleware
# from app.middleware.rbac import RBACMiddleware
# from app.grpc_services.admin_service import serve as serve_admin
# from app.grpc_services.inventory_service import serve as serve_inventory
# from app.middleware.error_handler import EnhancedErrorHandlerMiddleware

# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from fastapi import Request


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Lifespan event handler for startup and shutdown events."""
#     # Startup
#     await database.connect()
#     print("Database connected successfully")

#     # Start both gRPC services concurrently
#     loop = asyncio.get_event_loop()
#     admin_grpc = loop.create_task(serve_admin())
#     inventory_grpc = loop.create_task(serve_inventory())
#     print("gRPC Admin & Inventory Services started")

#     yield

#     # Shutdown
#     await database.disconnect()
#     print("Database disconnected")

#     # Stop gRPC services
#     for task in [admin_grpc, inventory_grpc]:
#         if not task.done():
#             task.cancel()
#             try:
#                 await task
#             except asyncio.CancelledError:
#                 pass
#     print("gRPC services stopped")


# app = FastAPI(
#     title="SANHRI-X Backend",
#     description="API documentation for the SANHRI-X Mall AI Assistant backend, including Admin Panel endpoints.",
#     version="1.0.0",
#     lifespan=lifespan,
#     contact={
#         "name": "TechnoNexis Backend Team",
#         "email": "backend@technonexis.com"
#     },
#     license_info={
#         "name": "MIT License",
#     }
# )

# # Routers
# app.include_router(auth.router)
# app.include_router(admin.router)
# app.include_router(shop_admin.router)

# # Middleware
# debug_mode = os.getenv("DEBUG", "false").lower() == "true"
# app.add_middleware(EnhancedErrorHandlerMiddleware, debug=debug_mode)
# app.add_middleware(RBACMiddleware)
# app.add_middleware(AdminJWTMiddleware)
# app.add_middleware(AdminLoggingMiddleware)

# @app.get("/")
# def root():
#     return {"Welcome": "SANHRI"}









# import os
# import asyncio
# from contextlib import asynccontextmanager

# from fastapi import FastAPI, Request
# from app.api import auth, admin, shop_admin
# from app.db import database
# from app.middleware.logging import AdminLoggingMiddleware
# from app.middleware.validation import AdminJWTMiddleware
# from app.middleware.rbac import RBACMiddleware
# from app.grpc_services.admin_service import serve as serve_admin
# from app.grpc_services.inventory_service import serve as serve_inventory
# from app.middleware.error_handler import EnhancedErrorHandlerMiddleware

# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address

# # -------------------------
# # Rate Limiter Setup
# # -------------------------
# limiter = Limiter(key_func=get_remote_address)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Lifespan event handler for startup and shutdown events."""
#     # Startup
#     await database.connect()
#     print("Database connected successfully")

#     # Start both gRPC services concurrently
#     loop = asyncio.get_event_loop()
#     admin_grpc = loop.create_task(serve_admin())
#     inventory_grpc = loop.create_task(serve_inventory())
#     print("gRPC Admin & Inventory Services started")

#     yield

#     # Shutdown
#     await database.disconnect()
#     print("Database disconnected")

#     # Stop gRPC services
#     for task in [admin_grpc, inventory_grpc]:
#         if not task.done():
#             task.cancel()
#             try:
#                 await task
#             except asyncio.CancelledError:
#                 pass
#     print("gRPC services stopped")

# # -------------------------
# # FastAPI App Config
# # -------------------------
# app = FastAPI(
#     title="SANHRI-X Backend",
#     description="API documentation for the SANHRI-X Mall AI Assistant backend, including Admin Panel endpoints.",
#     version="1.0.0",
#     lifespan=lifespan,
#     contact={
#         "name": "TechnoNexis Backend Team",
#         "email": "backend@technonexis.com"
#     },
#     license_info={
#         "name": "MIT License",
#     }
# )

# # Attach rate limiter to app
# app.state.limiter = limiter
# app.add_exception_handler(429, _rate_limit_exceeded_handler)

# # -------------------------
# # Routers
# # -------------------------
# app.include_router(auth.router)
# app.include_router(admin.router)
# app.include_router(shop_admin.router)

# # -------------------------
# # Middleware
# # -------------------------
# debug_mode = os.getenv("DEBUG", "false").lower() == "true"
# app.add_middleware(EnhancedErrorHandlerMiddleware, debug=debug_mode)
# app.add_middleware(RBACMiddleware)
# app.add_middleware(AdminJWTMiddleware)
# app.add_middleware(AdminLoggingMiddleware)

# # -------------------------
# # Root
# # -------------------------
# @app.get("/")
# def root():
#     return {"Welcome": "SANHRI"}









# import os
# import asyncio
# from contextlib import asynccontextmanager

# from fastapi import FastAPI
# from app.api import auth, admin, shop_admin
# from app.db import database
# from app.middleware.logging import AdminLoggingMiddleware
# from app.middleware.validation import AdminJWTMiddleware
# from app.middleware.rbac import RBACMiddleware
# from app.grpc_services.admin_service import serve as serve_admin
# from app.grpc_services.inventory_service import serve as serve_inventory
# from app.middleware.error_handler import EnhancedErrorHandlerMiddleware

# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from fastapi import Request


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Lifespan event handler for startup and shutdown events."""
#     # Startup
#     await database.connect()
#     print("Database connected successfully")

#     # # Start both gRPC services concurrently
#     # loop = asyncio.get_event_loop()
#     # admin_grpc = loop.create_task(serve_admin())
#     # inventory_grpc = loop.create_task(serve_inventory())
#     # print("gRPC Admin & Inventory Services started")

#     yield

#     # Shutdown
#     await database.disconnect()
#     print("Database disconnected")

#     # # Stop gRPC services
#     # for task in [admin_grpc, inventory_grpc]:
#     #     if not task.done():
#     #         task.cancel()
#     #         try:
#     #             await task
#     #         except asyncio.CancelledError:
#     #             pass
#     # print("gRPC services stopped")


# app = FastAPI(
#     title="SANHRI-X Backend",
#     description="API documentation for the SANHRI-X Mall AI Assistant backend, including Admin Panel endpoints.",
#     version="1.0.0",
#     lifespan=lifespan,
#     contact={
#         "name": "TechnoNexis Backend Team",
#         "email": "backend@technonexis.com"
#     },
#     license_info={
#         "name": "MIT License",
#     }
# )

# # Routers
# app.include_router(auth.router)
# app.include_router(admin.router)
# app.include_router(shop_admin.router)

# # Middleware
# debug_mode = os.getenv("DEBUG", "false").lower() == "true"
# app.add_middleware(EnhancedErrorHandlerMiddleware, debug=debug_mode)
# app.add_middleware(RBACMiddleware)
# app.add_middleware(AdminJWTMiddleware)
# app.add_middleware(AdminLoggingMiddleware)

# @app.get("/")
# def root():
#     return {"Welcome": "SANHRI"}



# import os
# import asyncio
# import threading
# from contextlib import asynccontextmanager

# from fastapi import FastAPI, Request
# from app.api import auth, admin, shop_admin
# from app.db import database
# from app.middleware.logging import AdminLoggingMiddleware
# from app.middleware.validation import AdminJWTMiddleware
# from app.middleware.rbac import RBACMiddleware
# from app.grpc_services.admin_service import serve as serve_admin
# from app.grpc_services.inventory_service import serve as serve_inventory
# from app.middleware.error_handler import EnhancedErrorHandlerMiddleware

# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address

# # -------------------------
# # Rate Limiter Setup
# # -------------------------
# limiter = Limiter(key_func=get_remote_address)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Lifespan event handler for startup and shutdown events."""
#     # Startup
#     await database.connect()
#     print("Database connected successfully")

#     # Start gRPC services in background threads to avoid blocking
#     def run_grpc_admin():
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         try:
#             loop.run_until_complete(serve_admin())
#         except Exception as e:
#             print(f"gRPC Admin service error: {e}")
#         finally:
#             loop.close()

#     def run_grpc_inventory():
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         try:
#             loop.run_until_complete(serve_inventory())
#         except Exception as e:
#             print(f"gRPC Inventory service error: {e}")
#         finally:
#             loop.close()

#     # Start gRPC services in daemon threads
#     admin_thread = threading.Thread(target=run_grpc_admin, daemon=True)
#     inventory_thread = threading.Thread(target=run_grpc_inventory, daemon=True)
    
#     admin_thread.start()
#     inventory_thread.start()
    
#     print("gRPC Admin & Inventory Services started in background")

#     yield

#     # Shutdown
#     await database.disconnect()
#     print("Database disconnected")
#     print("gRPC services will stop automatically (daemon threads)")

# # -------------------------
# # FastAPI App Config
# # -------------------------
# app = FastAPI(
#     title="SANHRI-X Backend",
#     description="API documentation for the SANHRI-X Mall AI Assistant backend, including Admin Panel endpoints.",
#     version="1.0.0",
#     lifespan=lifespan,
#     contact={
#         "name": "TechnoNexis Backend Team",
#         "email": "backend@technonexis.com"
#     },
#     license_info={
#         "name": "MIT License",
#     }
# )

# # Attach rate limiter to app
# app.state.limiter = limiter
# app.add_exception_handler(429, _rate_limit_exceeded_handler)

# # -------------------------
# # Routers
# # -------------------------
# app.include_router(auth.router)
# app.include_router(admin.router)
# app.include_router(shop_admin.router)

# # -------------------------
# # Middleware
# # -------------------------
# debug_mode = os.getenv("DEBUG", "false").lower() == "true"
# app.add_middleware(EnhancedErrorHandlerMiddleware, debug=debug_mode)
# app.add_middleware(RBACMiddleware)
# app.add_middleware(AdminJWTMiddleware)
# app.add_middleware(AdminLoggingMiddleware)

# # -------------------------
# # Root
# # -------------------------
# @app.get("/")
# def root():
#     return {"Welcome": "SANHRI"}






























# import logging

# # Configure API performance logger
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
#     handlers=[
#         logging.StreamHandler(),  # Console
#         logging.FileHandler("logs/api_performance.log", mode="a")  # Optional file
#     ]
# )


import os
import asyncio
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # ✅ CORS support

from app.api import auth, admin, shop_admin,store_hours,health

from app.db import database

from app.middleware.logging import AdminLoggingMiddleware
from app.middleware.validation import AdminJWTMiddleware
from app.middleware.rbac import RBACMiddleware
from app.middleware.performance_logging import PerformanceLoggingMiddleware

from app.grpc_services.admin_service import serve as serve_admin
from app.grpc_services.inventory_service import serve as serve_inventory
from app.grpc_services.session_service import serve as serve_session
from app.grpc_services.user_preference_service import serve as serve_user_preferences
from app.grpc_services.discount_campaign_service import serve as serve_discount_campaign

from app.middleware.error_handler import EnhancedErrorHandlerMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from app.extensions.limiter import limiter

from app.api import analytics
from app.api import discount_campaign

# -------------------------
# Rate Limiter Setup
# -------------------------
# limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown events."""
    # Startup
    await database.connect()
    print("Database connected successfully")
    
    # Start gRPC services in background threads to avoid blocking
    def run_grpc_admin():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(serve_admin())
        except Exception as e:
            print(f"gRPC Admin service error: {e}")
        finally:
            loop.close()

    def run_grpc_inventory():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(serve_inventory())
        except Exception as e:
            print(f"gRPC Inventory service error: {e}")
        finally:
            loop.close()


    def run_grpc_session():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(serve_session())
        except Exception as e:
            print(f"gRPC Session service error: {e}")
        finally:
            loop.close()

    def run_grpc_user_preferences():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(serve_user_preferences())
        except Exception as e:
            print(f"gRPC User Prefrence error: {e}")
        finally:
            loop.close()


    def run_grpc_discount_campaign():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(serve_discount_campaign())
        except Exception as e:
            print(f"gRPC Discount Campaign error: {e}")
        finally:
            loop.close()
    

    # Start gRPC services in daemon threads
    admin_thread = threading.Thread(target=run_grpc_admin, daemon=True)
    inventory_thread = threading.Thread(target=run_grpc_inventory, daemon=True)
    session_thread = threading.Thread(target=run_grpc_session, daemon=True)
    user_preferences_thread = threading.Thread(target=run_grpc_user_preferences, daemon=True)
    discount_thread = threading.Thread(target=run_grpc_discount_campaign, daemon=True)
    
    admin_thread.start()
    inventory_thread.start()
    session_thread.start()
    user_preferences_thread.start()
    discount_thread.start()
    
    print("gRPC Admin,Inventory, Session,User_Prefrences & Discount Campaign Services started in background")
    
    yield
    
    # Shutdown
    await database.disconnect()
    print("Database disconnected")
    print("gRPC services will stop automatically (daemon threads)")

# -------------------------
# FastAPI App Config
# -------------------------
app = FastAPI(
    title="SANHRI-X Backend",
    description="API documentation for the SANHRI-X Mall AI Assistant backend, including Admin Panel endpoints.",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "TechnoNexis Backend Team",
        "email": "backend@technonexis.com"
    },
    license_info={
        "name": "MIT License",
    }
)
# ✅ Add CORS middleware (IMPORTANT: Add early)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # local frontend
        "https://admin.sanhri.com"    # production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Attach rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# -------------------------
# Routers
# -------------------------
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(shop_admin.router)
app.include_router(analytics.router)
app.include_router(discount_campaign.router)
app.include_router(store_hours.router)
app.include_router(health.router)  # ✅ Add this after other routers

# -------------------------
# Middleware
# -------------------------
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
app.add_middleware(EnhancedErrorHandlerMiddleware, debug=debug_mode)
app.add_middleware(RBACMiddleware)
app.add_middleware(AdminJWTMiddleware)
app.add_middleware(AdminLoggingMiddleware)
app.add_middleware(PerformanceLoggingMiddleware)


# -------------------------
# Root
# -------------------------
@app.get("/")
def root():
    return {"Welcome": "SANHRI"}