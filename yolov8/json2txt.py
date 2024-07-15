# -*- coding: utf-8 -*-
import json
import os
import argparse
from tqdm import tqdm
 
 
def convert_label_json(json_dir, save_dir, classes):
    json_paths = os.listdir(json_dir)
    classes = classes.split(',')
 
    for json_path in tqdm(json_paths):
        # for json_path in json_paths:
        path = os.path.join(json_dir, json_path)
        with open(path, 'r') as load_f:
            json_dict = json.load(load_f)
        h, w = json_dict['imageHeight'], json_dict['imageWidth']
 
        # save txt path
        txt_path = os.path.join(save_dir, json_path.replace('json', 'txt'))
        txt_file = open(txt_path, 'w')
 
        for shape_dict in json_dict['shapes']:
            label = shape_dict['label']
            label_index = classes.index(label)
            points = shape_dict['points']
 
            points_nor_list = []
 
            for point in points:
                points_nor_list.append(point[0] / w)
                points_nor_list.append(point[1] / h)
 
            points_nor_list = list(map(lambda x: str(x), points_nor_list))
            points_nor_str = ' '.join(points_nor_list)
 
            label_str = str(label_index) + ' ' + points_nor_str + '\n'
            txt_file.writelines(label_str)
 
 
if __name__ == "__main__":
    """
    python json2txt_nomalize.py --json-dir my_datasets/color_rings/jsons --save-dir my_datasets/color_rings/txts --classes "cat,dogs"
    """
    parser = argparse.ArgumentParser(description='json convert to txt params')
    parser.add_argument('--json-dir', type=str,default='data/json', help='json path dir')
    parser.add_argument('--save-dir', type=str,default='data/txt' ,help='txt save dir')
    parser.add_argument('--classes', type=str, default='pallet,hole',help='classes')
    args = parser.parse_args()
    json_dir = args.json_dir
    save_dir = args.save_dir
    classes = args.classes
    convert_label_json(json_dir, save_dir, classes)