import pytest

from address_formatter import all_formats
from address_formatter.formatter import (
    AddressComponent,
    AdjectiveSuffixSet,
    KEYS,
    TYPES,
    IS_ERROR,

    NBSPACE,
    NBHYPHEN,
    NBSLASH,

    posessive_dot,
    space_after_dot,
    dot_after_word,
    check_start_with_type,
    check_portion,
    format_result,
)


def components():
    return [(key, value) for key, value in AddressComponent.__dict__.items()
            if not key.startswith('__')]


@pytest.mark.parametrize("component", components())
def test_keys_class_protocol(component):
    _, component_key = component

    keys = KEYS.get(component_key)

    assert isinstance(keys, dict)
    assert 'value_key' in keys
    assert 'type_key' in keys


@pytest.mark.parametrize("component", components())
def test_types_class_protocol(component):
    _, component_key = component

    component_type = TYPES.get(component_key)

    assert isinstance(component_type, dict)

    for key, value in component_type.items():
        assert isinstance(key, str)

        assert 'suffix_set' in value
        assert 'abbreviation' in value

        assert value['suffix_set'] in AdjectiveSuffixSet.__dict__.values()
        assert value['abbreviation']


def test_posessive_dot():
    assert posessive_dot('') == ''
    assert posessive_dot('a') == 'a'

    assert posessive_dot('им') == 'им.'
    assert posessive_dot(' им') == ' им.'
    assert posessive_dot('им ') == 'им. '
    assert posessive_dot(' им ') == ' им. '

    assert posessive_dot('им 1') == 'им. 1'
    assert posessive_dot('1 им') == '1 им.'

    assert posessive_dot('1им 1') == '1им 1'
    assert posessive_dot('1 им1') == '1 им1'

    assert posessive_dot('  им  ') == '  им.  '


def test_space_after_dot():
    assert space_after_dot('') == ''
    assert space_after_dot('.') == '. '
    assert space_after_dot('a.') == 'a. '
    assert space_after_dot('.a') == '. a'
    assert space_after_dot('. ') == '. '
    assert space_after_dot('.  ') == '.  '


def test_dot_after_word():
    assert dot_after_word('') == ''
    assert dot_after_word('п') == 'п.'
    assert dot_after_word('п ') == 'п '


def test_check_start_with_type():
    assert check_start_with_type('', ['1']) is False
    assert check_start_with_type('', []) is False

    assert check_start_with_type('1', []) is True
    assert check_start_with_type('a', []) is True
    assert check_start_with_type('a', ['1']) is True
    assert check_start_with_type('1123123', ['ая']) is False

    assert check_start_with_type('a', ['a']) is False
    assert check_start_with_type('aя', ['я']) is False

    assert check_start_with_type('пая', ['ая']) is False
    assert check_start_with_type('п-ая', ['ая']) is False
    assert check_start_with_type('1-ая', ['ая']) is False
    assert check_start_with_type('первая', ['ая']) is False

    assert check_start_with_type('z-я', ['ая']) is False
    assert check_start_with_type('1-я', ['ая']) is False

    assert check_start_with_type('пр 1-я', ['ая']) is True
    assert check_start_with_type('пр 1-ая', ['ая']) is True
    assert check_start_with_type('1-ый пр.', ['ый']) is True

    assert check_start_with_type('первая вторая', ['ая']) is False


def test_check_portion_incorrect_args():
    with pytest.raises(KeyError):
        check_portion({}, 'foo')

    assert check_portion({}, AddressComponent.REGION) is None
    assert check_portion({}, AddressComponent.REGION, value='foo') is None
    assert check_portion({}, AddressComponent.REGION,
                         component_type='foo') is None
    assert check_portion({}, AddressComponent.REGION, 'foo', 'bar') is IS_ERROR


def test_check_portion_default_values():
    assert check_portion({
        'region': 'свердловская',
        'region_type_full': 'область',
    }, AddressComponent.REGION) == f'свердловская{NBSPACE}обл.'

    assert check_portion(
        {'region_type_full': 'область'},
        AddressComponent.REGION,
        value='свердловская'
    ) == f'свердловская{NBSPACE}обл.'

    assert check_portion(
        {'region': 'свердловская'},
        AddressComponent.REGION,
        component_type='область',
    ) == f'свердловская{NBSPACE}обл.'

    assert check_portion(
        {},
        AddressComponent.REGION,
        value='свердловская',
        component_type='область',
    ) == f'свердловская{NBSPACE}обл.'


