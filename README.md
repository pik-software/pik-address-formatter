# pik-address-formatter #

This project aim is to provide address formatter from address components of housing building

Example:
```python
from address_formatter import all_formats
address_components = {
    "region": "Курганская", "region_type_full": "область",
    "area": "Катайский", "area_type_full": "район",
    "city": "Серов", "city_type_full": "город",
    "city_district": "Кировский", "city_district_type_full": "округ",
    "settlement": "Дрянное", "settlement_type_full": "село",
    "street": "Майская", "street_type_full": "улица",
    "house": "5", "house_type_full": "дом",
    "section": "6", "building": "7",
}
print(all_formats("plain address ", address_components, "5", 7)['all'])
```
Курганская обл., Катайский р⁠-⁠н, г. Серов, Кировский окр., с. Дрянное, ул. Майская, д. 5, корп. 6, стр. 7, м. 45

```text
    all_formats return dict of address formats
        all - full address with region, district, city, township, etc
        street_only - street or village
        finishing_with_village - region, district, city, township and village
        starting_with_street - street, building, section, construction, premise
        finishing_with_street - region, district, city, township, village, street
```

## HowToUse ##

* Add pik-address-formatter to requirements.txt
```
pik-address-formatter>=1.0,<2.0
```

* Add address_formats method to target model
```python
from django.db import models
from address_formatter import all_formats

class Account(models.Model):
    ...
    @property
    def address_formats(self):
        return all_formats(
            self.premise.address,
            self.building.user_address_components,
            self.premise.user_number,
            self.building.type,
    )
```
* If you dosn't have a premise model, just use without premise data
```python
from django.db import models
from address_formatter import all_formats

class Account(models.Model):
    ...
    @property
    def address_formats(self):
        return all_formats(
            self.building.address,
            self.building.user_address_components,
            building_type=self.building.type,
    )
```

* For details see docstring of all_formats
 