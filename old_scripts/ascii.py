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

def average_color(img):
    # Get the image data
    img_data = img.getdata()

    # Calculate the average color values
    total_red = total_green = total_blue = 0
    total_pixels = len(img_data)

    for pixel in img_data:
        total_red += pixel[0]
        total_green += pixel[1]
        total_blue += pixel[2]

    avg_red = total_red // total_pixels
    avg_green = total_green // total_pixels
    avg_blue = total_blue // total_pixels

    return avg_red, avg_green, avg_blue


def process(path,name):
    color_set = [average_color(Image.open(image_path)) for image_path in chars]

    image_path = path  

    # save the processed image to the 'riddles/static/processed/' directory
    output_path = f'{name}.png'

    img = Image.open(image_path).convert('RGB')
    img = reduce_image_size(img)  # pass the image object to the function
    width, height = img.size
    img = img.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
    width, height = img.size
    pix = img.load()

    outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = (0, 0, 0))

    for i in range(height):
        for j in range(width):
            pixel = pix[j, i]
            if len(pixel) == 3:
                r, g, b = pixel
                a = 255  # or any default value
            else:
                r, g, b, a = pixel
            closest_image = s.changeColor(colorValue.get_closest_image((r,g,b), chars,color_set),r,g,b)

            outputImage.paste(closest_image, (j*oneCharWidth, i*oneCharHeight))

    print('Overlaying')
    outputImage.save(output_path, "PNG")

    # remove 'riddles/static/' from the output_path to get the URL for the processed image
    processed_image_url = output_path.replace('riddles/static/', '')

    return processed_image_url