import aiohttp

from urllib.parse import urljoin


class Api:
    @classmethod
    def with_api_key(cls, api_key):
        return cls(api_key)

    def __init__(self, api_key):
        self._base_url = 'https://api.ned.nl/v1/'  # *with* slash!
        self._sess = aiohttp.ClientSession()
        self._headers = {
            'Accept': 'application/ld+json',
            'X-AUTH-TOKEN': api_key,
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        await self._sess.close()

    async def call(self, method, path, params=None):
        # request(self, method, url, params=None, data=None,
        #   headers=None, cookies=None, files=None, auth=None,
        #   timeout=None, allow_redirects=True, proxies=None, hooks=None,
        #   stream=None, verify=None, cert=None, json=None)
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with await session.request(
                    method=method,
                    url=urljoin(self._base_url, path),
                    params=params,
                    headers=self._headers,
                    timeout=30,
                    allow_redirects=False) as response:
                response.raise_for_status()
                return await response.json()
