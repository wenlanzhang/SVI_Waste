from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("E:\WorkSpace\SVI_Waste\waste27.pt")
    res_list = model('E:\WorkSpace\SVI_Waste\Data\\135\images\\0b29b847-4bGnLjKNVCN24NAYnp1cgw_0.jpg', imgsz=(400,300), conf=0.6, device=0)
    for r in res_list:
        p = r.boxes.cpu().conf.numpy()[0]
        print(p)