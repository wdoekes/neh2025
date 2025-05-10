from datetime import date
from enum import Enum


class Const(Enum):
    """
    Create a constant like Point.GRONINGEN and Point.NEDERLAND.
    """
    def __new__(cls, value, label):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

    def __str__(self):
        return self.label


def _hydra_members_to_python_const(response):
    """
    Hackery to auto-generate const.py.
    """
    from re import compile

    non_alnum = compile(r'[^A-Za-z0-9]+')

    def as_key(value):
        """Turn '12 Abc--def' into '_12_ABC_DEF'"""
        value = non_alnum.sub('_', value.strip())
        if not value or value[0].isdigit():
            value = f'_{value}'
        return value.upper()

    def as_value(value):
        return value.strip().replace('\\', '').replace("'", '')

    # "@context": "/v1/contexts/Activity"
    name = response['@context'].rsplit('/', 1)[-1]
    values = []
    for member in response['hydra:member']:
        values.append((
            member['id'],
            as_key(member['name']),
            as_value(member['name'])))

    # Turn the results into constants below.
    ret = [
        f'class {name}(Const):', '    """', '    ...docs...', '    """']
    for id_, key, label in values:
        ret.append(f"    {key} = ({id_}, '{label}')")
    ret.extend(['', ''])
    return '\n'.join(ret)


def make_query(api):
    """
    Decorator to turn a NamedTuple into an API query visitor.

    Usage:

        @make_query(api='some_api_path')
        class SomeApi(NamedType):
            someid: int = 123
            some_withbrackets: str = 'default'

        query = SomeApi(someid=5)
        response = await query.exec(api)

    Will turn 'some_withbrackets' into 'some[withbrackets]'.
    """
    def wrapper(cls):
        def marshall(self, value):
            if isinstance(value, str):
                return value
            if isinstance(value, int):
                return str(value)
            if isinstance(value, date):
                return value.strftime('%Y-%m-%d')
            if isinstance(value, Const):
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

            return await api.call('GET', self.api, params=params)

        cls.api = api  # api path
        cls.marshall = marshall
        cls.exec = exec
        return cls

    return wrapper
