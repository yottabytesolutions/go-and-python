import random
import string

STRING_DIGITS = string.ascii_letters + string.digits

from aiohttp import web


async def info(request):
    if random.random() > 1:
        return "Internal Server Error", 500

    random_string = ''.join(random.choices(STRING_DIGITS, k=50))
    return web.json_response({"random_string": random_string})


app = web.Application()
app.router.add_get('/info', info)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
