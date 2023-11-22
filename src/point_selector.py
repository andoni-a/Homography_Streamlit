# Import necessary libraries
from PIL import Image, ImageDraw

def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 2
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )

def process_image(image, points, streamlit_image_coordinates, image_key):
    img_processed = image.copy()
    draw = ImageDraw.Draw(img_processed)

    for idx, point in enumerate(points):
        coords = get_ellipse_coords(point)
        draw.ellipse(coords, fill="blue")
        draw.text((coords[2] + 5, coords[1]), str(idx + 1), fill="red")

    value = streamlit_image_coordinates(img_processed, key=image_key)
    return value