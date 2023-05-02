import redis
import requests

# cache = redis.Redis(host='localhost', port=6060)

# # cached_file = cache.get('aaCmCcJTldnaoCx')
# # print(cached_file)

# cache.set('test', 'TEST')

file_contents = "test"
response = requests.put(f'http://localhost:8080/api/fileserver/test', data=file_contents)
print(response.text)