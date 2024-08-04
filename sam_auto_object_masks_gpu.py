# Autor:    Ingmar Stapel
# Datum:    20240804
# Version:  1.0
# Homepage: https://ai-box.eu/
# Description:
# This program utilizes the Segment Anything Model (SAM) to automatically generate and visualize object masks in images. 
# It processes images within a specified folder, applies the SAM model to generate segmentation masks, filters out small 
# objects based on a configurable minimum contour area, and saves visualizations of the masks with contour boundaries 
# drawn. The visualizations are saved with a timestamp and area parameters in the filename for easy reference.

import os
import cv2
import torch
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from datetime import datetime

# Load the Segment Anything model with pre-trained weights
model_type = "vit_h"  # specify your model type here, e.g., vit_h, vit_l, etc.
checkpoint_path = "/mnt/raid-data/07_model_zoo/01_SAM/sam_vit_h_4b8939.pth"  # specify the path to your model checkpoint here

# Load the SAM model and move to CUDA
device = "cuda" if torch.cuda.is_available() else "cpu"
sam_model = sam_model_registry[model_type](checkpoint=checkpoint_path)
sam_model.to(device=device)

# Set the minimum mask region area
min_mask_region_area = 50000  # Set this to the desired minimum area for the masks

# Set the minimum contour area to filter out small objects
min_contour_area = 2000  # Set this to the desired minimum area for the contours

# Configure the mask generator with min_mask_region_area to filter out small objects
mask_generator = SamAutomaticMaskGenerator(
    model=sam_model,
    min_mask_region_area=min_mask_region_area,
    points_per_side=32,
    points_per_batch=64,
    pred_iou_thresh=0.95,  # Adjust for higher IoU threshold
    stability_score_thresh=0.95,
    box_nms_thresh=0.8,  # Increase NMS threshold to filter more overlapping masks
    crop_n_layers=1,
    crop_n_points_downscale_factor=2
)

def segment_and_visualize_objects(image_path, output_dir):
    # Read the image
    image = cv2.imread(image_path)

    # Generate masks
    masks = mask_generator.generate(image)

    # Create a copy of the original image for visualization
    vis_image = image.copy()

    for mask_dict in masks:
        mask = mask_dict['segmentation']  # Extract the segmentation mask
        
        # Ensure mask is binary
        binary_mask = (mask > 0).astype('uint8') * 255

        # Find contours to draw the boundaries of the mask
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            for contour in contours:
                area = cv2.contourArea(contour)
                if area >= min_contour_area:
                    # Draw the contours on the visualization image
                    cv2.drawContours(vis_image, [contour], -1, (0, 255, 0), 2)  # Green contours

    # Construct the output file path with min_mask_region_area and timestamp
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"{base_filename}_area_{min_mask_region_area}_contour_{min_contour_area}_{timestamp}_visualization.png"
    output_path = os.path.join(output_dir, output_filename)

    # Save the visualization image
    cv2.imwrite(output_path, vis_image)
    print(f"Visualization saved as {output_path}")

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                segment_and_visualize_objects(image_path, output_folder)

# Define input and output folders
input_folder = '/mnt/raid-data/01_raw_data/input/small/'
output_folder = '/mnt/raid-data/01_raw_data/output/visualization/'

# Process the folder
process_folder(input_folder, output_folder)
