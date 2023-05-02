import redis
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from flask import Flask, request, jsonify

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6060)

def get_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session

session = get_session()

# Create a connection pool for requests to the file server
pool = requests.Session()
adapter = HTTPAdapter(pool_connections=1000, pool_maxsize=1000)
pool.mount('http://', adapter)

@app.route('/')
def index():
    return 'You are in the middleware application'

@app.route('/api/fileserver/<filename>', methods=['GET', 'PUT', 'DELETE'])
def fileserver(filename):
    if request.method == 'GET':
        # Check cache first
        cached_file = cache.get(filename)
        if cached_file:
            return cached_file, 200
        else:
            # Fetch file from fileserver container
            response = pool.get(f'http://nginx_fileserver:1234/api/fileserver/{filename}')
            if response.status_code == 200:
                file_contents = response.content
                cache.set(filename, file_contents)
                return file_contents, 200
            else:
                return response.content, response.status_code


    elif request.method == 'PUT':
        # Write file to fileserver container and cache it
        file_contents = request.data
        response = pool.put(f'http://nginx_fileserver_put:1234/api/fileserver/{filename}', data=file_contents)
        if response.status_code == 201:
            pipeline = cache.pipeline()
            pipeline.set(filename, file_contents)
            pipeline.execute()
            return 'File created', 201
        else:
            return response.content, response.status_code

    elif request.method == 'DELETE':
        # Delete file from fileserver container and cache
        response = pool.delete(f'http://nginx_fileserver:1234/api/fileserver/{filename}')
        if response.status_code == 200:
            pipeline = cache.pipeline()
            pipeline.delete(filename)
            pipeline.execute()
            return 'File deleted', 200
        else:
            return response.content, response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)
