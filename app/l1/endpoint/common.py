# endpoint/common.py

# lib
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse, FileResponse
from fastapi import HTTPException

# l2
import app.l2.authorization as AUTH

# definition
router = APIRouter()
template = Jinja2Templates(directory="app/template/common")

# endpoint
@router.get("/")
async def get_root(req:Request):
    access_token:AUTH.AccessToken = req.state.access_token
    if access_token.account_role_=="guest":
        print("guest")
        pass
    elif access_token.account_role_=="user":
        print("user")
        return RedirectResponse("/user/")
    elif access_token.account_role_=="admin":
        print("admin")
        return RedirectResponse("/admin/")
    else:
        return HTTPException(status_code=400)


    resp = template.TemplateResponse(
        name="index.html",
        context={"request":req},
        status_code=200
    )
    resp.delete_cookie("sign_token")
    return resp



@router.get("/logout") # logout #############################################
async def get_logout(req:Request):
    req.state.access_token = AUTH.AccessToken( account_role_="guest" )
    return RedirectResponse(url="/")


@router.get("/favicon.ico") # icon #############################################
async def get_favicon():
    return FileResponse( path="app/static/image/icon/brightest_dungeon.ico" )