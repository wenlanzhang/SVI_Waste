from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import mmcv
import os
import csv
from tqdm import tqdm  # 用于显示进度条

# config_file = '../_myconfigs/pascal_voc/faster_rcnn_r50_fpn_1x_voc0712_SE.py'
config_file = '../_myconfigs/pascal_voc/faster_rcnn_r50_fpn_1x_voc0712_all_layer_SE_with_ClassBalancedDataset_and_low_nms_score_config_and_data_augumentation.py'
checkpoint_file = '../checkpoint_backup/epoch_48.pth'

# build the model from a config file and a checkpoint file
model = init_detector(config_file, checkpoint_file, device='cuda:0')

root = './batch_inference_data/'

# 创建/打开 result.csv 文件
csv_file_path = os.path.join(root, 'result.csv')
with open(csv_file_path, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # 写入表头
    csv_writer.writerow(['tile_row', 'tile_col', 'x_min', 'y_min', 'x_max', 'y_max', 'confidence_score', 'Class'])

    root_path = root

    # 使用 tqdm 包裹文件列表，显示进度条
    for _, dirs, files in os.walk(root_path):
        # 使用 tqdm 进度条包裹 files
        for file in tqdm(files, desc="Processing files", unit="file"):
            img_path = os.path.join(root_path, file)

            try:
                # Check if the file exists
                if not os.path.exists(img_path):
                    print(f"File not found: {img_path}")
                    continue

                # Manually check if the image can be loaded
                img = mmcv.imread(img_path)
                if img is None:
                    print(f"Error loading image: {img_path}")
                    continue

                # Perform inference
                results = inference_detector(model, img_path)

                # Parse tile_row and tile_col
                if '_tile_' in file:
                    file_parts = file.split('_')
                    tile_row = file_parts[2]  # Extract row info
                    tile_col = file_parts[3].split('.')[0]  # Extract col info and remove extension
                else:
                    tile_row = "N/A"
                    tile_col = "N/A"

                # Process results if not empty
                for class_id, class_result in enumerate(results):
                    if len(class_result) == 0:
                        continue
                    for detection in class_result:
                        x_min, y_min, x_max, y_max, confidence_score = detection
                        if confidence_score >= 0.3:
                            # 写入 CSV
                            csv_writer.writerow([tile_row, tile_col, x_min, y_min, x_max, y_max, confidence_score, model.CLASSES[class_id]])

                # 保存带有检测框的图像
                model.show_result(img_path, results, font_size=8,
                                  out_file=os.path.join(root, 'inference_visualization', file))

            except Exception as e:
                # 打印错误信息，并继续处理下一个文件
                print(f"Error processing file {file}: {e}")
                continue