def test_check_portion_replace_values():
    assert check_portion({
        'settlement': 'им Ленина',
        'settlement_type_full': 'поселок',
    }, AddressComponent.VILLAGE) == f'п.{NBSPACE}им.{NBSPACE}Ленина'

    assert check_portion({
        'settlement': 'им.Ленина',
        'settlement_type_full': 'поселок',
    }, AddressComponent.VILLAGE) == f'п.{NBSPACE}им.{NBSPACE}Ленина'

    assert check_portion({
        'street': 'Ленинский',
        'street_type_full': 'бульвар',
    }, AddressComponent.STREET) == f'Ленинский{NBSPACE}б{NBHYPHEN}р'

    assert check_portion({
        'street': 'Лен/cкий',
        'street_type_full': 'бульвар',
    }, AddressComponent.STREET) == f'Лен{NBSLASH}cкий{NBSPACE}б{NBHYPHEN}р'


def test_format_result():
    assert format_result(["foo", IS_ERROR]) == ""
    assert format_result(["foo", None]) == "foo"
    assert format_result(["foo", None, "buz"]) == "foo, buz"
    assert format_result(["", "foo", "buz"]) == "foo, buz"

    assert format_result(["foo", "buz"]) == "foo, buz"


def test_format_result_unique():
    assert format_result(["foo", "foo", "buz"]) == "foo, buz"
    assert format_result(["foo", "foo", "buz", "foo"]) == "foo, buz, foo"


def test_all_formats():
    test_address_components = {
        'area': None,
        'city': 'Брянск',
        'flat': None,
        '_type': 'addresscomponents',
        'block': None,
        'house': '9',
        'short': {
            'flat': None, 'house': '9', 'street': None, 'country': 'Россия',
            'locality': 'Брянск', 'flat_type': None, 'house_type': 'д',
            'postal_code': '241035', 'street_type': None,
            'flat_type_full': None,
            'house_type_full': 'дом', 'street_type_full': None
        },
        'region': 'Брянская',
        'street': None,
        'country': 'Россия',
        'section': None, 'building': None,
        'area_type': None, 'city_type': 'г', 'flat_type': None,
        'block_type': None,
        'house_type': 'д', 'settlement': None, 'postal_code': '241035',
        'region_type': 'обл', 'street_type': None, 'city_district': 'Бежицкий',
        'area_type_full': None, 'city_type_full': 'город',
        'flat_type_full': None,
        'block_type_full': None, 'house_type_full': 'дом',
        'settlement_type': None,
        'region_type_full': 'область', 'street_type_full': None,
        'city_district_type': 'р-н', 'settlement_type_full': None,
        'city_district_type_full': 'район'
    }

    result = all_formats("plain_address", test_address_components, "1", 1)
    assert result == {
        'all': f'Брянская{NBSPACE}обл., г.{NBSPACE}Брянск, Бежицкий{NBSPACE}р{NBHYPHEN}н, д.{NBSPACE}9, кв.{NBSPACE}1',  # noqa
        'street_only': 'plain_address',
        'finishing_with_village': f'Брянская{NBSPACE}обл., г.{NBSPACE}Брянск, Бежицкий{NBSPACE}р{NBHYPHEN}н',  # noqa
        'starting_with_street': f'д.{NBSPACE}9, кв.{NBSPACE}1',
        'finishing_with_street': f'Брянская{NBSPACE}обл., г.{NBSPACE}Брянск, Бежицкий{NBSPACE}р{NBHYPHEN}н',  # noqa
    }

    result = all_formats("plain_address", test_address_components, None, None)
    assert result == {
        'all': f'Брянская{NBSPACE}обл., г.{NBSPACE}Брянск, Бежицкий{NBSPACE}р{NBHYPHEN}н, д.{NBSPACE}9',  # noqa
        'street_only': 'plain_address',
        'finishing_with_village': f'Брянская{NBSPACE}обл., г.{NBSPACE}Брянск, Бежицкий{NBSPACE}р{NBHYPHEN}н',  # noqa
        'starting_with_street': f'д.{NBSPACE}9',
        'finishing_with_street': f'Брянская{NBSPACE}обл., г.{NBSPACE}Брянск, Бежицкий{NBSPACE}р{NBHYPHEN}н',  # noqa
    }


