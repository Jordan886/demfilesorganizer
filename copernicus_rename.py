# Copernicus/FABDEM Files need to be renamed before using organize.py
import os
import re

def rename_files():
    # Get the list of files in the current directory
    files = os.listdir('.')
    
    # Regular expression pattern to extract coordinates from file names
    pattern = r'([NS]\d{2}).*([EW]\d{3})'
    
    for file in files:
        # Check if the file is a TIFF image
        if file.endswith('.tif') or file.endswith('.tiff'):
            print(f'Found TIFF image: {file}')
            
            # Extract coordinates from the file name
            match = re.search(pattern, file)
            if match:
                lat = match.group(1)
                lon = match.group(2)
                print(f'Extracted coordinates: {lat} {lon}')
                
                # Construct the new file name
                new_name = f'{lat}{lon}.tif'
                
                # Rename the file
                os.rename(file, new_name)
                print(f'Renamed "{file}" to "{new_name}"')

if __name__ == '__main__':
    rename_files()
