from routes import clients_routes, members_routes, login_routes

# DICT FOR NAME AND BP
bps = {
    "/clientes": clients_routes.clients_bp,
    "/membros": members_routes.member_bp,
    "/config/login": login_routes.login_bp,
}