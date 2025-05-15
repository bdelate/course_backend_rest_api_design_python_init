from ninja import NinjaAPI
from api.endpoints.barks import router as barks_router
from api.endpoints.users import router as users_router

api = NinjaAPI()

api.add_router("/users", users_router, tags=["users"])
api.add_router("/barks", barks_router, tags=["barks"])
