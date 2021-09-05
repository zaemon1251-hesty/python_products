import responder
api = responder.API()

@api.route('/')
async def index(req, resp):
    resp.headers["Content-Type"] = "application/json; charset=UTF-8"
    resp.media = {"data": "サンプルデプロイ"}

if __name__ == '__main__':
    api.run()