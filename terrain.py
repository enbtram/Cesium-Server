from flask import Flask, request, send_from_directory, jsonify, make_response
import os
import gzip
import io
from multiprocessing import Process, cpu_count

app = Flask(__name__)

# Define gzip header
gzip_header = b'\x1f\x8b\x08'

# Define mime types
mime_types = {
    'application/json': ['czml', 'json', 'geojson', 'topojson'],
    'application/vnd.quantized-mesh': ['terrain'],
    'model/vnd.gltf+json': ['gltf'],
    'model/vnd.gltf.binary': ['glb', 'bgltf'],
    'application/octet-stream': ['b3dm', 'pnts', 'i3dm', 'cmpt', 'terrain'],
    'text/plain': ['glsl']
}

# Set headers
@app.after_request
def set_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "PUT,POST,GET,DELETE,OPTIONS"
    response.headers["X-Powered-By"] = '3.2.1'
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response

# Check gzip and next
def check_gzip_and_next(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(3)
            if header == gzip_header:
                return True
    except Exception as e:
        pass
    return False

# Known tileset formats
known_tileset_formats = ['.terrain', '.b3dm', '.pnts', '.i3dm', '.cmpt', '.glb', 'tileset.json']


@app.route('/<path:filename>', methods=['GET'])
def serve_file(filename):
    if any(filename.endswith(ext) for ext in known_tileset_formats):
        if check_gzip_and_next(filename):
            response = make_response(send_from_directory('local/terrain', filename))
            response.headers['Content-Encoding'] = 'gzip'
            return response
    return send_from_directory('local/terrain', filename)


@app.route('/')
def get_LayerJson():
    return send_from_directory(f"local/terrain", 'layer.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
