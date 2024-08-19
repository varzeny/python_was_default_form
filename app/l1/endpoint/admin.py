# endpoint/admin.py

# lib
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse, FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

# l2
import app.l2.authorization as AUTH

# definition
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(AUTH.admin_only)]
)
template = Jinja2Templates(directory="app/template/admin")

# endpoint
@router.get("/")
async def get_root(req:Request):


    resp = template.TemplateResponse(
        request=req,
        name="dashboard.html",
        context={},
        status_code=200
    )
    return resp