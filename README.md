# Segment Anything Model (SAM) auto object masks
## Description:
This program utilizes the Segment Anything Model (SAM) to automatically generate and visualize object masks in images. It processes images within a specified folder, applies the SAM model to generate segmentation masks, filters out small objects based on a configurable minimum contour area, and saves visualizations of the masks with contour boundaries drawn. The visualizations are saved with a timestamp and area parameters in the filename for easy reference.

## Features:
Automatic Mask Generation: Uses a pre-trained SAM model to generate segmentation masks.
Configurable Filtering: Filters out small objects based on a user-defined minimum contour area and mask region area.
Visualization: Draws contours around detected objects and saves the visualization with relevant metadata in the filename.
Batch Processing: Processes all images in a given input folder and saves the output to a specified output folder.

## How to Use:
Model and Paths Configuration: Specify the model type and checkpoint path, and configure the input and output folder paths.
Parameters Adjustment: Set min_mask_region_area and min_contour_area to desired values to control the filtering of small objects.
Run the Script: The script will process each image in the input folder, generate masks, filter based on the set parameters, and save the visualizations in the output folder.

## Picture with boxes
![Picture with boxes - not masked](https://github.com/custom-build-robots/SAM_auto_object_masks/blob/main/background_mix_644.jpg)

## Picture with mask's

![Picture with boxes - masked](https://github.com/custom-build-robots/SAM_auto_object_masks/blob/main/background_mix_644_area_50000_contour_2000_20240804_205848_visualization.png)
