import redis
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6060)

@app.route('/')
def index():
    return 'You are in the middleware application'

@app.route('/api/fileserver/<filename>', methods=['GET', 'PUT', 'DELETE'])
def fileserver(filename):
    if request.method == 'GET':
        # Check cache first
        cached_file = cache.get(filename)
        if cached_file:
            return cached_file.decode('utf-8'), 200
        else:
        # Fetch file from fileserver container
            response = requests.get(f'http://localhost:1234/api/fileserver/{filename}')
            if response.status_code == 200:
                file_contents = response.text
                cache.set(filename, file_contents)
                return file_contents, 200
            else:
                return 'File not found', 404


    elif request.method == 'PUT':
        # Write file to fileserver container and cache it
        file_contents = request.data.decode('utf-8')
        response = requests.put(f'http://localhost:1234/api/fileserver/{filename}', data=file_contents)
        if response.status_code == 201:
            cache.set(filename, file_contents)
            return 'File created', 201
        else:
            return 'Unable to create file', 500

    elif request.method == 'DELETE':
        # Delete file from fileserver container and cache
        response = requests.delete(f'http://localhost:1234/api/fileserver/{filename}')
        if response.status_code == 200:
            cache.delete(filename)
            return 'File deleted', 200
        else:
            return 'Unable to delete file', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
