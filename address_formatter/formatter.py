import operator
import re
from itertools import groupby
from typing import Optional, Union

__all__ = [
    'all_formats',
]

RE_POSESSIVE = re.compile(r"""
(^|\s)    # Совпадение если начало строки или пробелы, ссылается на \1
(им)       # Cсылается на \2
(?=\s|$)  # Совпадение если после "им" идут пробелы или конец строки
""", re.VERBOSE)
RE_SPACE_AFTER_DOT = re.compile(r"\.(?!\s)")
RE_NONDIGITS = re.compile(r"\D")
RE_NONLETTERS = re.compile(r"\W")

NBSPACE = '\u00A0'
NBHYPHEN = '\u2060-\u2060'
NBSLASH = '\u2060/\u2060'

IS_ERROR = object()


def unique_justseen(iterable, key=None):
    """Yields elements in order, ignoring serial duplicates

        >>> list(unique_justseen('AAAABBBCCDAABBB'))
        ['A', 'B', 'C', 'D', 'A', 'B']
        >>> list(unique_justseen('ABBCcAD', str.lower))
        ['A', 'B', 'C', 'A', 'D']

    """
    return map(next, map(operator.itemgetter(1), groupby(iterable, key)))


class AdjectiveSuffixSet:
    EMPTY = []
    MASCULINE = ["ый", "ий", "ой"]
    FEMININE = ["ая", "яя"]
    NEUTER = ["ое", "ее"]


class AddressComponent:
    REGION = "region"
    DISTRICT = "district"
    CITY = "city"
    TOWNSHIP = "township"
    VILLAGE = "village"
    STREET = "street"
    BUILDING = "building"
    SECTION = "section"
    CONSTRUCTION = "construction"
    OWNERSHIP = "ownership"


KEYS = {
    AddressComponent.REGION: {'value_key': 'region', 'type_key':
                              'region_type_full'},
    AddressComponent.DISTRICT: {'value_key': 'area',
                                'type_key': 'area_type_full'},
    AddressComponent.CITY: {'value_key': 'city', 'type_key': 'city_type_full'},
    AddressComponent.TOWNSHIP: {'value_key': 'city_district',
                                'type_key': 'city_district_type_full'},
    AddressComponent.VILLAGE: {'value_key': 'settlement',
                               'type_key': 'settlement_type_full'},
    AddressComponent.STREET: {'value_key': 'street',
                              'type_key': 'street_type_full'},
    AddressComponent.BUILDING: {'value_key': 'house',
                                'type_key': 'house_type_full'},
    AddressComponent.SECTION: {'value_key': 'section', 'type_key': None},
    AddressComponent.CONSTRUCTION: {'value_key': 'building',
                                    'type_key': None},
    AddressComponent.OWNERSHIP: {'value_key': None, 'type_key': None},
}

