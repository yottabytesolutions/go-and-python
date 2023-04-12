import asyncio

import aiohttp
from aiohttp import web
from aiohttp_remotes import setup as setup_remotes
from aiohttp_remotes import XForwardedRelaxed

SERVICE_ONE_URL = "http://upstream_service_one_python:8080/info"
SERVICE_TWO_URL = "http://upstream_service_two_python:8080/info"


class HttpException(Exception):
    pass


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            raise HttpException(f"Error {response.status}: {await response.text()}")
        return await response.json()


async def fetch_with_retry(session, url, retries=2, backoff_factor=2):
    for i in range(retries + 1):
        try:
            return await fetch(session, url)
        except Exception as e:
            if i < retries:
                await asyncio.sleep(backoff_factor ** i)
            else:
                return {"error": str(e)}


async def hello(request):
    name = request.match_info.get('name', "World")
    response = {"hello": name}
    upstream_responses = []

    async with aiohttp.ClientSession() as session:
        urls = [SERVICE_ONE_URL, SERVICE_TWO_URL]

        tasks = [fetch_with_retry(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for result in results:
            upstream_responses.append(result)

    response.update({"upstream_responses": upstream_responses})
    return web.json_response(response)


async def health(ignored):
    return web.json_response({"status": "OK"})


app = web.Application()
app.router.add_get('/{name}', hello)
app.router.add_get('/health', health)


async def init_app(application):
    await setup_remotes(
        application,
        XForwardedRelaxed(num=1)  # Rate limiting: 100 requests per 60 seconds
    )

    # Alternatively, use XForwardedStrict if you want to enforce the presence of X-Forwarded-* headers.
    # setup_remotes(app, XForwardedStrict(rate=100, period=60))
    application['config'] = {'rate_limit': 100}


if __name__ == '__main__':
    asyncio.run(init_app(app))
    web.run_app(app, host='0.0.0.0', port=8123)
