import os
import glob
import csv
import subprocess
import cv2 as cv
import numpy as np
# Fonts we want to extract glyphs from
fonts = [font.split('.')[0] for font in os.listdir('../Fonts') if font.endswith('.ttf')]

def getExtractorScript(fontAddr, pixelSize=600):
    return f'''
# Credit: https://superuser.com/a/1338994
import fontforge
F = fontforge.open("../{fontAddr}")
for name in F:
    filename = name + ".png"
    # print name
    # F[name].export(filename)
    F[name].export(filename, {pixelSize})     # set height to 600 pixels
F.close()
    '''

for font in fonts:
    print(font)
    # Set font file address
    fontAddr = os.path.join('../Fonts/', font)
    # Create font directory if not exists
    if not os.path.exists(font): os.mkdir(font)
    # Delete all files in the font directory
    oldFilesList = [ f for f in os.listdir(font) if f.endswith(".png") ]
    for f in oldFilesList:
        os.remove(os.path.join(font, f))

    # Write a script file to extract fonts for this font
    extractorScriptAddr = os.path.join(font, f'extract_{font.replace(" ", "_")}.py')
    extractorScript = open(extractorScriptAddr, "w")
    extractorScript.write(getExtractorScript(fontAddr))
    extractorScript.close()
    
    # Prompt which font is extracting
    print(f'\n\nExtracting fonts from {font} from {fontAddr} ...\n\n')
    # Extracting Glyphs from font using fontforge python script (ffpython)
    ffoutput = subprocess.call(['ffpython', f'extract_{font.replace(" ", "_")}.py'], cwd=font)
    
    # Read name mapping to rename glyph files
    # creates an object of {glyphNames: persianLetterName}
    nameMap = {}
    with open(os.path.join(font, f'../{fontAddr}_namesMap.csv')) as nameMapCsv:
        reader = csv.reader(nameMapCsv)
        next(reader) # Skipping header
        nameMap = {rows[0]:rows[1] for rows in reader}
    
    # Removing unnecessary files
    # remove extras like extension and addressing of the files
    imageFiles = [os.path.basename(os.path.splitext(name)[0]) for name in glob.glob(os.path.join(font, '*.png'))]


    im1 = cv.imread(os.path.join(font,"u0627.png"))
    im3 = cv.imread(os.path.join(font,"uFED2.png"))
    im2 = cv.imread(os.path.join(font,"uFEDF.png"))
    img = np.hstack([im3[:,:-1], im2[:,1:], im1])
    cv.imwrite(os.path.join(font,"u0627.png"), img)
    dotNameFiles = [os.path.basename(os.path.splitext(name)[0]) for name in glob.glob(os.path.join(font, '.*'))]
    # Mark which files to delete
    filesToKeep = [f'{name}.png' for name in nameMap.keys()]
    filesToDelete = [f'{name}.png' for name in imageFiles + dotNameFiles if name not in nameMap.keys()]
    # Delete files
    for _file in filesToDelete:
        os.remove(os.path.join(font, _file))
    # Rename files according to namesMap.csv
    for glyphName in nameMap.keys():
        if os.path.exists(os.path.join(font, f'{glyphName}.png')):
            os.rename(os.path.join(font, f'{glyphName}.png'), os.path.join(font, f'{nameMap[glyphName]}.png'))