# -*- coding: utf-8 -*-
"""Fault_detection_in Solar_panels.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dSGPd8PikTib9nTXqjDaOm18LMtI1ZxX
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the thermal image
img = cv2.imread('/content/s2.jpg') #path of the image of panel

# Define the color range to locate
lower_color_range = (150, 200, 200)  # Lower bound of the color range in RGB format
upper_color_range = (255, 255, 255)  # Upper bound of the color range in RGB format

# Define the range of x-axis and y-axis to search in
x_start = 600
x_end = 850
y_start = 200
y_end = 500

# Create a mask for the specified color range, x-axis range, and y-axis range
mask = np.zeros_like(img[:, :, 0])
mask[(img[:, :, 0] >= lower_color_range[0]) & (img[:, :, 0] <= upper_color_range[0]) &
     (img[:, :, 1] >= lower_color_range[1]) & (img[:, :, 1] <= upper_color_range[1]) &
     (img[:, :, 2] >= lower_color_range[2]) & (img[:, :, 2] <= upper_color_range[2]) &
     (np.arange(img.shape[1])[np.newaxis, :] >= x_start) & (np.arange(img.shape[1])[np.newaxis, :] <= x_end) &
     (np.arange(img.shape[0])[:, np.newaxis] >= y_start) & (np.arange(img.shape[0])[:, np.newaxis] <= y_end)] = 255
# Find the contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop through the contours and find their centroid
for cnt in contours:
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        print(f"The centroid of the color range {lower_color_range} - {upper_color_range} is located at ({cx}, {cy})")
        # Draw a circle at the centroid location and label with the coordinates
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)
        cv2.putText(img, f"({cx}, {cy})", (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the original image and the mask image using Matplotlib
fig, axs = plt.subplots(1, 2, figsize=(25, 15))
axs[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
axs[0].set_title('Original Image')
axs[1].imshow(mask, cmap='gray')
axs[1].set_title('Mask Image')
plt.show()
