# Django Terran

This repository contains `django-terran` application.

## What is Django Terran?

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
    - A country may have more than one calling code. Kazakhstan has four: "71", "72", "75", "76", "77". Dominican repulic has three: "1809", "1829", "1849".
    - Length of a phone number is not fixed. In Germany phone number may anything be between 6 and 12 digits.
- Organization Identifiers
    - Some countries assign a unique identifier to all organizations, some do not. Format of that organization identifier is country specific.
- Person Identifiers
    - Some countries assign a unique identifier to all citizens/residents, some do not. Format of that person identifier is country specific.
- Bank account numbers
    - Some countries support IBAN, but IBAN format is country specific. Some countries do not support IBAN.

## So, what do I get?

You get information about countries, administrative divisions, currencies, settlements (cities, towns, villages, hamlets). You'll need `django-terran` **and** fixtures (https://github.com/django-terran/django-terran-fixtures) because application is obviously data driven.

It may be a bit hard to comprehend, so you can play with an example application (browse to http://localhost:8080/signup/signup/); or just watch a video https://youtu.be/5uyuUl5GV6o