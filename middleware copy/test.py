import redis
import requests

# cache = redis.Redis(host='localhost', port=6060)

# # cached_file = cache.get('aaCmCcJTldnaoCx')
# # print(cached_file)

# cache.set('test', 'TEST')

file_contents = "test"
response = requests.get(f'http://localhost:1234/api/fileserver/test')
print(response.status_code)