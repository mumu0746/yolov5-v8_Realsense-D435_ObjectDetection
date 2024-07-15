task: segment  # YOLO task, i.e. detect, segment, classify, pose
mode: train  # YOLO mode, i.e. train, val, predict, export, track, benchmark
 
# Train settings -------------------------------------------------------------------------------------------------------
model: yolov8s-seg.yaml  # path to model file, i.e. yolov8n.pt, yolov8n.yaml
#model:runs/detect/yolov8s/weights/best.pt
data: seg.yaml # path to data file, i.e. coco128.yaml
epochs: 10  # number of epochs to train for
patience: 50  # epochs to wait for no observable improvement for early stopping of training
batch: 16  # number of images per batch (-1 for AutoBatch)