from datetime import date
from typing import NamedTuple

from . import const


class UtilizationQuery(NamedTuple):
    point: int = const.Point.NEDERLAND
    type: int = const.Type.ALL.value
    granularity: int = const.Granularity.HOUR
    granularitytimezone: int = 0  # FIXME: 0=UTC
    classification: int = 1       # FIXME: 1=forecast
    activity: int = const.Activity.PROVIDING
    validfrom_after: str = None
    validfrom_before: str = None
    order_validfrom: int = 'asc'

    def marshall(self, value):
        if isinstance(value, str):
            return value
        if isinstance(value, int):
            return str(value)
        if isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        if isinstance(value, const.PrettyEnum):
            return str(value.value)
        raise NotImplementedError((type(value), value))

    async def exec(self, api):
        params = {}
        for field in self._fields:
            if '_' in field:
                key = '{}[{}]'.format(*field.split('_', 1))
            else:
                key = field
            params[key] = self.marshall(getattr(self, field))

        return await api.call('GET', 'utilizations', params=params)
