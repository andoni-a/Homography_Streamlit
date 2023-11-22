import cv2
import numpy as np
import random

def resize_image_keep_aspect(image, target_size=(950, 950)):
    h, w = image.shape[:2]
    scale = min(target_size[0] / w, target_size[1] / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized_image, scale

def calculate_homography(points_persp, points_top):
    pts_persp = np.array(points_persp, dtype=np.float32)
    pts_top = np.array(points_top, dtype=np.float32)
    H, _ = cv2.findHomography(pts_persp, pts_top, cv2.RANSAC, 5.0)
    return H

def apply_homography(persp_img, top_img, H, alpha=0.6):
    """
    Apply homography to perspective image and overlay it on the top image.
    
    :param persp_img: Perspective image (numpy array)
    :param top_img: Top view image (numpy array)
    :param H: Homography matrix
    :param alpha: Transparency level for the overlay (default 0.6)
    :return: Image with the warped perspective overlaid on the top image with red tint
    """
    # Warp perspective
    height, width, channels = top_img.shape
    warped_persp = cv2.warpPerspective(persp_img, H, (width, height))

    # Apply a red tint to the warped image
    red_tint = np.full(warped_persp.shape, (0, 0, 255), dtype=np.uint8)  # Red tint
    tinted_warped = cv2.addWeighted(warped_persp, 0.5, red_tint, 0.5, 0)

    # Blend the tinted warped image with the top image
    blended_image = cv2.addWeighted(top_img, 1 - alpha, tinted_warped, alpha, 0)

    return blended_image

def draw_matches(top_img, persp_img, points_top, points_persp):
    h1, w1 = top_img.shape[:2]
    h2, w2 = persp_img.shape[:2]
    nWidth = w1 + w2
    nHeight = max(h1, h2)
    new_img = np.zeros((nHeight, nWidth, 3), np.uint8)
    new_img[:h1, :w1, :3] = top_img
    new_img[:h2, w1:w1+w2, :3] = persp_img

    for pt1, pt2 in zip(points_top, points_persp):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pt2_mod = (pt2[0] + w1, pt2[1])
        cv2.line(new_img, pt1, pt2_mod, color, 1)

    return new_img