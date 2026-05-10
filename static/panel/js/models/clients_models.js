import { ApiRequest } from "../utils/request.js"

export class Client{
    async get(id=null){
        const req = await new ApiRequest("/clientes")
        return req.send()
    };

    async create(name, domain, template=null){
        const data = { name: name, subdomain: domain };
        template ? data["template"] = template : null;
        const req = await new ApiRequest("/clientes", "POST", data)
        return req.send()
    };

    async update(client_id, type, value, msg=null){
        const data = { id: client_id, type: type, value: value, msg:msg}
        const req = await new ApiRequest("/clientes", "PATCH", data)
        return req.send()
    };

    async remove(client_id){
        const req = await new ApiRequest(`/clientes?id=${client_id}`, "DELETE")
        return req.send()
    };
};