TYPES = {
    AddressComponent.REGION: {
        "город": {"suffix_set": AdjectiveSuffixSet.EMPTY, "abbreviation": "г"},
        "край": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                 "abbreviation": "кр"},
        "область": {"suffix_set": AdjectiveSuffixSet.FEMININE,
                    "abbreviation": "обл"},
        "республика": {"suffix_set": AdjectiveSuffixSet.FEMININE,
                       "abbreviation": "респ"}
    },

    AddressComponent.DISTRICT: {
        "город": {"suffix_set": AdjectiveSuffixSet.EMPTY, "abbreviation": "г"},
        "поселение": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                      "abbreviation": "пос"},
        "район": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                  "abbreviation": "р-н"}
    },

    AddressComponent.CITY: {
        "город": {"suffix_set": AdjectiveSuffixSet.EMPTY, "abbreviation": "г"},
        "сельское поселение": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                               "abbreviation": "с/п"}
    },

    AddressComponent.TOWNSHIP: {
        "округ": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                  "abbreviation": "окр"},
        "район": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                  "abbreviation": "р-н"}
    },

    AddressComponent.VILLAGE: {
        "гаражно-строительный кооп.": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                                       "abbreviation": "кооп"},
        "дачный поселок": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                           "abbreviation": "д/п"},
        "деревня": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                    "abbreviation": "д"},
        "квартал": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                    "abbreviation": "кв"},
        "микрорайон": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                       "abbreviation": "мкр"},
        "поселок": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                    "abbreviation": "п"},
        "рабочий поселок": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                            "abbreviation": "р/п"},
        "село": {"suffix_set": AdjectiveSuffixSet.EMPTY, "abbreviation": "с"},
        "станция": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                    "abbreviation": "ст"},
        "территория": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                       "abbreviation": "тер"},
        "хутор": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                  "abbreviation": "хут"}
    },

    AddressComponent.STREET: {
        "аллея": {"suffix_set": AdjectiveSuffixSet.FEMININE,
                  "abbreviation": "ал"},
        "бульвар": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                    "abbreviation": "б-р"},
        "городок": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                    "abbreviation": "гор"},
        "квартал": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                    "abbreviation": "кв"},
        "километр": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                     "abbreviation": "км"},
        "линия": {"suffix_set": AdjectiveSuffixSet.FEMININE,
                  "abbreviation": "лин"},
        "микрорайон": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                       "abbreviation": "мкр"},
        "набережная": {"suffix_set": AdjectiveSuffixSet.FEMININE,
                       "abbreviation": "наб"},
        "переулок": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                     "abbreviation": "пер"},
        "площадь": {"suffix_set": AdjectiveSuffixSet.FEMININE,
                    "abbreviation": "пл"},
        "поселок": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                    "abbreviation": "п"},
        "проезд": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                   "abbreviation": "пр"},
        "проспект": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                     "abbreviation": "просп"},
        "разъезд": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                    "abbreviation": "р-д"},
        "станция": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                    "abbreviation": "ст"},
        "территория": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                       "abbreviation": "тер"},
        "тракт": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                  "abbreviation": "тр"},
        "тупик": {"suffix_set": AdjectiveSuffixSet.MASCULINE,
                  "abbreviation": "туп"},
        "улица": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                  "abbreviation": "ул"},
        "шоссе": {"suffix_set": AdjectiveSuffixSet.NEUTER, "abbreviation": "ш"}
    },

    AddressComponent.BUILDING: {
        "дом": {"suffix_set": AdjectiveSuffixSet.EMPTY, "abbreviation": "д"}
    },

    AddressComponent.SECTION: {
        "корпус": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                   "abbreviation": "корп"}
    },

    AddressComponent.CONSTRUCTION: {
        "строение": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                     "abbreviation": "стр"}
    },

    AddressComponent.OWNERSHIP: {
        "квартира": {"suffix_set": AdjectiveSuffixSet.EMPTY,
                     "abbreviation": "кв"},
        "место": {"suffix_set": AdjectiveSuffixSet.EMPTY, "abbreviation": "м"}
    }
}


def posessive_dot(value: str) -> str:
    """ Добавляет точку к "им"
    проспект им Ленина -> проспект им. Ленина
    """
    return RE_POSESSIVE.sub(r'\1\2.', value)


def space_after_dot(value: str) -> str:
    return RE_SPACE_AFTER_DOT.sub('. ', value)


def dot_after_word(value: str) -> str:
    if value and not RE_NONLETTERS.search(value):
        return f'{value}.'

    return value


def check_numeral_suffix(word, suffix_set):
    numeral_suffix = next((
        suffix for suffix in suffix_set
        if word.endswith(f'-{suffix}') or word.endswith(f'-{suffix[-1]}')
    ), None)

    if numeral_suffix is not None:
        word_without_suffix = word[:-len(numeral_suffix) - 1]
        if not RE_NONDIGITS.search(word_without_suffix):
            return False

    return True


def check_start_with_type(value: str, suffix_set: list) -> bool:
    """ Стартовать ли порцию адреса с типа адреса
    Например:
        1-я квартира
        квартира 1
    """
    if not value:
        return False

    if not suffix_set:
        return True

    for word in value.split(' '):
        if not RE_NONDIGITS.search(word):
            continue

        if not check_numeral_suffix(word, suffix_set):
            continue

        # Конструкция найдет первый нужный элемент, либо вернет None
        suff = next((suff for suff in suffix_set if word.endswith(suff)), None)

        if suff is not None:
            continue

        return True

    return False


