from collections import namedtuple
from datetime import datetime, timezone


class Utilization(namedtuple(
        'Utilization',
        'capacity volume percentage emission emissionfactor datetime period')):
    # - capacity (kWh)
    # - volume (kWh)
    # - emission (kg)
    # - emissionfactor (kg/KWh)
    #
    # For forecast, we've seen capacity and volume be equal for nuclear,
    # solar and wind.
    #
    # For a test, we see that nednl.const.Type.NUCLEAR expected
    # production (capacity, or volume) equals 485000 kWh for an
    # hour. That corresponds to:
    # 485_000 (kWh) * 24 * 365 = 4_248_600 MWh
    # That corresponds to "[in Borsele] wordt jaarlijks rond de
    # 3,8 miljoen MWh (megawattuur) gemaakt".
    pass


class Utilizations:
    @classmethod
    def from_response(cls, response):
        """
        De actuele opwek van elektriciteit en de afzet van gas in
        Nederland. Het totaal en uitgesplitst naar energiedrager.

        Week vooruit voorspelling van zonne-energie, windenergie op
        land, windenergie op zee, gasconsumptie van huishoudens en
        kleine bedrijven. Voor zonne-energie en windenergie op land is
        er ook een uitsplitsing naar provincies mogelijk; bij
        windenergie op zee is een uitsplitsing naar losse windparken op
        zee.

        De opwek in capaciteit (kW), productievolumes in kWh,
        CO₂-emissies in kg en CO₂-emissiefactoren in kg/KWh.

        Historische data beschikbaar; bij sommige energiedragers wel zo
        vroeg als januari 2016.

        10 minuten, kwartier, uur, dag, maand en jaar waarden.
        """
        count = response['hydra:totalItems']
        values = []
        for value in response['hydra:member']:
            begin = datetime.strptime(
                value['validfrom'],
                '%Y-%m-%dT%H:%M:%S+00:00').replace(tzinfo=timezone.utc)
            end = datetime.strptime(
                value['validto'],
                '%Y-%m-%dT%H:%M:%S+00:00').replace(tzinfo=timezone.utc)

            values.append(Utilization(
                capacity=value['capacity'],
                volume=value['volume'],
                percentage=value['percentage'],
                emission=value['emission'],
                emissionfactor=value['emissionfactor'],
                datetime=begin,
                period=(end - begin)))
        assert len(values) == count, (len(values), count)
        return cls(values)

    def __init__(self, values):
        self.values = values
