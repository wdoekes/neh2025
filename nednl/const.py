"""
Source: https://ned.nl/nl/handleiding-api
"""
from enum import Enum


class PrettyEnum(Enum):
    def __new__(cls, value, label):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

    def __str__(self):
        return self.label


class Activity(PrettyEnum):
    """
    /Geeft het activiteitstype aan: opwek (providing) of consumptie (consuming)/
    """
    PROVIDING = (1, 'Providing')
    CONSUMING = (2, 'Consuming')
    IMPORT = (3, 'Import')
    EXPORT = (4, 'Export')
    STORAGE_IN = (5, 'Storage in')
    STORAGE_OUT = (6, 'Storage out')
    STORAGE = (7, 'Storage')


class Granularity(PrettyEnum):
    """
    /De data is gegroepeerd op een bepaalde granulariteit of
    tijdsinterval. Hiernaast zie je de beschikbare tijdsintervallen./
    """
    _10_MINUTES = (3, '10 minutes')
    _15_MINUTES = (4, '15 minutes')
    HOUR = (5, 'Hour')
    DAY = (6, 'Day')
    MONTH = (7, 'Month')
    YEAR = (8, 'Year')


class Point(PrettyEnum):
    """
    /Over welke geografische gebied moet de data gaan?/
    """
    NEDERLAND = (0, 'Nederland')  
    GRONINGEN = (1, 'Groningen')
    FRIESLAND = (2, 'Friesland')
    DRENTHE = (3, 'Drenthe')
    OVERIJSSEL = (4, 'Overijssel')
    FLEVOLAND = (5, 'Flevoland')
    GELDERLAND = (6, 'Gelderland')
    UTRECHT = (7, 'Utrecht')
    NOORD_HOLLAND = (8, 'Noord-Holland')
    ZUID_HOLLAND = (9, 'Zuid-Holland')
    ZEELAND = (10, 'Zeeland')
    NOORD_BRABANT = (11, 'Noord-Brabant')
    LIMBURG = (12, 'Limburg')
    OFFSHORE = (14, 'Offshore')
    WINDPARK_LUCHTERDUINEN = (28, 'Windpark Luchterduinen')
    WINDPARK_PRINCES_AMALIA = (29, 'Windpark Princes Amalia')
    WINDPARK_EGMOND_AAN_ZEE = (30, 'Windpark Egmond aan Zee')
    WINDPARK_GEMINI = (31, 'Windpark Gemini')
    WINDPARK_BORSELLE_I_II = (33, 'Windpark Borselle I&II')
    WINDPARK_BORSELLE_III_IV = (34, 'Windpark Borselle III&IV')
    WINDPARK_HOLLANDSE_KUST_ZUID = (35, 'Windpark Hollandse Kust Zuid')
    WINDPARK_HOLLANDSE_KUST_NOORD = (36, 'Windpark Hollandse Kust Noord')


class Type(PrettyEnum):
    ALL = (0, 'All')
    WIND = (1, 'Wind')
    SOLAR = (2, 'Solar')
    BIOGAS = (3, 'Biogas')
    HEATPUMP = (4, 'HeatPump')
    COFIRING = (8, 'Cofiring')
    GEOTHERMAL = (9, 'Geothermal')
    OTHER = (10, 'Other')
    WASTE = (11, 'Waste')
    BIOOIL = (12, 'BioOil')
    BIOMASS = (13, 'Biomass')
    WOOD = (14, 'Wood')
    WINDOFFSHORE = (17, 'WindOffshore')
    FOSSILGASPOWER = (18, 'FossilGasPower')
    FOSSILHARDCOAL = (19, 'FossilHardCoal')
    NUCLEAR = (20, 'Nuclear')
    WASTEPOWER = (21, 'WastePower')
    WINDOFFSHOREB = (22, 'WindOffshoreB')
    NATURALGAS = (23, 'NaturalGas')
    BIOMETHANE = (24, 'Biomethane')
    BIOMASSPOWER = (25, 'BiomassPower')
    OTHERPOWER = (26, 'OtherPower')
    ELECTRICITYMIX = (27, 'ElectricityMix')
    GASMIX = (28, 'GasMix')
    GASDISTRIBUTION = (31, 'GasDistribution')
    WKK_TOTAL = (35, 'WKK Total')
    SOLARTHERMAL = (50, 'SolarThermal')
    WINDOFFSHOREC = (51, 'WindOffshoreC')
    INDUSTRIALCONSUMERSGASCOMBINATION = (53, 'IndustrialConsumersGasCombination')
    INDUSTRIALCONSUMERSPOWERGASCOMBINATION = (54, 'IndustrialConsumersPowerGasCombination')
    LOCALDISTRIBUTIONCOMPANIESCOMBINATION = (55, 'LocalDistributionCompaniesCombination')
    ALLCONSUMINGGAS = (56, 'AllConsumingGas')
