from PIL import Image
import math
import random

# with random one
def get_closest_image(rgb_value, image_objs, color_set, perturbation_factor=30):
    # Introduce a small random perturbation to the target color
    target = tuple([
        min(255, max(0, c + random.randint(-perturbation_factor, perturbation_factor)))
        for c in rgb_value
    ])
    # 2. Optimized Search
    # We find the index of the color with the smallest squared distance
    best_index = -1
    min_dist = float('inf')

    for i, color in enumerate(color_set):
        # Squared Euclidean Distance (No math.sqrt needed!)
        dist = (target[0] - color[0])**2 + (target[1] - color[1])**2 + (target[2] - color[2])**2
        
        if dist < min_dist:
            min_dist = dist
            best_index = i
    return image_objs[best_index]


if __name__ == "__main__":
    # Replace (100, 150, 200) with the actual RGB value you want to match
    rgb_value = (100, 150, 200)
    
    # Replace ['path/to/image1.jpg', 'path/to/image2.jpg', ...] with the actual paths to your image files
    image_paths = ['1.jpg', '2.jpg', '3.jpg']

    closest_image = get_closest_image(rgb_value, image_paths)
    closest_image.show()