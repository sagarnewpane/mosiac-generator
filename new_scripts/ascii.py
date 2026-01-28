from PIL import Image, ImageDraw
import math
import old_scripts.colorValue as colorValue
# import overlay
import old_scripts.s as s

chars = [f"SquaredImages/img_{i}.jpg" for i in range(1,73)]
# charArray = list(chars)
charLength = len(chars)
interval = charLength/256

scaleFactor = 0.3

oneCharWidth = 50
oneCharHeight = 50


def reduce_image_size(img, max_size=500):
    width, height = img.size
    aspect_ratio = width / height

    if width > height:
        new_width = max_size
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = max_size
        new_width = int(new_height * aspect_ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)
    print(f"Reduced image size from {width}x{height} to {new_width}x{new_height}")
    img.save('resixed.png')
    return img

# def average_color(img):
#     # Get the image data
#     img_data = img.getdata()

#     # Calculate the average color values
#     total_red = total_green = total_blue = 0
#     total_pixels = len(img_data)

#     for pixel in img_data:
#         total_red += pixel[0]
#         total_green += pixel[1]
#         total_blue += pixel[2]

#     avg_red = total_red // total_pixels
#     avg_green = total_green // total_pixels
#     avg_blue = total_blue // total_pixels

#     return avg_red, avg_green, avg_blue

def average_color(img):
    """Calculates the average RGB color of a PIL Image object."""
    # resizing to 1x1 is a fast way to get the average color
    img_small = img.resize((1, 1), Image.Resampling.LANCZOS)
    return img_small.getpixel((0, 0))


def crop_center_square(img, size=50):
    """Crop image to square from center and resize."""
    width, height = img.size
    min_dim = min(width, height)
    
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    
    img = img.crop((left, top, right, bottom))
    return img.resize((size, size), Image.LANCZOS)


def process(path,outputPath,name,tile_library=chars):

    tile_library = [crop_center_square(Image.open(p).convert('RGB'), oneCharWidth) for p in tile_library]
    color_set = [average_color(tile) for tile in tile_library]

    image_path = path  

    # save the processed image to the 'riddles/static/processed/' directory
    output_path = f'{outputPath}/{name}.png'

    img = Image.open(image_path).convert('RGB')
    img = reduce_image_size(img,350)  # pass the image object to the function
    width, height = img.size
    img = img.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.Resampling.NEAREST)
    width, height = img.size
    pix = img.load()

    outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = (0, 0, 0))

    cache = {}
    for i in range(height):
        for j in range(width):
            r,g,b = pix[j, i][:3]
            color_key = (r,g,b)
            if color_key not in cache:
                closest_path = colorValue.get_closest_image(color_key, tile_library, color_set)
                cache[color_key] = s.changeColor(closest_path.copy(), r, g, b)
            
            closest_image = cache[color_key]
            outputImage.paste(closest_image, (j*oneCharWidth, i*oneCharHeight))

    print('Overlaying')
    outputImage.save(output_path, "PNG")
    return output_path

