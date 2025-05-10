#!/usr/bin/env python3
import asyncio

from datetime import date, timedelta
from json import dumps

import nednl
from settings import NEDNL_API_KEY


async def main():
    async with nednl.Api.with_api_key(NEDNL_API_KEY) as api:
        today = date.today()
        today_plus_1 = today + timedelta(days=1)

        query = nednl.UtilizationQuery(
            type=nednl.Type.SOLAR,
            validfrom_after=today,
            validfrom_before=today_plus_1,
        )
        resp = await query.exec(api)
        print(dumps(resp))


if __name__ == '__main__':
    asyncio.run(main())
