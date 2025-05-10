import aiohttp
import re

from json import dump, load
from os.path import join as pathjoin
from urllib.parse import urljoin


class Api:
    @classmethod
    def with_api_key(cls, api_key):
        return cls(api_key)

    def __init__(self, api_key):
        self._base_url = 'https://api.ned.nl/v1/'  # *with* slash!
        self._cache_dir = None
        self._illegal_char_re = re.compile(r'[^A-Za-z0-9_=-]')
        self._sess = aiohttp.ClientSession()
        self._headers = {
            'Accept': 'application/ld+json',
            'X-AUTH-TOKEN': api_key,
        }

    def set_cache_dir(self, cache_dir):
        self._cache_dir = cache_dir

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        await self._sess.close()

    async def call(self, method, path, params=None):
        """
        TODO: Move this cache wrapper to a mixin. It does not belong in
        this class.
        """
        if method == 'GET' and self._cache_dir:
            cache_params = '-'.join(f'{k}={v}' for k, v in params.items())
            cache_key = f'{method}-{path}-{cache_params}'
            cache_filename = pathjoin(
                self._cache_dir,
                self._illegal_char_re.sub('-', cache_key) + '.cache')
        else:
            cache_filename = None

        if cache_filename:
            try:
                with open(cache_filename, 'r') as fp:
                    response = load(fp)
            except FileNotFoundError:
                pass
            else:
                return response

        response = await self.force_call(method, path, params=params)

        if cache_filename:
            with open(cache_filename, 'w') as fp:
                dump(response, fp, indent=2)

        return response

    async def force_call(self, method, path, params=None):
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
