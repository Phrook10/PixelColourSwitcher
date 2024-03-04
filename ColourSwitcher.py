# Copyright (c) 2024 Joshua Haller
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#imports
from PIL import Image
import os

def replacecolour(imagePath, sourcecolour, targetcolour, outputPath, debugFile):
    try:
        #Open the image
        image = Image.open(imagePath)
        
        #Get the size of the image
        width, height = image.size
        
        #Open debug file for writing
        debugFile.write(f"Processing image: {imagePath}\n")
        
        #Iterate over each pixel in the image
        for y in range(height):
            for x in range(width):
                currentcolour = image.getpixel((x, y))                                                          #Get the current pixel colour
                
                #Check if the current pixel matches the source colour
                if currentcolour[:3] == sourcecolour:
                    
                    #Replace the current pixel with the target colour
                    newcolour = targetcolour + (currentcolour[3],)                                              #Preserve the alpha channel
                    image.putpixel((x, y), newcolour)
                    debugFile.write(f"Replaced colour at pixel ({x}, {y}) with: {newcolour}\n")                 #Write debug info to file
        
        image.save(outputPath)                                                                                  #Save the modified image
        return True
    except Exception as e:
        debugFile.write(f"Error processing image: {e}\n")
        return False

if __name__ == "__main__":
    #Input directory containing images to modify
    directory = input("Enter the directory path containing images to modify (press Enter for current directory): ")
    if not directory:                                                                                           #If directory input is empty (user pressed Enter)
        directory = os.getcwd()                                                                                 #Set directory to current working directory
    
    #Input source and target colours in RGB format
    sourcecolour = tuple(int(x) for x in input("Enter the source colour (RGB format, e.g., 255 0 0): ").split())
    targetcolour = tuple(int(x) for x in input("Enter the corresponding target colour (RGB format, e.g., 0 255 0): ").split())
    
    #Open debug file for writing
    debugFilePath = os.path.join(directory, "debugOutput.txt")
    with open(debugFilePath, 'w') as debugFile:
        
        #Iterate over files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                inputImagePath = os.path.join(directory, filename)                                              #Full path of the input image
                outputImagePath = os.path.join(directory, "modified_" + filename)                               #Full path of the output image
                
                # Replace colour in the image
                success = replacecolour(inputImagePath, sourcecolour, targetcolour, outputImagePath, debugFile)
                if success:
                    print(f"Processed: {inputImagePath} -> {outputImagePath}")
                else:
                    print(f"Error processing: {inputImagePath}")
    
    print(f"Debug output saved to: {debugFilePath}")


