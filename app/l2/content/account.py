# content/account.py

# lib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# schema


# definition
async def read_account_by_email(email:str, ss:AsyncSession):
    resp = await ss.execute(
        statement=text("SELECT * FROM account WHERE email_=:a"),
        params={"a":email}
    )
    return resp.mappings().fetchone()


async def create_account(email_:str, hashed_password_:str, ss:AsyncSession):
    try:
        await ss.execute(
            statement=text("INSERT INTO account(role_, email_, hashed_password_) VALUES(:a, :b, :c);"),
            params={"a":"user", "b":email_, "c":hashed_password_}
        )
        return True
    except Exception as e:
        print("ERROR from create_account : ", e)
        return None
    

async def read_account_by_id(id_:int, ss:AsyncSession):
    try:
        resp = await ss.execute(
            statement=text("SELECT * FROM account WHERE id_=:a;"),
            params={"a":id_}
        )
        respData = resp.mappings().fetchone()
        return respData
    except Exception as e:
        print("ERROR from read_account_by_id : ", e)
        return None