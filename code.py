import json

def geojson_to_svg(geojson_path, svg_path, width=500, height=500):
    def coordinates_to_path(coordinates, scale, translate):
        path_data = ""
        for polygon in coordinates:
            for ring in polygon:
                for i, point in enumerate(ring):
                    x = (point[0] - translate[0]) * scale[0]
                    y = (point[1] - translate[1]) * scale[1]
                    command = "M" if i == 0 else "L"
                    path_data += f"{command}{x},{height - y} "
                path_data += "Z "
        return path_data.strip()

    with open(geojson_path, 'r') as f:
        data = json.load(f)

    # Find bounds of the coordinates
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    for feature in data['features']:
        geometry = feature['geometry']
        coords = geometry['coordinates']
        if geometry['type'] == 'Polygon':
            coords = [coords]
        for polygon in coords:
            for ring in polygon:
                for point in ring:
                    x, y = point
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

    scale_x = width / (max_x - min_x)
    scale_y = height / (max_y - min_y)
    scale = (scale_x, scale_y)
    translate = (min_x, min_y)

    svg_paths = []
    for feature in data['features']:
        geometry = feature['geometry']
        coords = geometry['coordinates']

        if geometry['type'] == 'Polygon':
            svg_paths.append(coordinates_to_path([coords], scale, translate))
        elif geometry['type'] == 'MultiPolygon':
            for polygon_coords in coords:
                svg_paths.append(coordinates_to_path([polygon_coords], scale, translate))

    with open(svg_path, 'w') as f:
        f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')
        for path in svg_paths:
            f.write(f'  <path d="{path}" fill="none" stroke="black"/>\n')
        f.write('</svg>')

# Example usage
geojson_to_svg('./data/pulau.json', 'output.svg')
