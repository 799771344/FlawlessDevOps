import asyncio
import httpx
import aiohttp
import requests

from common.log import logger


class AsyncAiohttp:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def request(self, method, url, headers=None, data=None, proxy_url=None, **kwargs):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        timeout = aiohttp.ClientTimeout(total=10)  # 总超时时间设置为10秒
        for attempt in range(4):  # 1 initial attempt + 3 retries
            try:
                async with self.session.request(method=method, url=url, headers=headers, data=data, proxy=proxy_url,
                                                timeout=timeout, **kwargs) as response:
                    response.raise_for_status()  # 会引发HTTP异常，如果状态码是4xx或5xx
                    bytes_data = await response.read()
                    return response.status, bytes_data
            except aiohttp.ClientResponseError as e:
                logger.error(f"Client response error: {e}")
                if e.status >= 500 and attempt < 3:  # 重试服务端错误
                    await asyncio.sleep(3 ** attempt)  # 指数退避策略
                else:
                    raise
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.error(f"Request failed: {e}")
                if attempt < 3:
                    await asyncio.sleep(3 ** attempt)  # 指数退避策略
                else:
                    raise
            except Exception as e:
                logger.critical(f"Unexpected error: {e}", exc_info=True)  # 记录堆栈信息
                raise

    async def get(self, url, headers=None, proxy_url=None, **kwargs):
        return await self.request("GET", url, headers=headers, proxy_url=proxy_url, **kwargs)

    async def post(self, url, headers=None, data=None, proxy_url=None, **kwargs):
        return await self.request("POST", url, headers=headers, data=data, proxy_url=proxy_url, **kwargs)


async_aiohttp = AsyncAiohttp()


class AsyncHttpx:

    async def request(self, method, url, headers=None, data=None, proxy_url=None, **kwargs):
        async with httpx.AsyncClient(proxies={"http": proxy_url, "https": proxy_url}) as client:
            response = await client.request(method=method, url=url, headers=headers, data=data, **kwargs)
            return response.status_code, response.text

    async def get(self, url, headers=None, proxy_url=None, **kwargs):
        async with httpx.AsyncClient(proxies={"http://": proxy_url, "https://": proxy_url}, verify=False,
                                     timeout=30) as client:
            response = await client.get(url=url, headers=headers, **kwargs)
            return response.status_code, response.text

    async def post(self, url, headers=None, data=None, proxy_url=None, **kwargs):
        async with httpx.AsyncClient(proxies={"http": proxy_url, "https": proxy_url}) as client:
            response = await client.post(url=url, headers=headers, data=data, **kwargs)
            return response.status_code, response.text


async_httpx = AsyncHttpx()


class AsyncRequests:
    async def _fetch(self, session, method, url, headers=None, data=None, proxy_url=None, **kwargs):
        proxies = None
        if proxy_url is not None:
            proxies = {"http": proxy_url, "https": proxy_url}
        with session.request(method=method, url=url, headers=headers, data=data, proxies=proxies, **kwargs) as response:
            return response.status_code, response.content.decode()

    async def request(self, method, url, headers=None, data=None, proxy_url=None, **kwargs):
        with requests.session() as session:
            status, response_text = await self._fetch(session, method, url, headers=headers, data=data,
                                                      proxy_url=proxy_url, **kwargs)
            return status, response_text

    async def get(self, url, headers=None, data=None, proxy_url=None, **kwargs):
        with requests.session() as session:
            status, response_text = await self._fetch(session, "GET", url, headers=headers, data=data,
                                                      proxy_url=proxy_url, **kwargs)
            return status, response_text

    async def post(self, url, headers=None, data=None, proxy_url=None, **kwargs):
        with requests.session() as session:
            status, response_text = await self._fetch(session, "POST", url, headers=headers, data=data,
                                                      proxy_url=proxy_url, **kwargs)
            return status, response_text


async_requests = AsyncRequests()
