# endpoint/guest.py

# lib
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse, FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

# l2
import app.l2.content as CONTENT
import app.l2.database as DB
import app.l2.authorization as AUTH
import app.l2.email as EMAIL

# definition
router = APIRouter(
    prefix="/guest",
    dependencies=[Depends(AUTH.guest_only)]
)
template = Jinja2Templates(directory="app/template/guest")


# schema
from pydantic import BaseModel, Field
class reqSign(BaseModel):
    step_:int
    email_:str|None = Field( default=None, min_length=4, max_length=45, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    code_:int|None = Field(default=None)
    password_:str|None = Field(default=None, min_length=4, max_length=45)


class reqLogin(BaseModel):
    email_:str|None = Field( default=None, min_length=4, max_length=45, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    password_:str|None = Field(default=None, min_length=4, max_length=45)


# endpoint
@router.post("/login")
async def post_login(req:Request, reqData:reqLogin, ss:AsyncSession=Depends(DB.get_ss)):
    print("입력받은 값 : ",reqData)
    try:
        respData = await CONTENT.read_account_by_email(reqData.email_, ss)
        if reqData:
            if AUTH.verify_hash(reqData.password_, respData["hashed_password_"]):
                req.state.access_token = AUTH.AccessToken(
                    account_id_=respData["id_"],
                    account_role_=respData["role_"]
                )
                return JSONResponse(status_code=200, content={"role_":respData["role_"]})
            else:
                raise Exception("wrong password")

    except Exception as e:
        print("ERROR from post_login : ", e)
        return JSONResponse(status_code=400, content={})


@router.get("/signup")
async def get_signup(req:Request):
    resp = template.TemplateResponse(
        name="signup.html",
        context={"request":req},
        status_code=200
    )
    return resp

@router.post("/sign")
async def post_sign(req:Request, reqData:reqSign, ss:AsyncSession=Depends(DB.get_ss)):
    print("입력 받은 값 : ",reqData)
    try:
        # sign_token
        decoded_data = AUTH.get_token_from_cookie(req, "sign_token")
        if decoded_data:
            sign_token = AUTH.SignToken(**decoded_data)
        else:
            sign_token = AUTH.SignToken()

        # 정상적인 진행인지 확인
        if not sign_token.step_ == reqData.step_:
            raise Exception("wrong sequence")


        resp = JSONResponse(status_code=200, content={})

        if reqData.step_==0:
            print("step : 0")
            # 메일 확인
            respData = await CONTENT.read_account_by_email(reqData.email_, ss)
            if respData:
                raise Exception("this email is already exist")
            else:
                # email 발송
                code_ = await EMAIL.send_code_for_time(req, reqData.email_)
                if not code_:
                    raise Exception("email sequence error")

                sign_token.step_=1
                sign_token.email_=reqData.email_
                sign_token.code_= code_
                return AUTH.put_token_to_cookie(resp, sign_token)
            
        elif reqData.step_==1:
            print("step : 1")
            # print( type(reqData) )
            if not reqData.code_ == sign_token.code_:
                raise Exception("verification code is not same")
            else:
                sign_token.step_=2
                return AUTH.put_token_to_cookie(resp, sign_token)
        
        elif reqData.step_==2:
            print("step : 2")
            hashed_password_ = AUTH.create_hash(reqData.password_)
            result = await CONTENT.create_account(sign_token.email_, hashed_password_, ss)
            if not result:
                raise Exception("insert account fail")
            else:
                resp.delete_cookie("sign_token")
                await ss.commit()
                return resp
        
        else:
            raise Exception("wrong sequence")
        
    except Exception as e:
        print("ERROR from post_sign : ", e)
        return JSONResponse(status_code=400, content={})
