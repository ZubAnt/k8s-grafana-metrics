.PHONY: requirements.txt docs clean

define get_requirements
import tomlkit
with open('poetry.lock') as t:
    lock = tomlkit.parse(t.read())
    for p in lock['package']:
        if not p['category'] == 'dev' and not p['name'].endswith('-stubs'):
            print(f"{p['name']}=={p['version']}")
endef
export get_requirements


define get_services
import json
with open('services.json') as fp:
    services = json.load(fp)
    result = {}
    for item in services:
        if item['fields'].get('key') and item['fields'].get('secret'):
            result[item['fields']['key']+item['fields']['secret']] = item['pk']
print(json.dumps(result, indent=2))
endef
export get_services

requirements.txt: poetry.lock
	poetry run python -c "$$get_requirements" > requirements.txt

