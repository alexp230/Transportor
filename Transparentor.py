from PIL import Image
import numpy as np

def MakeImageTransparent(inputPath: str, outputPath: str, backgroundColors: list, keepColors: bool):

    image = Image.open(inputPath).convert("RGBA") # open image in RGBA format
    imageData = np.array(image) # make a list of list of the pixels of the image

    def inRange(pixel, color_range):
        return all(color_range[i][0] <= pixel[i] <= color_range[i][1] for i in range(4))
    
    allPixels = imageData.shape[0] * imageData.shape[1]
    pixelCount = 0

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
                if (not keepColors):
                    imageCopy[y, x] = [255,255,255,255]
            
            pixelCount += 1
            printProgressBar(pixelCount, allPixels)

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

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    @params:
        iteration   - Required  : current iteration (int)
        total       - Required  : total iterations (int)
        prefix      - Optional  : prefix string (str)
        suffix      - Optional  : suffix string (str)
        decimals    - Optional  : positive number of decimals in percent complete (int)
        length      - Optional  : character length of bar (int)
        fill        - Optional  : bar fill character (str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (str)
    """
    def CalculateBar():
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

    if (iteration == total):
        CalculateBar()
        print("\n")
        return

    if (iteration % 175 != 0):
        return
    
    CalculateBar()    


# Ranges of colors of potential backgrounds
Gray = [(150, 250), (150, 250), (150, 250), (100, 255)]
White = [(250, 255), (250, 255), (250, 255), (100, 255)]
Black = [(0, 10), (0, 10), (0, 10), (250, 255)]
TransParent = [(0, 50), (0, 50), (0, 50), (0, 255)]

fileName = "UAB"
fileExtension = "png"
keepColors = True

fileInput = f"Inputs/{fileName}.{fileExtension}"
fileOutput = f"Outputs/{fileName}-new.{fileExtension}"

print()
# PrintPixelsOfImage(fileInput)
MakeImageTransparent(fileInput, fileOutput, [Gray, White, Black, TransParent], keepColors)
