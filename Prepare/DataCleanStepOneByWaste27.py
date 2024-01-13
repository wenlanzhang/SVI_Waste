import os
import csv

from ultralytics import YOLO

PNG_MAP = {}
CSV_LIST = []

def build_png_ind():
    folder_path = "E:\WorkSpace\SVI_Waste\source\Maoran"
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            PNG_MAP[filename] = file_path
def read_csv():
    csv_file_path = "E:\WorkSpace\SVI_Waste\source\Maoran\pano_nairobi.csv"
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            CSV_LIST.append(row)


def label_png():
    count = 0
    ang_list = ["_0", "_90", "_180", "_270"]
    model = YOLO("E:\WorkSpace\SVI_Waste\waste27.pt")
    for line in CSV_LIST:
        pre_name = line[2]
        if pre_name == "panoid":
            continue
        for ang in ang_list:
            name = pre_name+ang+".jpg"
            if name in PNG_MAP:
                path = PNG_MAP[name]
                if os.path.exists(path):
                    count = count + 1
                    print(count)
                    res_list = model(path,
                                     imgsz=(400, 300), conf=0.6, device=0)
                    mark = False
                    for res in res_list:
                        p_list = res.boxes.cpu().conf.numpy()
                        if p_list.size > 0:
                            p = p_list[0]
                            if p > 0:
                                line.append(p)
                                mark = True
                                break
                    if not mark:
                        line.append(0)
            else:
                line.append(-1)

    csv_file_path = 'E:\WorkSpace\SVI_Waste\source\output.csv'
    # 将二维数组写入CSV文件
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(CSV_LIST)


if __name__ == '__main__':
    build_png_ind()
    read_csv()
    label_png()