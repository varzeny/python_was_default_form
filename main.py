# main.py

"""
uvicorn main:app --host 0.0.0.0 --port 9100

background-color: rgb(43, 26, 31);
border: 1px solid lightgoldenrodyellow;

"""

# lib
from fastapi import FastAPI, staticfiles

# core
import app.core.util as UTIL

# l1
from app.l1.middleware.access import AccessMiddleware
from app.l1.endpoint.common import router as common_router
from app.l1.endpoint.guest import router as guest_router
from app.l1.endpoint.user import router as user_router
from app.l1.endpoint.admin import router as admin_router

# l2
import app.l2.database as DB
import app.l2.authorization as AUTH
import app.l2.email as EMAIL


# definition
async def startup():
    # database
    DB.setup( app.state.config["database"] )

    # authorization
    AUTH.setup( app.state.config["authorization"] )

    # email
    EMAIL.setup( app.state.config["email"] )

    
    print("startup done !")

async def shutdown():


    print("shutdown done !") 


# app
app = FastAPI(
    on_startup=[startup],
    on_shutdown=[shutdown]
)

# mount
app.mount(
    path="/static",
    app=staticfiles.StaticFiles(directory="app/static")
)

# middleware
app.add_middleware( AccessMiddleware )

# router
app.include_router( common_router )
app.include_router( guest_router )
app.include_router( user_router )
app.include_router( admin_router )

# config
app.state.config = UTIL.read_json_from_file("config.json")


if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9100, reload=True)
