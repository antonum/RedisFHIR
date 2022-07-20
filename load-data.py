import redis
import json
import os
r = redis.Redis(host='localhost', port=6379, db=0)

filenames = os.listdir('data')
for filename in filenames:
    print('processing file '+filename)
    f = open('data/'+filename)
    bundle=json.load(f)
    for entry in bundle['entry']:
        resource_type=entry['resource']['resourceType']
        resource_id=entry['resource']['id']
        key=resource_type+":"+resource_id
        body=entry['resource']
        r.json().set(key, "$", body)