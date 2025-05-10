#!/usr/bin/env python3
import asyncio

from datetime import date, timedelta
from json import dumps

import nednl.api
import nednl.const
import nednl.query

from settings import NEDNL_API_KEY


async def print_nednl_const(api):
    import nednl.helpers

    print('"""')
    print('Source: https://ned.nl/nl/handleiding-api')
    print('"""')
    print('from .helpers import PrettyEnum')
    for query in (
            nednl.query.Activity(),
            nednl.query.Classification(),
            nednl.query.Granularity(),
            nednl.query.GranularityTimeZone(),
            nednl.query.Point(),
            nednl.query.Type(),
            ):
        resp = await query.exec(api)
        print()
        print()
        print(nednl.helpers._hydra_members_to_python_const(resp).strip())


async def main():
    async with nednl.api.Api.with_api_key(NEDNL_API_KEY) as api:
        today = date.today()
        today_plus_1 = today + timedelta(days=1)

        if 0:
            await print_nednl_const(api)
        else:
            query = nednl.query.Utilization(
                type=nednl.const.Type.SOLAR,
                validfrom_after=today,
                validfrom_before=today_plus_1,
            )
            resp = await query.exec(api)
            print(dumps(resp))


if __name__ == '__main__':
    asyncio.run(main())
