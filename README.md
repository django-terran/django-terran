# Django Terran

This repository contains `django-terran` application.

## What is Django Terran?

**TLDR**: https://youtu.be/5uyuUl5GV6o

Django terran helps you with internationalization of your sign up, registration form or other data collection.

Bad/good news: all countries are different.

Everything you can possibly assume about addresses, phone numbers, bank requisites is probably wrong for some other country.
For example:
- Address
    - Fields of address are not fixed
        - There are countries without administrative divisions like Gibraltar
        - There are countries with two levels of administrative divisions like France or UK
        - But second level of administrative division may be optional
    - Order of fields in address is not fixed
        - In Afghanistan post code goes before province
        - In Albania county goes before post code
    - Field names are not fixed
        - Whatever is State is one country may be Province, Governorate or County in another.
        - Post codes are called ZIP codes in US and Post indexes in Russia.
- Phone numbers
    - A country may have more than one calling code. Kazakhstan has four: "71", "72", "75", "76", "77". Dominican Repulic has three: "1809", "1829", "1849".
    - Length of a phone number is not fixed. In Germany phone number may anything be between 6 and 12 digits.
- Organization Identifiers
    - Some countries assign a unique identifier to all organizations, some do not. Format of that organization identifier is country specific.
- Person Identifiers
    - Some countries assign a unique identifier to all citizens/residents, some do not. Format of that person identifier is country specific.
- Bank account numbers
    - Some countries support IBAN, but IBAN format is country specific. Some countries do not support IBAN.

## So, what do I get?

You get information about countries, administrative divisions, currencies, settlements (cities, towns, villages, hamlets). You'll need `django-terran` **and** fixtures (https://github.com/django-terran/django-terran-fixtures) because application is obviously data driven.

### Examples

1. Belarus

    Address has one level of administartive divisions which are called Region.

    Belarus has post codes which must look like "{6 digits}".

    Address is written as:
    ```
    Belarus
    Region
    PostCode Settlement
    District, road, house number
    ```
    Belarus has IBAN which must look like "BY{2 digits}{2 symbols}{4 digits}{16 symbols}".

    Calling code of Belarus is +375.

    There is a government registry of organizations in Belarus.
    Organization ID is called "VAT identification number" and must look like "{9 digits}".

