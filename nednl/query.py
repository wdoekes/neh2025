from typing import NamedTuple

from . import const
from .helpers import make_query


@make_query(api='activities')
class Activity(NamedTuple):
    pass


@make_query(api='classifications')
class Classification(NamedTuple):
    pass


@make_query(api='granularities')
class Granularity(NamedTuple):
    pass


@make_query(api='granularity_time_zones')
class GranularityTimeZone(NamedTuple):
    pass


@make_query(api='points')
class Point(NamedTuple):
    pass


@make_query(api='types')
class Type(NamedTuple):
    pass


@make_query(api='utilizations')
class Utilization(NamedTuple):
    point: int = const.Point.NEDERLAND
    type: int = const.Type.ALL
    granularity: int = const.Granularity.HOUR
    granularitytimezone: int = const.GranularityTimeZone.UTC
    classification: int = const.Classification.FORECAST
    activity: int = const.Activity.PROVIDING
    validfrom_after: str = None
    validfrom_before: str = None
    order_validfrom: str = 'asc'
