from ninja import NinjaAPI

from backend.core.api_v1 import router as core_router

api = NinjaAPI()

api.add_router("/v1/", core_router)
