import os
import random

if __name__ == '__main__':
    trainval_percent = 1.0
    train_percent = 0.9
    xmlfilepath = "/Users/wenlanzhang/Downloads/PhD_UCL/Data/GoogleStreetView/Train/Train0315/images"  # Use image path here
    txtsavepath = "/Users/wenlanzhang/Downloads/PhD_UCL/Data/GoogleStreetView/Train/Train0315/dataSet"
    total_xml = os.listdir(xmlfilepath)
    if not os.path.exists(txtsavepath):
        os.makedirs(txtsavepath)

    num = len(total_xml)
    list_index = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list_index, tv)
    train = random.sample(trainval, tr)

    file_trainval = open(txtsavepath + '/trainval.txt', 'w')
    file_test = open(txtsavepath + '/test.txt', 'w')
    file_train = open(txtsavepath + '/train.txt', 'w')
    file_val = open(txtsavepath + '/val.txt', 'w')

    for i in list_index:
        filename_parts = total_xml[i].split('.')
        name = xmlfilepath + "/" + filename_parts[0] + '.' + filename_parts[1] + '\n'
        if i in trainval:
            file_trainval.write(name)
            if i in train:
                file_train.write(name)
            else:
                file_val.write(name)
        else:
            file_test.write(name)

    file_trainval.close()
    file_train.close()
    file_val.close()
    file_test.close()