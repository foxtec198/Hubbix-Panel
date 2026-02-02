from models.members import Member
from utils.db import db
from flask import jsonify, request as rq
from datetime import datetime as dt
from functools import cache

class ServiceMember:
    """
    =================================
    ====== SERVIÇO DE MEMBROS =======
    =================================

    ### CRUD Básico para funcionamento do painel:
    create - Cria um membro

    read - Obtém uma lista de membros ou dados do membro!

    update - Atualiza os dados do mebro de acordo com o ID
    
    delete - Remove um membro do BD

    """

    @cache
    def create(self) -> tuple:
        """
        ### Criação de Membros para o Painel
        _para mais duvidas veja o [Repositório do Hubbix Panel](https://github.com/foxtec198/Hubbix-panel)_

        :rtype: tuple
        :returns: MSG, 201 | MSG, 400
        """

        data = rq.form # Obtem o JSON da requisição
        new_member = Member() # Instancia o novo membro
        name = data.get("name") # Nome
        email = data.get("email") # Email Unico
        partnership = data.get("partnership_id") # ID da parceria
        if name and email and partnership:
            join_date = dt.now() # Data de criação (Agora)
            new_member.name = name # Insere o nome
            new_member.email = email # Insere o email 
            new_member.partnership_id = partnership # Insere o id de parceria
            new_member.join_date = join_date # Insere a data de criação
            db.session.add(new_member) # Adiciona o novo membro a sessão
            db.session.commit() # Comita os dados no BD
            return jsonify("Sucesso"), 201 # Retorna CREATED, 201
        return jsonify("Dados obrigatórios faltando!"), 400 # Retorna BAD REQUEST, 400

    @cache
    def read(self) -> tuple:
        """
        ### Obter membros do Painel
        _para mais duvidas veja o [Repositório do Hubbix Panel](https://github.com/foxtec198/Hubbix-panel)_

        :rtype: tuple
        :returns: member_data, 200 | MSG, 404
        """
        id = rq.args("id") # Obtem o ID do membro pela query  string
        if id: # Confirma se foi passado um ID
            member = Member._search_by_id(id) # Busca o membro no banco de dados
            if member: return jsonify(member.to_dict()), 200 # Confirma se encontrou o membro e retorna seus dados SUCCESS, 200
            return jsonify("Membro não encontrado!"), 404 # Retorna NOT FOUND, 404
        members = Member.query.all() # Obtem todos os membros
        members_list = [member.to_dict() for member in members] # Converte os membros para dicionário
        return jsonify(members_list), 200 # Retorna a lista de membros SUCCESS, 200
    
    @cache
    def update(self) -> tuple:
        """
        ### Atualização de Membros do Painel
        _para mais duvidas veja o [Repositório do Hubbix Panel](https://github.com/foxtec198/Hubbix-panel)_

        :rtype: tuple
        :returns: MSG, 200 | MSG, 400 | MSG, 404
        """

        data = rq.form # Obtem o JSON da requisição
        id = data.get("id") # Obtem o ID da request
        member = Member._search_by_id(id) # Busca o membro no banco de dados
        if member:
            # Obtem os dados para atualização
            name = data.get("name") 
            email = data.get("email")
            active = data.get("active")
            last_login = data.get("last_login")

            # Atualiza os dados conforme declarado
            member.name = name if name else ...
            member.email = email if email else ...
            member.active = active if active else ...
            member.last_login = last_login if last_login else ...

            db.session.commit() # Comita as mudanças no BD
            return jsonify("Membro atualizado com sucesso!"), 200 # Retorna SUCCESS, 200
        return jsonify("Membro não encontrado!"), 404 # Retorna NOT FOUND, 404

    @cache
    def delete(self) -> tuple:
        """
        ### Remoção de Membro do Painel por id
        _para mais duvidas veja o [Repositório do Hubbix Panel](https://github.com/foxtec198/Hubbix-panel)_

        :rtype: tuple
        :returns: MSG, 200 | MSG, 404         
        """
        id = rq.args.get("id") # Obtem o ID do membro pela query string
        member = Member._search_by_id(id) # Busca o membro no banco de dados
        if member:
            db.session.delete(member) # Deleta o membro da sessão
            db.session.commit() # Comita as mudanças no BD
            return jsonify("Membro deletado com sucesso!"), 200 # Retorna SUCCESS, 200
        return jsonify("Membro não encontrado!"), 404 # Retorna NOT FOUND, 404
    




        