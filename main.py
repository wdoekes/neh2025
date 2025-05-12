#!/usr/bin/env python3
import argparse
import asyncio

from datetime import date, timedelta

import nednl.api
import nednl.const
import nednl.helpers
import nednl.query

from settings import CACHE_DIR, NEDNL_API_KEY


async def generate_nednl_const_py(args):
    async with nednl.api.Api.with_api_key(NEDNL_API_KEY) as api:
        api.set_cache_dir(CACHE_DIR)
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


async def print_csv_test(args):
    async with nednl.api.Api.with_api_key(NEDNL_API_KEY) as api:
        api.set_cache_dir(CACHE_DIR)

        begin_date = date.today()  # + timedelta(days=2)
        end_date = begin_date + timedelta(days=1)

        collected = {}
        for type_ in (
                nednl.const.Type.ALL,
                nednl.const.Type.WIND,  # <- PROVIDING, interesting
                nednl.const.Type.SOLAR,  # <- PROVIDING, interesting
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
                nednl.const.Type.FOSSILGASPOWER,  # <- PROVIDING, interesting
                nednl.const.Type.FOSSILHARDCOAL,  # <- PROVIDING, interesting
                nednl.const.Type.NUCLEAR,  # <- PROVIDING, interesting
                nednl.const.Type.WASTEPOWER,  # <- PROVIDING, interesting
                nednl.const.Type.WINDOFFSHOREB,
                nednl.const.Type.NATURALGAS,
                nednl.const.Type.BIOMETHANE,
                nednl.const.Type.BIOMASSPOWER,  # <- PROVIDING, interesting
                nednl.const.Type.OTHERPOWER,  # <- PROVIDING, interesting
                nednl.const.Type.ELECTRICITYMIX,  # <- PROVIDING, unsure what to do with this
                nednl.const.Type.GASMIX,
                nednl.const.Type.GASPRIVATEDISTRIBUTIONCOMPANIES,
                nednl.const.Type.GASDISTRIBUTION,
                nednl.const.Type.WKK_TOTAL,  # <- PROVIDING, interesting
                nednl.const.Type.SOLARTHERMAL,
                nednl.const.Type.WINDOFFSHOREC,
                nednl.const.Type.INDUSTRIALCONSUMERSGASCOMBINATION,
                nednl.const.Type.INDUSTRIALCONSUMERSPOWERGASCOMBINATION,
                nednl.const.Type.LOCALDISTRIBUTIONCOMPANIESCOMBINATION,
                nednl.const.Type.ALLCONSUMINGGAS,
                nednl.const.Type.ELECTRICITYLOAD,  # <- PROVIDING, interesting
                ):
            query = nednl.query.Utilization(
                # activity=nednl.const.Activity.CONSUMING,
                # granularitytimezone=nednl.const.GranularityTimeZone.EUROPE_AMSTERDAM,
                type=type_,
                validfrom_after=begin_date,
                validfrom_before=end_date,
            )
            utilizations = await query.list(api)
            if utilizations.values:
                print(type_, len(utilizations), ' <--' if len(utilizations) != 24 else '')
                collected[type_.name] = utilizations

        print(','.join(collected.keys()))
        for row in zip(*[uts.values for uts in collected.values()]):
            print(','.join(f'{ut.volume}' for ut in row))


async def predict_next_week(args):
    async with nednl.api.Api.with_api_key(NEDNL_API_KEY) as api:
        api.set_cache_dir(CACHE_DIR)

        # Predictions of WIND/SOLAR exist up to a week.
        # Predictions of GAS are less far into the future (1 day and
        # maybe a bit more).
        #
        # I'm afraid we'll need to do some predicting based off the past.
        # But the predictions are (a) time-dependent, and (b)
        # environment (wind+solar) dependent, and as a bonus we have no
        # idea what "events" will do (holidays, sports events, DST
        # changes, etc.).
        #
        # We'll have to start with a sliding 48 hours perhaps?
        #
        # P.S. Also maybe print an "hour earlier", so that long running
        # tasks, like washing of clothes do not spill over into the next
        # hour which might be expensive (avondspits).
        begin_date = date.today() + timedelta(days=1)
        end_date = begin_date + timedelta(days=1)

        # "Good power" is power we want to promote use of.
        # We get 7 day predictions here.
        good_power = (
            nednl.const.Type.SOLAR,
            nednl.const.Type.WINDOFFSHORE,
            nednl.const.Type.WIND,
        )
        # "Stable power" is power that does not scale up/down, like nuclear.
        # (We still query it, in case it changes.)
        # We get 1 day predictions, but we can just copy them for a week.
        stable_power = (
            nednl.const.Type.NUCLEAR,
            nednl.const.Type.WASTEPOWER,
            nednl.const.Type.OTHERPOWER,
        )
        # "Scalable power" is power that we want to avoid, because it
        # includes gas/coal. Easiest to tune, but bad in terms of CO2
        # output.
        # Here we'll need to "invent" values.
        scalable_power = (
            nednl.const.Type.FOSSILGASPOWER,
            nednl.const.Type.FOSSILHARDCOAL,
            nednl.const.Type.BIOMASSPOWER,
            nednl.const.Type.WKK_TOTAL,
        )
        # Double check: this should be the sum of the previous power sources.
        check_power = (
            nednl.const.Type.ELECTRICITYMIX,
        )

        source_types = {
            'good_power': good_power,
            'stable_power': stable_power,
            'scalable_power': scalable_power,
            'check_power': check_power,
        }
        test = 0
        for name, types in source_types.items():
            for type_ in types:
                query = nednl.query.Utilization(
                    # activity=nednl.const.Activity.CONSUMING,
                    # granularitytimezone=nednl.const.GranularityTimeZone.EUROPE_AMSTERDAM,
                    classification=nednl.const.Classification.FORECAST,  # BACKCAST is empty?
                    type=type_,
                    validfrom_after=begin_date,
                    validfrom_before=end_date,
                )
                utilizations = await query.list(api)

                # Quick check that the number[0]s add up. They do, when all values exist.
                if name != 'check_power':
                    test += sum(i.volume for i in utilizations.values[0:24])
                else:
                    test -= sum(i.volume for i in utilizations.values[0:24])
                print(name, test, utilizations.values[0].datetime)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers()

    parser_generate_nednl_const_py = sub.add_parser('generate_nednl_const_py')
    parser_generate_nednl_const_py.set_defaults(afunc=generate_nednl_const_py)

    parser_print_csv_test = sub.add_parser('print_csv_test')
    parser_print_csv_test.set_defaults(afunc=print_csv_test)

    parser_predict_next_week = sub.add_parser('predict_next_week')
    parser_predict_next_week.set_defaults(afunc=predict_next_week)

    args = parser.parse_args()
    afunc = getattr(args, 'afunc', None)
    if not afunc:
        parser.print_usage()
        exit(1)

    asyncio.run(afunc(args))



if __name__ == '__main__':
    main()
