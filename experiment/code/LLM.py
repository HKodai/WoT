import matplotlib.pyplot as plt
import numpy as np

# Define the ASCII art
ascii_art = [
    "                ####     ####     ##   ##",
    " ##       ##      ### ###",
    " ##       ##      #######",
    " ##       ##      #######",
    " ##   #   ##   #  ## # ##",
    " ##  ##   ##  ##  ##   ##",
    "#######  #######  ##   ##"
]

# Define a color mapping for characters
color_map = {
    ' ': (1, 1, 1),  # White for spaces
    '#': (0, 0, 0),  # Black for '#'
}

# Create an array to hold the colors
rows = len(ascii_art)
cols = max(len(row) for row in ascii_art)  # Find the maximum row length
image = np.zeros((rows, cols, 3))  # Initialize an array for RGB colors

# Fill the image array with colors based on the ASCII art
for i, row in enumerate(ascii_art):
    for j, char in enumerate(row):
        if char in color_map:
            image[i, j] = color_map[char]

# Create the figure
fig, ax = plt.subplots(figsize=(8, 4))
ax.imshow(image, aspect='auto')
ax.axis('off')  # Turn off the axis

# Show the figure
plt.show()