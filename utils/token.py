from jwt import encode, decode
from dateutils import relativedelta
from os import getenv
from datetime import datetime

def create_token(dados:dict):
    dados["exp"] = datetime.now() + relativedelta(hours=8)
    token = str(encode(dados, getenv("SECRET"), algorithm="HS256"))
    return token

def decode_token(token:str):
    try:
        data = decode(token, getenv("SECRET"), algorithms=["HS256"])
        return data
    except Exception as e:
        print(e)
        return None