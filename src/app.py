import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
import cv2
import json

# Placeholder for modular component imports (to be created)
from homography import resize_image_keep_aspect, calculate_homography, apply_homography, draw_matches
from point_selector import get_ellipse_coords, process_image

# Streamlit page configuration
st.set_page_config(page_title="Image Homography and Overlay Tool", layout="wide")

st.title("Image Homography and Overlay Tool")

# Initialize session state for storing points
if "ref_image" not in st.session_state:
    st.session_state["ref_image"] = None
if "trans_image" not in st.session_state:
    st.session_state["trans_image"] = None
if "points_top" not in st.session_state:
    st.session_state["points_top"] = []
if "points_persp" not in st.session_state:
    st.session_state["points_persp"] = []

# Function to resize image for display
def resize_image(image):
    #with Image.open(image_path) as img:
        # Resize image to fit within Streamlit window, maintaining aspect ratio
    image.thumbnail((950, 950), Image.ANTIALIAS)
    return image

col1, col2 = st.columns(2)

# Image Uploads
col1, col2 = st.columns(2)
with col1:
    st.header("Reference Image")
    ref_image_file = st.file_uploader("Upload the reference image", type=["png", "jpg", "jpeg"])
    if ref_image_file:
        st.session_state["ref_image"] = Image.open(ref_image_file)

    if st.session_state.get("ref_image") is not None:
        value_top = process_image(resize_image(st.session_state["ref_image"]), st.session_state["points_top"], streamlit_image_coordinates, "top")
        
        if value_top is not None:
            point_top = value_top["x"], value_top["y"]
            if point_top not in st.session_state["points_top"]:
                st.session_state["points_top"].append(point_top)
                st.rerun()

with col2:
    st.header("Transform Image")
    trans_image_file = st.file_uploader("Upload the Transform image", type=["png", "jpg", "jpeg"])
    if trans_image_file:
        st.session_state["trans_image"] = Image.open(trans_image_file)

    if st.session_state.get("trans_image") is not None:
        value_persp = process_image(resize_image(st.session_state["trans_image"]), st.session_state["points_persp"], streamlit_image_coordinates, "persp")
    # Handle the value_persp as before
        
        if value_persp is not None:
            point_persp = value_persp["x"], value_persp["y"]
            if point_persp not in st.session_state["points_persp"]:
                st.session_state["points_persp"].append(point_persp)
                st.rerun()

# Convert PIL images to OpenCV format and resize
if st.session_state["ref_image"] is not None:
    ref_image_cv = np.array(st.session_state["ref_image"].convert('RGB'))
    ref_image_cv = cv2.cvtColor(ref_image_cv, cv2.COLOR_RGB2BGR)
    ref_image_cv, _ = resize_image_keep_aspect(ref_image_cv)

if st.session_state["trans_image"] is not None:
    trans_image_cv = np.array(st.session_state["trans_image"].convert('RGB'))
    trans_image_cv = cv2.cvtColor(trans_image_cv, cv2.COLOR_RGB2BGR)
    trans_image_cv, _ = resize_image_keep_aspect(trans_image_cv)

# Place a button in the Streamlit app
if st.button('Calculate Homography'):
    if ref_image_cv is not None and trans_image_cv is not None and st.session_state["points_top"] and st.session_state["points_persp"]:
        # Calculate Homography
        H = calculate_homography(st.session_state["points_persp"], st.session_state["points_top"])

        # Apply Homography
        warped_image = apply_homography(trans_image_cv, ref_image_cv, H, alpha=0.6)

        # Optionally, draw matches (can be omitted if not needed)
        matched_image = draw_matches(ref_image_cv, trans_image_cv, st.session_state["points_top"], st.session_state["points_persp"])

        # Convert result back to PIL format for display
        warped_image_pil = Image.fromarray(cv2.cvtColor(warped_image, cv2.COLOR_BGR2RGB))
        matched_image_pil = Image.fromarray(cv2.cvtColor(matched_image, cv2.COLOR_BGR2RGB))

        # Display results
        st.image(matched_image_pil, caption="Matched Image")
        st.image(warped_image_pil, caption="Warped Image")
        