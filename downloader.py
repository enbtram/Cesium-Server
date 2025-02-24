import json
import math
import os

import requests

def download_image(url, filename):
    """Download an image from a URL and save it to a local file."""
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Raise an error if the request was unsuccessful
        response.raise_for_status()

        # Open a local file in binary write mode and save the image
        with open(filename, 'wb') as file:
            file.write(response.content)

        print(f"Image downloaded successfully: {filename}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def lat_lon_to_tile(lat, lon, zoom):
    pixelX = (lon + 180) / 360 * 256 * (2 ** zoom)
    pixelY = (1 - math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))) / math.pi) / 2 * 256 * (
            2 ** zoom)

    tileX = int(pixelX // 256)
    tileY = int(pixelY // 256)

    return tileX, tileY


def tile_to_quadkey(tile_x, tile_y, zoom):
    quadkey = ''
    for z in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (z - 1)
        if (tile_x & mask) != 0:
            digit += 1
        if (tile_y & mask) != 0:
            digit += 2
        quadkey += str(digit)
    return quadkey

def get_tile_images(lat1, lon1, lat2, lon2, zoom):
    # Get tile coordinates for both points
    tile1_x, tile1_y = lat_lon_to_tile(lat1, lon1, zoom)
    tile2_x, tile2_y = lat_lon_to_tile(lat2, lon2, zoom)

    # Determine the range of tiles
    min_x = min(tile1_x, tile2_x)
    max_x = max(tile1_x, tile2_x)
    min_y = min(tile1_y, tile2_y)
    max_y = max(tile1_y, tile2_y)

    # Generate URLs for all tiles in the range
    tiles_urls = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            quadkey = tile_to_quadkey(x, y, zoom)
            url = f"https://ecn.t0.tiles.virtualearth.net/tiles/a{quadkey}.jpeg?g=14875"  # Example URL format
            tiles_urls.append((zoom, x, y, url))
    return tiles_urls


def save_paths_to_json(paths, chunk_index):
    print(chunk_index)
    for path in paths:
        (zoom, x, y, url) = path
        print(zoom, x, y, url)
        if not os.path.exists(os.path.join('local/tiles', f'{zoom - 1}')):
            os.mkdir(os.path.join('local/tiles', f'{zoom - 1}'))
        if not os.path.exists(os.path.join('local/tiles', f'{zoom - 1}', f'{x}')):
            os.mkdir(os.path.join('local/tiles', f'{zoom - 1}', f'{x}'))
        download_path = os.path.join(os.path.join('local/tiles', f'{zoom - 1}', f'{x}'), f"{y}.jpg")
        download_image(url, download_path)


# Example usage
lat1 = #
lon1 = #
lat2 = #
lon2 = #

import multiprocessing
import sys

if __name__ == "__main__":
    tile_image_urls = get_tile_images(lat1, lon1, lat2, lon2, int(sys.argv[1]))

    # Get the number of available CPU cores
    num_cpus = multiprocessing.cpu_count()

    # Split the list into chunks for each CPU core
    chunk_size = len(tile_image_urls) // num_cpus + (len(tile_image_urls) % num_cpus > 0)
    chunks = [tile_image_urls[i:i + chunk_size] for i in range(0, len(tile_image_urls), chunk_size)]

    # Create a pool of workers
    with multiprocessing.Pool(processes=num_cpus) as pool:
        pool.starmap(save_paths_to_json, [(chunk, i) for i, chunk in enumerate(chunks)])

    print("All files have been processed and saved.")
