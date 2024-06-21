import os
import wand.image as PM
from wand.color import Color
from tqdm import tqdm

# List of Fonts to look for extracted images of glyphs
fonts = [font.split('.')[0] for font in os.listdir('../Fonts') if font.endswith('.ttf')]
#fonts = ['roya_bold']

fontsProgBar = tqdm(total=len(fonts), desc='Fonts')
for font in fonts:
    print(font)
    # Getting list of old _trim images and delete them
    oldProcessedImages = [image for image in os.listdir(font) if image.endswith('_trim.png')]
    for image in oldProcessedImages:
        os.remove(os.path.join(font, image))
    
    # for each glyph image, remove the background and trim the image
    images = [image for image in os.listdir(font) if image.endswith('.png')]
    # Define colors
    white = Color("#ffffff")
    trans = Color("#00000000")

    glyphProgBar = tqdm(total=len(images), desc='Glyphs', leave=False)
    for image in images:
        # Read the image
        glyphImage = PM.Image(filename=os.path.join(font, image))
        # Remove the backgroundf
        glyphImage.format='png'
        twenty_percent = int(65535*0.2)  # Note: percent must be calculated from Quantum
        glyphImage.transparent_color(white, alpha=0.0, fuzz=twenty_percent)
        # Trim the image
        glyphImage.trim(color=Color('rgba(0,0,0,0)'),fuzz=0)
        
        # If glyph is a Number resize it to 87 pixel height(35 for zero).
        # otherwise 58 pixel height.
        if os.path.splitext(image)[0].isnumeric():
            if os.path.splitext(image)[0] == '0': glyphImage.resize(None, 35)
            else: 
                glyphImage.resize(67, 70)
        else:
            glyphImage.resize(90, 70)
        glyphImage.save(filename=os.path.join(font, f'{image.split(".")[0]}_trim.png'))

        glyphProgBar.update(1)
    glyphProgBar.close()
    fontsProgBar.update(1)
fontsProgBar.close()