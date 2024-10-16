import os
import re

def extract_folder_name(filename):
    # Extract coordinates from the filename using regular expression
    match = re.match(r'([NS])(\d+)([EW])(\d+)', filename)
    if match:
        lat_dir, lat_val, lon_dir, lon_val = match.groups()
        lat_val = int(lat_val)
        lon_val = int(lon_val)

        # Calculate base folder latitude
        if lat_dir == 'S':
            base_folder_lat = -(((lat_val - 1) // 10) + 1) * 10
        else:  # 'N'
            base_folder_lat = (lat_val // 10) * 10

        # Calculate base folder longitude
        if lon_dir == 'W':
            base_folder_lon = -(((lon_val - 1) // 10) + 1) * 10
        else:  # 'E'
            base_folder_lon = (lon_val // 10) * 10

        # Handle special case for longitude 180
        if abs(base_folder_lon) > 170:
            base_folder_lon = 180 if lon_dir == 'E' else -180

        lat_folder = f"{base_folder_lat:+03d}"
        lon_folder = f"{base_folder_lon:+04d}"

        return f"{lat_folder}{lon_folder}"
    else:
        print(f"No coordinates found in filename: {filename}")
        return None

def main():
    # Get all files in the current directory
    files = [f for f in os.listdir() if os.path.isfile(f) and not f.lower().endswith('.zip')]

    for file in files:
        folder_name = extract_folder_name(file)
        if folder_name:
            # Create the folder if it doesn't exist
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            # Extract the coordinates from the filename
            match = re.match(r'([NS]\d+[EW]\d+)', file)
            if match:
                coordinates = match.group()
                # Get the file extension
                file_extension = os.path.splitext(file)[1]
                # Rename the file to include only the coordinates and original extension
                new_filename = f"{coordinates}{file_extension}"
                # Move the file into the folder with the new filename
                os.rename(file, os.path.join(folder_name, new_filename))
            else:
                print(f"No coordinates found in filename: {file}")

if __name__ == "__main__":
    main()