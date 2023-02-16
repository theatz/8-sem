import asyncio
import aiohttp
import aiohttp_socks
import backoff

class AsyncHTTPConnector:
    def __init__(self, max_connections=10, timeout=30, proxy=None):
        self.session = None
        self.max_connections = max_connections
        self.timeout = timeout
        self.proxy = proxy

    async def __aenter__(self):
        connector_kwargs = {'limit': self.max_connections, 'limit_per_host': self.max_connections, 'force_close': True, 'enable_cleanup_closed': True, 'ssl': False}
        if self.proxy:
            connector = aiohttp_socks.SocksConnector.from_url(self.proxy, **connector_kwargs)
        else:
            connector = aiohttp.TCPConnector(**connector_kwargs)
        self.session = aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=3)
    async def request(self, method, url, **kwargs):
        async with self.session.request(method, url, **kwargs) as response:
            response_text = await response.text()
            return response_text
