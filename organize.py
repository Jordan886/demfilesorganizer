import os
import re

def extract_folder_name(filename):
    # Extract coordinates from the filename using regular expression
    match = re.match(r'([NS])(\d+)([EW])(\d+)', filename)
    if match:
        lat_dir, lat_val, lon_dir, lon_val = match.groups()
        direction_mapping = {"N": "+", "S": "-", "E": "+", "W": "-"}
        lat_val = int(lat_val)
        lon_val = int(lon_val)

        lat_sign = direction_mapping.get(lat_dir)
        lon_sign = direction_mapping.get(lon_dir)

        if lat_sign is None or lon_sign is None:
            print(f"Invalid direction in filename: {filename}")
            return None

        # Adjust the sign for the first part of the folder name for southern hemisphere coordinates
        if lat_sign == "-":
            base_folder_lat = ((lat_val // 10) + 1) * 10
        else:
            base_folder_lat = (lat_val // 10) * 10

        if lon_sign == "-":
             base_folder_lon = ((lon_val // 10) +1) * 10
        else:
            base_folder_lon = (lon_val // 10) * 10

        # If tile W180 do not create -190 folder
        if base_folder_lon >= 180:
             base_folder_lon = 180

        lat_folder = f"{lat_sign}{str(base_folder_lat).zfill(2)}"
        lon_folder = f"{lon_sign}{str(base_folder_lon).zfill(3)}"

        return f"{lat_folder}{lon_folder}"
    else:
        print(f"No coordinates found in filename: {filename}")
        return None



def main():
    # Get all files in the current directory
    files = [f for f in os.listdir() if os.path.isfile(f)]

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
