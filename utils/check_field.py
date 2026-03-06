from hashlib import sha256
from functools import wraps
from flask import request as rq, jsonify, render_template
from jwt import decode
from datetime import datetime as dt
from utils.token import decode_token

def check_password_hash(pwd: str, hash: str) -> bool: # Confirma o hash do password
    if sha256(str(pwd).encode()).hexdigest() == hash: return True
    return False

def safe_route(func): # Rota responsavel pela verificação do Access Token
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = rq.cookies.get("access_token", False) # Obtem o token do Header
        if not access_token: return jsonify("Token de acesso obrigatorio"), 400 # Caso não encontre, retorna BAD REQUEST
        try: # Teste de token
            data = decode_token(access_token) # Obtem os dados do JWT Token depois dedescriptografar
            if  int(dt.now().timestamp()) >= data.get("exp"): return jsonify("Token expirado, refazer login!"), 401  # Confere se o mesmo não esta expirado
            kwargs["token_data"] = data # Adiciona os dados do token no Kwargs
            return func(*args, **kwargs) # Retorna a função e seus params
        except Exception as e: return jsonify("Token de acesso invalido"), 401 # Retorna invalido 401 UNAUTHORIZED
    return wrapper # Retorna o wrapper