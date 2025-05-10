#!/usr/bin/env python3
import asyncio

from datetime import date, timedelta

import nednl.api
import nednl.const
import nednl.query

from settings import CACHE_DIR, NEDNL_API_KEY


async def print_nednl_const(api):
    import nednl.helpers

    print('"""')
    print('Source: https://ned.nl/nl/handleiding-api')
    print('"""')
    print('from .helpers import Const')
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
        api.set_cache_dir(CACHE_DIR)

        today = date.today()
        today_plus_1 = today + timedelta(days=1)

        if 0:
            await print_nednl_const(api)
        else:
            for type_ in (
                    nednl.const.Type.ALL,
                    nednl.const.Type.WIND,
                    nednl.const.Type.SOLAR,
                    nednl.const.Type.BIOGAS,
                    nednl.const.Type.HEATPUMP,
                    nednl.const.Type.AIRHEATPUMP,
                    nednl.const.Type.HYBRIDHEATPUMP,
                    nednl.const.Type.GROUNDHEATPUMP,
                    nednl.const.Type.COFIRING,
                    nednl.const.Type.GEOTHERMAL,
                    nednl.const.Type.OTHER,
                    nednl.const.Type.WASTE,
                    nednl.const.Type.BIOOIL,
                    nednl.const.Type.BIOMASS,
                    nednl.const.Type.WOOD,
                    nednl.const.Type.WOODACTIVEHEATING,
                    nednl.const.Type.WOODCOMFORTHEATING,
                    nednl.const.Type.WINDOFFSHORE,
                    nednl.const.Type.FOSSILGASPOWER,
                    nednl.const.Type.FOSSILHARDCOAL,
                    nednl.const.Type.NUCLEAR,
                    nednl.const.Type.WASTEPOWER,
                    nednl.const.Type.WINDOFFSHOREB,
                    nednl.const.Type.NATURALGAS,
                    nednl.const.Type.BIOMETHANE,
                    nednl.const.Type.BIOMASSPOWER,
                    nednl.const.Type.OTHERPOWER,
                    nednl.const.Type.ELECTRICITYMIX,
                    nednl.const.Type.GASMIX,
                    nednl.const.Type.GASPRIVATEDISTRIBUTIONCOMPANIES,
                    nednl.const.Type.GASDISTRIBUTION,
                    nednl.const.Type.WKK_TOTAL,
                    nednl.const.Type.SOLARTHERMAL,
                    nednl.const.Type.WINDOFFSHOREC,
                    nednl.const.Type.INDUSTRIALCONSUMERSGASCOMBINATION,
                    nednl.const.Type.INDUSTRIALCONSUMERSPOWERGASCOMBINATION,
                    nednl.const.Type.LOCALDISTRIBUTIONCOMPANIESCOMBINATION,
                    nednl.const.Type.ALLCONSUMINGGAS,
                    ):
                print()
                print(type_)
                query = nednl.query.Utilization(
                    # activity=nednl.const.Activity.CONSUMING,
                    type=type_,
                    validfrom_after=today,
                    validfrom_before=today_plus_1,
                )
                utilizations = await query.list(api)
                for utilization in utilizations.values:
                    print(utilization)


if __name__ == '__main__':
    asyncio.run(main())
