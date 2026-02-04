from flask import request as rq, Blueprint
from services.member_service import ServiceMember

member_bp = Blueprint("Membros", __name__)
member_service = ServiceMember()

@member_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return member_service.read()
        case "POST": return member_service.create()
        case "PATCH": return member_service.update()
        case "DELETE": return member_service.delete()