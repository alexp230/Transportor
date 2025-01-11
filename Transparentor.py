from PIL import Image
import numpy as np

def MakeImageTransparent(inputPath: str, outputPath: str, backgroundColors: list):

    image = Image.open(inputPath).convert("RGBA") # open image in RGBA format
    imageData = np.array(image) # make a list of list of the pixels of the image

    def inRange(pixel, color_range):
        return all(color_range[i][0] <= pixel[i] <= color_range[i][1] for i in range(4))
    
    imageCopy = imageData.copy()

    # Loop through all pixels in image
    for y in range(imageData.shape[0]):
        for x in range(imageData.shape[1]):
            pixel = imageData[y, x]

            # If pixel is apart of the background colors, then make transparent, else make it white
            for backgroundColor in backgroundColors:
                if (inRange(pixel, backgroundColor)):
                    imageCopy[y, x] = [0, 0, 0, 0]
                    break
            else:
                imageCopy[y, x] = [255,255,255,255]

    # Create a new image from the modified copy and make new file
    Image.fromarray(imageCopy, mode="RGBA").save(outputPath)

    print(f"Transparent image successfully saved to {outputPath}")

def PrintPixelsOfImage(imagePath):

    image = Image.open(imagePath).convert("RGB") # open the image
    width, height = image.size
    pixels = image.load()
    
    # Loop through each pixel and print its RGB values
    for y in range(height//4):
        for x in range(width):
            r, g, b = pixels[x, y]
            print(f"Pixel ({x}, {y}): R={r}, G={g}, B={b}")


# Ranges of colors of potential backgrounds
Gray = [(150, 250), (150, 250), (150, 250), (100, 255)]
White = [(250, 255), (250, 255), (250, 255), (100, 255)]
Black = [(0, 10), (0, 10), (0, 10), (250, 255)]


fileInput = "Number6.png"
fileOutput = "Number6New.png"

MakeImageTransparent(fileInput, fileOutput, [White, Gray])
