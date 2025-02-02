from flask import Flask, jsonify, send_file, send_from_directory

app = Flask(__name__)


def quad_to_index(quadkey):
    """Convert a quadkey to tile_x, tile_y, and zoom_level."""
    tile_x = 0
    tile_y = 0
    zoom_level = len(quadkey)

    # Iterate through each character in the quadkey
    for i in range(zoom_level):
        digit = int(quadkey[i])
        mask = 1 << (zoom_level - i - 1)

        # Update tile_x and tile_y based on the digit
        if digit == 1:
            tile_x |= mask  # Top-right quadrant
        elif digit == 2:
            tile_y |= mask  # Bottom-left quadrant
        elif digit == 3:
            tile_x |= mask  # Bottom-right quadrant
            tile_y |= mask

    return tile_x, tile_y, zoom_level


@app.route('/v1/assets/2/endpoint')
def fetch_app_data():
    return jsonify(
        {"type": "IMAGERY", "externalType": "BING",
         "options": {"url": "http://192.168.130.33:8001", "mapStyle": "Aerial",
                     "key": "AmXdbd8UeUJtaRSn7yVwyXgQlBBUqliLbHpgn2c76DfuHwAXfRrgS5qwfHU6Rhm8"}, "attributions": [{
            "html": "<span><a href=\"https://cesium.com\" target=\"_blank\"><img alt=\"Cesium ion\" "
                    "src=\"https://assets.ion.cesium.com/ion-credit.png\"></a></span>",
            "collapsible": False}]}
    )
    # return jsonify({"type":"IMAGERY","externalType":"BING","options":{"url":"https://dev.virtualearth.net","mapStyle":"Aerial","key":"AmXdbd8UeUJtaRSn7yVwyXgQlBBUqliLbHpgn2c76DfuHwAXfRrgS5qwfHU6Rhm8"},"attributions":[{"html":"<span><a href=\"https://cesium.com\" target=\"_blank\"><img alt=\"Cesium ion\" src=\"https://assets.ion.cesium.com/ion-credit.png\"></a></span>","collapsible":False}]})


@app.route('/REST/v1/Imagery/Metadata/Aerial')
def fetch_raster_data():
    return send_file('cfg/raster.json')


@app.route('/tiles/<quadkey>')
def fetch_tiles(quadkey):
    tile_x, tile_y, zoom_level = quad_to_index(quadkey)
    return send_from_directory(f'local/tiles/{zoom_level - 1}/{tile_x}', f'{tile_y}.jpg')

@app.route('/v1/tiles/<z>/<x>/<y>')
def fetch_v1_tiles(z, x, y):
    return send_from_directory(f'local/tiles/{z - 1}/{x}', f'{y}.jpg')


# mapbox

@app.route('/tokens/v2')
def fetch_tokens():
    return jsonify({
        'token': {
            'id': 'ugi103',
            'usage': '10000',
            'default': True,
            'user': 'U GUM IL',
            'authorization': 'Bearer <3g4!Hm*jk#9gRX>',
            'modified': '2025/01/01',
            'client': '12345678',
            'token': '12345678'
        },

        'Code': 0,
    })
@app.route('/v4/mapbox.satellite/<quadkey>')
def fetch_mapbox_satellite_tiles(quadkey):
    tile_x, tile_y, zoom_level = quad_to_index(quadkey)
    return send_from_directory(f'local/tiles/{zoom_level - 1}/{tile_x}', f'{tile_y}.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
