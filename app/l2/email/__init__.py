# email/__init__.py

# lib
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import os
from random import randint

# module
from .email_client import *

# definition



CONFIG = {}
CLIENTS:dict[str,EmailClient] = {}
TEMPLATE = Jinja2Templates( directory=os.path.join( os.path.dirname(__file__), "form" ) )

def setup(config:dict):
    global CONFIG, CLIENTS
    CONFIG = config

    # email 클라잉언트 생성
    for k, v in CONFIG.items():
        CLIENTS[k]=EmailClient(**v)


async def send_code_for_time(req:Request, email_:str):
    try:
        code_=randint(10000, 99999)

        html = TEMPLATE.TemplateResponse(
            name="sign_form.html",
            request=req,
            context={
                "verification_code":code_
            },
            status_code=200
        )

        resp = await CLIENTS["gamemaster"].send_email(
            to=email_,
            subject="verification code is arrived from Brightest Dungeon",
            subtype="html",
            body=html.body.decode("utf-8")
        )
        if resp:
            return code_
        else:
            raise Exception("send_mail error")
        
    except Exception as e:
        print("ERROR from send_code_for_time : ", e)
        return None

