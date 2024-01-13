import os

def replace_first_15_with_0(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line.replace('15', '0', 1))

def process_txt_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            replace_first_15_with_0(file_path)

if __name__ == "__main__":
    folder_path = "E:\WorkSpace\SVI_Waste\Data\Waste4Yolo\labels"  # 替换为你的文件夹路径
    process_txt_files(folder_path)