1. France

    Address has one or two levels of administartive divisions which are called Region and Department.

    France has post codes which must look like "{5 digits}".

    Address is written as:
    ```
    House number, road
    PostCode, Settlement
    Region, Department
    France
    ````
    France has IBAN which must look like "FR{12 digits}{11 symbols}{2 digits}".

    Calling code of France is +33.

    There is a government registry of organizations in France.
    Organization ID is called "VAT identification number" and must look like "FR{2 symbols}{9 digits}".

1. Georgia

    Address has one level of administartive divisions which are called Mkhare.

    Georgia has post codes which must look like "{4 digits}".

    Post codes are called post indexes.
    Address is written as:
    ```
    House number, road
    PostCode Settlement
    Mkhare
    Georgia
    ```
    Georgia has IBAN which must look like "GE{2 digits}{2 letters}{16 digits}".

    Calling code of Georgia is +995.

    There is a government registry of organizations in Georgia.
    Organization ID is called "Identificaion Code" and must look like "{9 digits}".

    There is a government registry of people in Georgia.
    Person ID is called "Personal Number" and must look like "{11 digits}".

1. United Arab Emirates

    Address has one level of administartive divisions which are called Emirate.

    UAE has no post codes.

    Address is written as:
    ```
    House number, road, district
    Settlement
    Emirate
    United Arab Emirates
    ```
    UAE has no IBAN.

    Calling code of UAE is +971.

1. United Stated of America

    Address has one level of administartive divisions which are called State.

    USA has post codes which must look like "{5 digits}" optionally followed by a dash and additional digits.
    Post codes are called ZIP codes.

    Address is written as:
    ```
    House number, road,
    Apartment or unit,
    Settlement, State abbreviation, ZIP code
    United States of America
    ```
    Calling code of USA is +1

    There is a government registry of organizations in USA.
    Organization ID is called "Employer Identification Number" and must look like "{9 digits}".

    There is a government registry of people in USA, but we pretend there is not, since SSN is very confidential.
    If your web-site collects SSN, you may configure that in data/user/countries/US.json file and regenerate fixtures.


It may be a bit hard to comprehend, so you can play with an example application (browse to http://localhost:8080/signup/signup/); or just watch a video https://youtu.be/5uyuUl5GV6o

## How can I help?

Except obvious, help with data https://github.com/django-terran/django-terran-data?tab=readme-ov-file#how-can-i-help

## Detailed description of Models

### [Currency](terran/models/currency.py#L24)

- iso_4217_n3 [^1]

    [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) three-digit code, primary key.
- iso_4217_a3 [^1]

    [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) three-letter code.
- is_enabled

    A boolean flag is case you want to limit available currencies.
- names [^1]

    A dictionary with names. Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- decimal_digits [^1]

    Number of decimal digits. While most currencies have two digits, not all currencies do.

### [Country](terran/models/country.py#L38)

- iso_3166_n3 [^1]

    [ISO 3166](https://en.wikipedia.org/wiki/ISO_3166) three-digit code, primary key.
- iso_3166_a2 [^1]

    [ISO 3166](https://en.wikipedia.org/wiki/ISO_3166) two-letter code.
- iso_3166_a3 [^1]

    [ISO 3166](https://en.wikipedia.org/wiki/ISO_3166) three-letter code.
- is_enabled

    A boolean flag is case you want to limit available countries.
- currency [^1]

    A reference to the currently used currency.
- names [^1]

    A dictionary with names.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- languages [^1]

    A list of official or de facto official languages. List is ordered from most popular (more speakers) to least popular (less speakers).
- address_input_layout [^3]

    A list which defined the order is which address fields should be placed in adress input form.
    It's assumed that country field is always the first, as all other fields depend on the country field.
    The following values are allowed:
     - level1area
     - level2area
     - postcode
     - settlement
     - street
- address_output_format [^3]

    A string, Django/Jinja2 template which formats address from parts according to the country specific rules.
    The following context variables are expected:
    - has_country
    - has_level1area
    - has_level2area
    - has_postcode
    - has_recipient
    - has_settlement
    - has_street
    - country_name
    - level1area_code (ISO 3166 A2 uppercase, only USA uses that)
    - level1area_name
    - level2area_code (ISO 3166 A2 uppercase, no country uses that)
    - level2area_name
    - postcode_text
    - recipient_text
    - settlement_text
    - street_text
- address_level1area_names [^1]

    A dictionary with names of level 1 administrative divisions; or null if country has no level 1 administrative divisions.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- address_level2area_names [^1]

    A dictionary with names of level 2 administrative divisions; or null if country has no level 2 administrative divisions.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- address_settlement_names [^3]

    A dictionary with names of settlement part.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- address_street_names [^3]

    A dictionary with names of street part.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
    If street part should be split in lines (like in USA), each value is not a string, but an array of strings.
- address_postcode_names [^3]

    A dictionary with names of post code; or null if country has no post code.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- address_postcode_input_pattern [^3]

    A Python/JavaScript regular expression for a valid post code; or null if country has no post code.
- address_postcode_input_example [^3]

    An example of a valid post code; or null if country has no post code.
- phone_names [^3]

    A dictionary with names of phone number.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- phone_prefixes [^3]

    A list of country calling codes.
- phone_input_pattern [^3]

    A Python/JavaScript regular expression for a valid phone number.
- phone_input_example [^3]

    An example of a valid phone number.
- phone_output_format [^3]

    A dictionary of regular expression patterns and replacement describing grouping up digits of a phone number.
    Patterns are tried in the order they are defined.
    Backreferences are declared with Python syntax \\{n}.
    Python syntax for backreferences can be converted into JavaScript syntax with a simple str.replace("\\", "$").
- organization_id_names [^3]

    A dictionary with names of organization identifier; or null if country has no organization identifier.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- organization_id_abbreviations [^3]

    A dictionary with abbreviations of organization identifier; or null if country has no organization identifier.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- organization_id_input_pattern [^3]

    A Python/JavaScript regular expression for a valid organization identifier; or null if country has no organization identifier.
- organization_id_input_example [^3]

    An example of a valid organization identifier; or null if country has no organization identifier.
- organization_id_output_format [^3]

    A dictionary of regular expression patterns and replacement describing grouping up symbols of a organization identifier; or null if country has no organization identifier.
    Patterns are tried in the order they are defined.
    Backreferences are declared with Python syntax \\{n}.
    Python syntax for backreferences can be converted into JavaScript syntax with a simple str.replace("\\", "$").
- person_id_names [^3]

    A dictionary with names of person identifier; or null if country has no person identifier.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- person_id_abbreviations [^3]

    A dictionary with abbreviations of person identifier; or null if country has no person identifier.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- person_id_input_pattern [^3]

    A Python/JavaScript regular expression for a valid person identifier; or null if country has no person identifier.
- person_id_input_example [^3]

    An example of a valid person identifier; or null if country has no person identifier.
- person_id_output_format [^3]

    A dictionary of regular expression patterns and replacement describing grouping up symbols of a person identifier; or null if country has no person identifier.
    Patterns are tried in the order they are defined.
    Backreferences are declared with Python syntax \\{n}.
    Python syntax for backreferences can be converted into JavaScript syntax with a simple str.replace("\\", "$").

- iban_names [^3]

    A dictionary with names of IBAN; or null if country has no IBAN.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.

- iban_input_pattern [^3]

    A Python/JavaScript regular expression for a valid IBAN; or null if country has no IBAN.
- iban_input_example [^3]

    An example of a valid IBAN; or null if country has no IBAN.
- iban_output_format [^3]

    A dictionary of regular expression patterns and replacement describing grouping up symbols of a IBAN; or null if country has no IBAN.
    Patterns are tried in the order they are defined.
    Backreferences are declared with Python syntax \\{n}.
    Python syntax for backreferences can be converted into JavaScript syntax with a simple str.replace("\\", "$").

### [CountryCurrency](terran/models/country.py#L239)
- id

    Primary key, unique identifier.
- country [^1]

    Reference to the country.
- currency

    [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) three-letter code.
    This field is not a reference to Currency model, because Currency model does not contain historical currencies.
- since

    Since when this currency was a valid legal tender.
- until

    Until when this currency was a valid legal tender.

### [Level1Area](terran/models/level1area.py#L24)

- id

    Primary key, unique identifier.
- country [^1]

    Reference to the country to which Level1Area belongs.
- iso_3166_a2 [^1]

    [ISO 3166](https://en.wikipedia.org/wiki/ISO_3166) code.
    Despite the name A2 it is not actually 2 letter long, but it starts with 2 letter country code.
- names [^1]

    A dictionary with names.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- expando [^2][^3]

    Some loosely structured additional data. No promises, format may change with each release.
    The following properties are often present:
    -  "open_street_map_type"

        Must be "node", "way", or "relation". Usually equals "relation".
    - "open_street_map_id"

        Integer identifier of Open Street Map element.
    - "postal_codes"

        A list of postal codes.
    - "wikidata_page_name"

        Name of wikidata article. Usually looks like "Q" followed by a number.
    - "wikipedia_pages"

        A dictionary of Wikipedia page names.
        Keys are Wikipedia languages.

### [Level2Area](terran/models/level2area.py#L25)

- id

    Primary key, unique identifier.
- country [^1]

    Reference to the country to which Level2Area belongs.
- level1area [^1]

    Reference to the Level1Area to which Level2Area belongs.
- iso_3166_a2 [^1]

    [ISO 3166](https://en.wikipedia.org/wiki/ISO_3166) code.
    Despite the name A2 it is not actually 2 letter long, but it starts with 2 letter country code.
    Beware Level1Area.iso_3166_a2 is not a prefix of Level2Area.iso_3166_a2.
- names [^1]

    A dictionary with names.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- expando [^2][^3]

    Some loosely structured additional data. No promises, format may change with each release.
    The following properties are often present:
    -  "open_street_map_type"

        Must be "node", "way", or "relation". Usually equals "relation".
    - "open_street_map_id"

        Integer identifier of Open Street Map element.
    - "postal_codes"

        A list of postal codes.
    - "wikidata_page_name"

        Name of wikidata article. Usually looks like "Q" followed by a number.
    - "wikipedia_pages"

        A dictionary of Wikipedia page names.
        Keys are Wikipedia languages.

### [Settlement](terran/models/settlement.py#L31)

**DO NOT reference this model.**

List of settlements is not exhaustive or up to date and will never be exhaustive and up to date.
There is no way to list all currently populated settlements around the globe.
Use Settlement model to suggest in autocomplete scenarios; or to find a settlement by latitude and longitude.

- id

    Primary key, unique identifier.
    If comes from Open Street Map, then equals to Open Street Map node ID.
    However, that is implementation detail. You should not rely on that.
    Better use "open_street_map_type" and "open_street_map_id" from expando attribute.
- country [^2]

    Reference to the country to which Settlement belongs.
- level1area [^2]

    Reference to the Level1Area to which Settlement belongs.
    Nullable, may be None. While nullability may not make sence at first, remember that Open Street Map data is not complete.
- level2area [^2]

    Reference to the Level2Area to which Settlement belongs.
    Nullable, may be None. While nullability may not make sence at first, remember that Open Street Map data is not complete.
- names [^2]

    A dictionary with names.
    Keys are locale codes supported by Django, see `django.conf.global_settings.LANGUAGES`.
- place_type [^2]

    A type of place.
    City, town, village, or hamlet.
- population [^2]

    Population of the settlement.
    May be zero. While value of zero may not make sence at first, remember that Open Street Map data is not complete.
    Use to prefer larger settlements in autocomplete suggestions.
- latitude [^2]

    Latitude of the settlement. Latitude ranges from -90 to 90 degrees.
    When comes from Open Street Map precision is 7 decimal digits.
- longitude [^2]

    Longitude of the settlement. Longitude ranges from -180 to 180 degrees.
    When comes from Open Street Map precision is 7 decimal digits.
- geocell [^2]

    A value between 0 and 6483600, geographic cell index
    A geographic cell is a rectange exactly 0.1 degree latitude by 0.1 degree longitude.
    A geographic cell is a rectange approximately 11 km by 11 km or smaller. Closer to the poles rectangle becomes narrow.
    A geographic cell is an effective way to find settlement from latitude and longitude without invoving a GIS engine.

    There are about 7.64 settlements per geocell on average.
    Geocell 3285343 (Uganda) has 992 settlements which is the most.
    Geocell 2990876 (Indonesia) has 34 settlements which is the most for settlements with 10 thousands or more of population.

    To find the closest to the coordinates settlement, but not too far away, use get_closest.
    ```python
    settlement = Settlement.objects.get_closest(latitude, longitude)
    ```

- expando [^2][^3]

    Some loosely structured additional data. No promises, format may change with each release.
    The following properties are often present:
    -  "open_street_map_type"

        Must be "node", "way", or "relation". Usually equals "node".
    - "open_street_map_id"

        Integer identifier of Open Street Map element.
    - "postal_codes"

        A list of postal codes.

    - "wikidata_page_name"

        Name of wikidata article. Usually looks like "Q" followed by a number.

    - "wikipedia_pages"

        A dictionary of Wikipedia page names.
        Keys are Wikipedia languages.

[^1]: Sourced from Common Locale Data Repository.
[^2]: Sourced from Open Street Map.
[^3]: Sourced from Wikipedia or user supplied data.