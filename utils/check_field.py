from hashlib import sha256
from functools import wraps
from flask import request, jsonify
from jwt import decode
from datetime import datetime as dt

def check_password_hash(pwd: str, hash: str) -> bool: # Confirma o hash do password
    if sha256(str(pwd).encode()).hexdigest() == hash: return True
    return False

def safe_route(func): # Rota responsavel pela verificação do Access Token
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get("Access-Token", False) # Obtem o token do Header
        if not access_token: return jsonify("Token de acesso obrigatório"), 400 # Caso não encontre, retorna BAD REQUEST
        try: # Teste de token
            data = decode(access_token, "secret", algorithms=["HS256"]) # Obtem os dados do JWT Token depois dedescriptografar
            if  int(dt.now().timestamp()) >= data.get("exp"): return jsonify("Token expirado, refazer login!"), 401  # Confere se o mesmo não esta expirado
            return func(*args, **kwargs) # Retorna a função e seus params
        except Exception as e: return jsonify("Token de acesso inválido"), 401 # Retorna invalido 401 UNAUTHORIZED
    return wrapper # Retorna o wrapper