@pytest.mark.parametrize("testcase", (
    (
        {
            "region": "Курганская", "region_type_full": "область",
            "area": "Катайский", "area_type_full": "район",
            "city": "Серов", "city_type_full": "город",
            "city_district": "Кировский", "city_district_type_full": "округ",
            "settlement": "Дрянное", "settlement_type_full": "село",
            "street": "Майская", "street_type_full": "улица",
            "house": "5", "house_type_full": "дом",
            "section": "6", "building": "7",
        }, {
            "plain_address": "",
            "premise_number": "45",
            "building_type": 2,
        },
        'all',
        'Курганская\xa0обл., Катайский\xa0р\u2060-\u2060н, г.\xa0Серов, Кировский\xa0окр., с.\xa0Дрянное, ул.\xa0Майская, д.\xa05, корп.\xa06, стр.\xa07, м.\xa045'  # noqa
    ), (
        {
            "region": None, "region_type_full": None,
            "area": None, "area_type_full": None,
            "city": "Калач-на-Дону", "city_type_full": "город",
            "city_district": None, "city_district_type_full": None,
            "settlement": "им В.В.Петрова", "settlement_type_full": "село",
            "street": None, "street_type_full": None,
            "house": "5", "house_type_full": "дом",
            "section": None, "building": "7"
        }, {
            "plain_address": "",
            "premise_number": "45",
            "building_type": 2,
        },
        'all',
        'г.\xa0Калач\u2060-\u2060на\u2060-\u2060Дону, с.\xa0им.\xa0В.\xa0В.\xa0Петрова, д.\xa05, стр.\xa07, м.\xa045'  # noqa
    ), (
        {
            "region": "Пермский", "region_type_full": "край",
            "area": None, "area_type_full": None,
            "city": "Грелово", "city_type_full": "сельское поселение",
            "city_district": None, "city_district_type_full": None,
            "settlement": None, "settlement_type_full": None,
            "street": "Апрельский", "street_type_full": "бульвар",
            "house": "543", "house_type_full": "дом",
            "section": None, "building": None
        }, {
            "plain_address": "",
            "premise_number": "45",
            "building_type": 4,
        },
        'starting_with_street',
        'Апрельский\xa0б\u2060-\u2060р, д.\xa0543, м.\xa045'
    ), (
        {
            "region": "Пермский", "region_type_full": "край",
            "area": None, "area_type_full": None,
            "city": "Грелово", "city_type_full": "сельское поселение",
            "city_district": None, "city_district_type_full": None,
            "settlement": None, "settlement_type_full": None,
            "street": "Апрельский", "street_type_full": "бульвар",
            "house": "543", "house_type_full": "дом",
            "section": None, "building": None
        }, {
            "plain_address": "",
            "premise_number": "45",
            "building_type": 1,
        },
        'finishing_with_village',
        'Пермский\xa0кр., с\u2060/\u2060п\xa0Грелово'
    ), (
        {
            "region": None, "region_type_full": None,
            "area": None, "area_type_full": None,
            "city": None, "city_type_full": None,
            "city_district": None, "city_district_type_full": None,
            "settlement": None, "settlement_type_full": None,
            "street": "5-я", "street_type_full": "линия",
            "house": None, "house_type_full": None,
            "section": None, "building": None
        }, {
            "plain_address": "",
            "premise_number": "45",
            "building_type": 4,
        },
        'street_only',
        '5\u2060-\u2060я\xa0лин.'
    ), (
        {
            "region": None, "region_type_full": None,
            "area": None, "area_type_full": None,
            "city": None, "city_type_full": None,
            "city_district": None, "city_district_type_full": None,
            "settlement": None, "settlement_type_full": None,
            "street": None, "street_type_full": None,
            "house": None, "house_type_full": None,
            "section": None, "building": None
        }, {
            "plain_address": "г Москва, ул Кривая",
            "premise_number": "45",
            "building_type": 4,
        },
        'street_only',
        'г Москва, ул Кривая'
    ),
))
def test_all_formats_testcases(testcase):
    address_components, kwargs, mode, result_address = testcase
    result = all_formats(address_components=address_components, **kwargs)
    assert result[mode] == result_address


@pytest.mark.parametrize("format_args", (
    (None, None, None),
    ({}, None, None),
))
def test_all_formats_invalid_input(format_args: tuple):
    plain_address = "plain_address"
    result = all_formats(plain_address, *format_args)
    assert result == {
            'all': plain_address,
            'street_only': plain_address,
            'finishing_with_village': plain_address,
            'starting_with_street': plain_address,
            'finishing_with_street': plain_address,
        }
