from flask import request as rq, jsonify
from models.members import Member
from utils.check_field import check_password_hash
from utils.token import create_token

class LoginService:
    def login(self): # Realiza o login devolvendo um token
        dados = rq.get_json() # Obtem o JSON 
        email = dados.get("email", False) # Obtem o email default FALSe
        pwd = dados.get("password", False) # Obtem a senha, default FALSE
        if email: # Confirma se foi passado o emial
            if pwd: # Confirma se foi passado a senha
                member = Member._search_by_email(email) # Obtem o user do banco de dados (Filter by email)
                if member: # Checka se o user existe
                    if member.active: # Checka se o user esta ativo
                        if check_password_hash(pwd, member.hash): # Checka o HASH da Senha 
                            token = create_token({ "member_id": member.id, "partnership_id": member.partnership_id, "client_id": member.client_id }) # Cria o access token
                            return {
                                "access_token": token,
                                "display_name": member.name,
                                "email": member.email,
                                "last_login": member.last_login
                            }, 200 # Cria o token e retorna os dados do usuário
                        return jsonify("Senha incorreta"), 401 # Retorna a senha incorreta 401, UNAUTHORIZED
                    return jsonify("Usuário inativo, entrar em contato com sua parceria!"), 401 # usuário inativo 401, UNAUTHORIZES
                return jsonify("Email não encontrado"), 404 # User/Email nao encontrado 404, NOT FOUND
            return jsonify("Senha obrigatoria"), 400 # Senha obrigatoria 400, BAD REQUEST
        return jsonify("Email obrigatoria"), 400 # Email obrigatoria 400, BAD REQUEST
