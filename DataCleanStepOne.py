import os
import csv

from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import detection_utils
from predictor import VisualizationDemo

PNG_MAP = {}
CSV_LIST = []

def setup_cfg():
    # load config from file and command-line arguments
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")
    # Set score_threshold for builtin models
    # cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    # cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    # cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    # cfg.freeze()
    return cfg

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
    cfg = setup_cfg()
    demo = VisualizationDemo(cfg)
    ang_list = ["_0", "_90", "_180", "_270"]
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
                    img = detection_utils.read_image(path, format="BGR")
                    predictions, _ = demo.run_on_image(img)
                    res_list = predictions['panoptic_seg'][1]
                    mark = False
                    for res in res_list:
                        is_thing = res["isthing"]
                        cate_id = res["category_id"]
                        if is_thing == False and cate_id in (11, 47):
                            line.append(res.get("area"))
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