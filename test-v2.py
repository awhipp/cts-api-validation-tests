import os
import time
import requests
from retrying import retry
from requests.structures import CaseInsensitiveDict

url = os.environ['CTS_API_URL'] + 'api/v2/'

headers = CaseInsensitiveDict()

if 'API_KEY' in os.environ:
    headers['x-api-key'] = os.environ['API_KEY']
else:
    headers['Origin'] = os.environ['TESTING_ORIGIN']

email = os.environ['USER_EMAIL']
headers['Content-Type'] = 'application/json'

@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=5000)
def execute_get(url, headers, should_fail):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        if should_fail:
            print('GET %s failed (was supposed to).' % url)
        else:
            print(response.content)
            raise Exception('GET %s Failed with Code %s' % (url, str(response.status_code)))
    else:
        print('GET %s succeeded.' % url)

@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=5000)
def execute_post(url, headers, body, should_fail):
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        if should_fail:
            print('POST %s failed (was supposed to).' % url)
        else:
            print(response.content)
            raise Exception('POST %s Failed with Code %s' % (url, str(response.status_code)))
    else:
        print('POST %s succeeded.' % url)

# Test 1
for year in range(2016, 2022):
    body = { 
        "sites.org_state_or_province": ["CA", "OR"], 
        "record_verification_date_gte": "%s-06-01" % year, 
        "include": ["nci_id"] 
    }
    execute_post(url + 'trials', headers, body, False)

# Test 2 (max of 50)
for i in range(0, 6):
    size = (i * 10) + 1
    execute_get(url + 'trials?size=%s' % (size), headers, size > 50)

# Test 3 (no fail)
for i in range(0, 6):
    size = (i * 10**i) + 1
    execute_get(url + 'trials?size=%s&export=json&email=%s' % (size, email), headers, False)

# Test 4 (max of 50000)
for i in range(0, 6):
    size = (i * 10**i) + 1
    execute_get(url + 'organizations?size=%s' % size, headers, size > 50000)

# Test 5 (max of 50000)
for i in range(0, 6):
    size = (i * 10**i) + 1
    execute_get(url + 'interventions?size=%s' % size, headers, size > 50000)

# Test 6 (max of 50000)
for i in range(0, 6):
    size = (i * 10**i) + 1
    execute_get(url + 'diseases?size=%s' % size, headers, size > 50000)

# Test 7 (max of 200)
for i in range(0, 6):
    size = (i * 10**i) + 1
    execute_get(url + 'biomarkers?size=%s' % size, headers, size > 200)