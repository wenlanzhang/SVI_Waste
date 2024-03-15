import os

def create_empty_txt_files(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over files in the input folder
    for filename in os.listdir(input_folder):
        if os.path.isfile(os.path.join(input_folder, filename)):
            # Generate path for output text file
            output_file_path = os.path.join(output_folder, filename.split('.')[0] + '.txt')

            # Create an empty text file
            with open(output_file_path, 'w') as f:
                pass  # Empty file

            print(f"Created empty file: {output_file_path}")


if __name__ == "__main__":
    input_folder = '/Users/wenlanzhang/Downloads/PhD_UCL/Data/GoogleStreetView/Background'
    output_folder = '/Users/wenlanzhang/Downloads/PhD_UCL/Data/GoogleStreetView/Background/BgTxt'

    create_empty_txt_files(input_folder, output_folder)
