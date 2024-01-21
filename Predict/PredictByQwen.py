import random

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
import os
import csv

Tokenizer = AutoTokenizer.from_pretrained("/mnt/e/WorkSpace/Qwen-VL-Chat", trust_remote_code=True)
Model = AutoModelForCausalLM.from_pretrained("/mnt/e/WorkSpace/Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()
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

def label_png_four_ang():
    count = 0
    ang_list = ["_0", "_90", "_180", "_270"]
    tmp_list = CSV_LIST
    for line in tmp_list:
        inner_count = 0
        pre_name = line[2]
        if pre_name == "panoid":
            continue
        for ang in ang_list:
            name = pre_name+ang+".jpg"
            if name in PNG_MAP and line[inner_count+8] != '0':
                path = PNG_MAP[name]
                if os.path.exists(path):
                    count = count + 1
                    print(count)
                    res = predict_by_blm(path, "这张图片中是否含有垃圾堆?")
                    print(res)
                    mark = False
                    if "是" in res or "yes" in res:
                        line.append(1)
                        mark = True
                    if not mark:
                        line.append(0)
            else:
                print("do not need predict")
                line.append(0)
            inner_count = inner_count+1

    csv_file_path = '/mnt/e/WorkSpace/SVI_Waste/source/output.csv'
    # 将二维数组写入CSV文件
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(tmp_list)

def predict_by_blm(path, ques):
    torch.manual_seed(random.randint(1, 100000))

    query = Tokenizer.from_list_format([
        {'image': path},
        {'text': ques},
    ])
    response, history = Model.chat(Tokenizer, query=query, history=None)
    return response

if __name__ == '__main__':
    build_png_ind("/mnt/e/WorkSpace/SVI_Waste/source/Maoran")
    read_csv("/mnt/e/WorkSpace/SVI_Waste/output_20240119_gs.csv")
    label_png_four_ang()