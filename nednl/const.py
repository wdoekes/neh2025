"""
Source: https://ned.nl/nl/handleiding-api
"""
from .helpers import Const


class Activity(Const):
    """
    /Geeft het activiteitstype aan: opwek (providing) of consumptie (consuming)/
    """
    PROVIDING = (1, 'Providing')
    CONSUMING = (2, 'Consuming')
    IMPORT = (3, 'Import')
    EXPORT = (4, 'Export')
    STORAGE_IN = (5, 'Storage In')
    STORAGE_OUT = (6, 'Storage Out')
    STORAGE = (7, 'Storage')


class Classification(Const):
    """
    /Geeft het Classificatietype aan. (Bijv. Near-realtime of Voorspelling)/
    """
    FORECAST = (1, 'Forecast')
    CURRENT = (2, 'Current')
    BACKCAST = (3, 'Backcast')


class Granularity(Const):
    """
    /De data is gegroepeerd op een bepaalde granulariteit of
    tijdsinterval. Hiernaast zie je de beschikbare tijdsintervallen./
    """
    _1MIN = (1, '1Min')     # from API only
    _5MIN = (2, '5Min')     # from API only
    _10MIN = (3, '10Min')
    _15MIN = (4, '15Min')
    HOUR = (5, 'Hour')
    DAY = (6, 'Day')
    MONTH = (7, 'Month')
    YEAR = (8, 'Year')


class GranularityTimeZone(Const):
    """
    /Elke granulariteit is geldig voor een bepaalde tijdzone, dit
    gegevensrecord bevat de naam van deze tijdzone./

    Note that the docs say CET, which is wrong. Europe/Amsterdam is
    probably right, but you might want to stick with UTC for sanity.
    """
    UTC = (0, 'UTC')
    EUROPE_AMSTERDAM = (1, 'Europe/Amsterdam')


class Point(Const):
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
    EILANDEN = (13, 'Eilanden')                 # from API only
    OFFSHORE = (14, 'Offshore')
    FCNEDERLAND = (15, 'FCNederland')           # from API only
    FCGRONINGEN = (16, 'FCGroningen')           # from API only
    FCFRIESLAND = (17, 'FCFriesland')           # from API only
    FCDRENTHE = (18, 'FCDrenthe')               # from API only
    FCOVERIJSSEL = (19, 'FCOverijssel')         # from API only
    FCFLEVOLAND = (20, 'FCFlevoland')           # from API only
    FCGELDERLAND = (21, 'FCGelderland')         # from API only
    FCUTRECHT = (22, 'FCUtrecht')               # from API only
    FCNOORD_HOLLAND = (23, 'FCNoord-Holland')   # from API only
    FCZUID_HOLLAND = (24, 'FCZuid-Holland')     # from API only
    FCZEELAND = (25, 'FCZeeland')               # from API only
    FCNOORD_BRABANT = (26, 'FCNoord-Brabant')   # from API only
    FCLIMBURG = (27, 'FCLimburg')               # from API only
    WINDPARK_LUCHTERDUINEN = (28, 'Windpark Luchterduinen')
    WINDPARK_PRINCES_AMALIA = (29, 'Windpark Princes Amalia')
    WINDPARK_EGMOND_AAN_ZEE = (30, 'Windpark Egmond aan Zee')               # from DOCS only
    WINDPARK_GEMINI = (31, 'Windpark Gemini')                               # from DOCS only
    WINDPARK_BORSELLE_I_II = (33, 'Windpark Borselle I&II')                 # from DOCS only
    WINDPARK_BORSELLE_III_IV = (34, 'Windpark Borselle III&IV')             # from DOCS only
    WINDPARK_HOLLANDSE_KUST_ZUID = (35, 'Windpark Hollandse Kust Zuid')     # from DOCS only
    WINDPARK_HOLLANDSE_KUST_NOORD = (36, 'Windpark Hollandse Kust Noord')   # from DOCS only


class Type(Const):
    """
    /Wat is het type energiedrager?/
    """
    ALL = (0, 'All')
    WIND = (1, 'Wind')
    SOLAR = (2, 'Solar')
    BIOGAS = (3, 'Biogas')
    HEATPUMP = (4, 'HeatPump')
    AIRHEATPUMP = (5, 'AirHeatPump')            # from API only
    HYBRIDHEATPUMP = (6, 'HybridHeatPump')      # from API only
    GROUNDHEATPUMP = (7, 'GroundHeatPump')      # from API only
    COFIRING = (8, 'Cofiring')
    GEOTHERMAL = (9, 'Geothermal')
    OTHER = (10, 'Other')
    WASTE = (11, 'Waste')
    BIOOIL = (12, 'BioOil')
    BIOMASS = (13, 'Biomass')
    WOOD = (14, 'Wood')
    WOODACTIVEHEATING = (15, 'WoodActiveHeating')       # from API only
    WOODCOMFORTHEATING = (16, 'WoodComfortHeating')     # from API only
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
    GASPRIVATEDISTRIBUTIONCOMPANIES = (29, 'GasPrivateDistributionCompanies')       # from API only
    GASDISTRIBUTION = (31, 'GasDistribution')                                       # from DOCS only
    WKK_TOTAL = (35, 'WKK Total')                                                   # from DOCS only
    SOLARTHERMAL = (50, 'SolarThermal')                                             # from DOCS only
    WINDOFFSHOREC = (51, 'WindOffshoreC')                                           # from DOCS only
    INDUSTRIALCONSUMERSGASCOMBINATION = (53, 'IndustrialConsumersGasCombination')   # from DOCS only
    INDUSTRIALCONSUMERSPOWERGASCOMBINATION = (54, 'IndustrialConsumersPowerGasCombination')     # from DOCS only
    LOCALDISTRIBUTIONCOMPANIESCOMBINATION = (55, 'LocalDistributionCompaniesCombination')       # from DOCS only
    ALLCONSUMINGGAS = (56, 'AllConsumingGas')                                       # from DOCS only
