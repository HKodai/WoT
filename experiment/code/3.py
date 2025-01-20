import matplotlib.pyplot as plt
import numpy as np

# Define the ASCII art
ascii_art = [
    "..####.",
    ".##..##",
    ".....##",
    "...###.",
    ".....##",
    ".##..##",
    "..####."
]

# Define the color mapping
color_map = {
    '#': (0, 0, 0),  # Black for '#'
    '.': (1, 1, 1)   # White for '.'
}

# Create a 2D array to hold the RGB values
rows = len(ascii_art)
cols = max(len(row) for row in ascii_art)  # Get the maximum row length
image_data = np.zeros((rows, cols, 3))  # Initialize an array for RGB values

# Fill the image data based on the ASCII art
for i, row in enumerate(ascii_art):
    for j, char in enumerate(row):
        image_data[i, j] = color_map[char]

# Create the figure
fig, ax = plt.subplots()
ax.imshow(image_data, aspect='equal')
ax.axis('off')  # Turn off the axis

# Show the figure
plt.show()