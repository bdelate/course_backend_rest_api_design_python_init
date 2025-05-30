from ninja import NinjaAPI
from api.endpoints.barks import router as barks_router
from api.endpoints.users import router as users_router
from common.auth.token import TokenAuth

api = NinjaAPI(auth=TokenAuth(), title="Social Dog API")

api.add_router("/users", users_router, tags=["users"])
api.add_router("/barks", barks_router, tags=["barks"])
