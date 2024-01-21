import os
import csv

from ultralytics import YOLO

PNG_MAP = {}
CSV_LIST = []

def build_png_ind(folder_path):
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            PNG_MAP[filename] = file_path

def read_csv(csv_file_path):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            CSV_LIST.append(row)


def label_png(model):
    count = 0
    tmp_list = CSV_LIST
    for line in tmp_list:
        name = line[1]
        if name == "id":
            continue
        if name in PNG_MAP:
            path = PNG_MAP[name]
            if os.path.exists(path):
                count = count + 1
                print(count)
                res_list = model(path, device=0)
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
        csv_writer.writerows(tmp_list)

def label_png_four_ang(model):
    count = 0
    ang_list = ["_0", "_90", "_180", "_270"]
    tmp_list = CSV_LIST
    for line in tmp_list:
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
                    res_list = model(path, device=0)
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
        csv_writer.writerows(tmp_list)


if __name__ == '__main__':
    # build_png_ind("E:\WorkSpace\SVI_Waste\source\mapillary\\Used")
    # build_png_ind("E:\WorkSpace\SVI_Waste\source\self\\Used")
    # read_csv("E:\WorkSpace\SVI_Waste\source\All_Img.csv")
    # label_png(YOLO("E:\WorkSpace\SVI_Waste\Yolo8\Customised_Model\waste47.pt"))

    # build_png_ind("E:\WorkSpace\SVI_Waste\source\Maoran")
    # read_csv("E:\WorkSpace\SVI_Waste\source\Maoran\pano_nairobi.csv")
    # label_png_four_ang(YOLO("E:\WorkSpace\SVI_Waste\Yolo8\Customised_Model\waste47.pt"))
    read_csv("E:\WorkSpace\SVI_Waste\output_20240119_gs.csv")
    t = CSV_LIST
    print(t)