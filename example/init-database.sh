#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

if [[ "${BASH_TRACE:-0}" == "1" ]]; then
    set -o xtrace
fi

cd "$(dirname "$0")"

rm ~db.sqlite3 || true

./manage.py makemigrations terran
./manage.py migrate
./manage.py createsuperuser --username admin --email admin@example.com

./manage.py loaddata ../../../django-terran-fixtures/currencies.json
./manage.py loaddata ../../../django-terran-fixtures/countries.json
./manage.py loaddata ../../../django-terran-fixtures/level1areas.json
./manage.py loaddata ../../../django-terran-fixtures/level2areas.json

./manage.py loaddata ../../../django-terran-fixtures/settlements/DE-000.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/DE-001.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/FR-000.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/FR-001.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/FR-002.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/FR-003.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/FR-004.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/FR-005.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/GB-000.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/GE-000.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/US-000.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/US-001.json
./manage.py loaddata ../../../django-terran-fixtures/settlements/US-002.json

