from .advertisement import router as advertisement_router
from .advertisement_update import router as advertisement_editing_router
from .group_director import router as group_director_router
from .simple_user import router as simple_user_router
# from .simple_user import router as user_router

routers_list = [
    advertisement_router,
    advertisement_editing_router,
    group_director_router,
    simple_user_router
]

__all__ = [
    "routers_list"
]