def check_portion(data: dict, address_component: str,
                  value: Optional[str] = None,
                  component_type: Optional[str] = None) \
        -> Union[str, None, 'IS_ERROR']:
    """Возвращает составные части адреса:
        str при нормальной обработке
        None если не пришел value, либо component_type
        IS_ERROR если пришел неожиданный component_type
    """
    # Целенаправленно поднимаем исключение если компонент на нашелся
    keys = KEYS[address_component]
    value_key = keys['value_key']
    type_key = keys['type_key']

    # берем value и component_type из data, либо из параметров функции
    if value_key is not None:
        value = data.get(value_key, value)

    if type_key is not None:
        component_type = data.get(type_key, component_type)

    if value is None or component_type is None:
        return None

    try:
        component_tuple = TYPES[address_component][component_type]
        abbreviation = component_tuple['abbreviation']
        suffix_set = component_tuple['suffix_set']
    except KeyError:
        return IS_ERROR

    value = posessive_dot(value)
    value = space_after_dot(value)
    abbreviation = dot_after_word(abbreviation)

    start_with_type = check_start_with_type(value, suffix_set)

    value = value.replace(". ", f'.{NBSPACE}').replace("-", NBHYPHEN) \
        .replace("/", NBSLASH)

    abbreviation = abbreviation.replace(" ", NBSPACE) \
        .replace("-", NBHYPHEN).replace("/", NBSLASH)

    return f"{abbreviation}{NBSPACE}{value}" if start_with_type \
        else f"{value}{NBSPACE}{abbreviation}"


def format_result(portions: list) -> str:
    """
    Если при обработке вернулся IS_ERROR возвращаем пустое значение
    Если при обработке вернулся None просто отфильтровываем его
    """
    if IS_ERROR in portions:
        return ""

    clean_porions = [portion for portion in portions if portion]

    return ", ".join(unique_justseen(clean_porions))


def all_formats(plain_address: str, address_components: Optional[dict],  # noqa
                premise_number: str = None, building_type: int = None):
    """ Address formatter on address components from housing building

    :param plain_address: default address if failed to build address
    :param address_components: dict of address_components
    :param premise_number: premise number
    :param building_type: type of building, 2 or 4 for garage or parking
    :return: dict of address formats
        all - full address with region, district, city, township, etc
        street_only - street or village
        finishing_with_village - region, district, city, township and village
        starting_with_street - street, building, section, construction, premise
        finishing_with_street - region, district, city,
            township, village, street

        >>> address_components = {
            "region": "Курганская", "region_type_full": "область",
            "area": "Катайский", "area_type_full": "район",
            "city": "Серов", "city_type_full": "город",
            "city_district": "Кировский", "city_district_type_full": "округ",
            "settlement": "Дрянное", "settlement_type_full": "село",
            "street": "Майская", "street_type_full": "улица",
            "house": "5", "house_type_full": "дом",
            "section": "6", "building": "7",
        }
        >>> all_formats("plain address ", address_components, "5", 7)['all']
        Курганская обл., Катайский р⁠-⁠н, г. Серов, Кировский окр.,
        с. Дрянное, ул. Майская, д. 5, корп. 6, стр. 7, м. 45
    """
    data = address_components

    if not data:
        return {
            'all': plain_address,
            'street_only': plain_address,
            'finishing_with_village': plain_address,
            'starting_with_street': plain_address,
            'finishing_with_street': plain_address,
        }

    section_type = "корпус"
    construction_type = "строение"
    # 2, 4 -> garage or parking
    ownership_type = "место" if building_type in [2, 4] else "квартира"

    region = check_portion(data, AddressComponent.REGION)
    district = check_portion(data, AddressComponent.DISTRICT)
    city = check_portion(data, AddressComponent.CITY)
    township = check_portion(data, AddressComponent.TOWNSHIP)
    village = check_portion(data, AddressComponent.VILLAGE)
    street = check_portion(data, AddressComponent.STREET)
    building = check_portion(data, AddressComponent.BUILDING)
    section = check_portion(data, AddressComponent.SECTION,
                            component_type=section_type)
    construction = check_portion(data, AddressComponent.CONSTRUCTION,
                                 component_type=construction_type)
    ownership = check_portion(data, AddressComponent.OWNERSHIP,
                              value=premise_number,
                              component_type=ownership_type)

    data_street = data.get('street')

    return {
        'all': format_result([
            region,
            district,
            city,
            township,
            village,
            street,
            building,
            section,
            construction,
            ownership,
        ]) or plain_address,
        'street_only': format_result([
            street if data_street is not None else village,
        ]) or plain_address,
        'finishing_with_village': format_result([
            region,
            district,
            city,
            township,
        ] + ([village] if data_street is not None else [])
        ) or plain_address,
        'starting_with_street': format_result(
            ([village] if data_street is None else []) + [
                street,
                building,
                section,
                construction,
                ownership,
            ]) or plain_address,
        'finishing_with_street': format_result([
            region,
            district,
            city,
            township,
            village,
            street,
        ]) or plain_address,
    }
