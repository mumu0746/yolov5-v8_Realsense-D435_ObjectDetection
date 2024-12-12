# yolov5-v8_Realsense-D435_ObjectDetection
### 0 前言
1. 使用YoloV5/V8进行目标检测，并包含其他功能性python代码，注意：数据集需要自己制作（照片和txt文件）
2. 如果要进一步得到目标中心点的三维坐标，则刚需**Intel Realsense摄像机**
3. 下面对本仓库的文件夹做一些说明

### 1 yolov8
1. 包含：**yolov8模型训练**的使用说明，但只能以图片或者拍好的视频进行目标检测实例分割
2. 如果想要将其运用到项目当中，比如我所负责的智能叉车和苹果采摘项目，最好是通过摄像头的实时识别，因此，文件夹中的video.py即为使用**Intel Realsense D435双目深度摄像机**，将训练好的.pt模型权重文件导入，进行实时识别的python代码，同样，也简单写好了video.py的使用说明

### 2 yolov5
1. 最初的项目运用的是yolov5进行目标识别，但由于我们需要精确得到目标物体的三维坐标点，因此采用实例分割+多边形拟合算法是更好的选择，但困于**yolov5没有实例分割这一功能**，最终无奈放弃
2. 但是yolov5的使用教程还是打算写一写，因为如果只是单纯的简单的目标检测，yolov5已经够用，目的是为初学者提供一些捷径，少走一些弯路

### 3 数据集加工
1. 包含：将xml文件转换为txt文件
2. 包含：计算使用labelme打标签的标签总数
3. 包含：令图片和标签**一一对应**的python代码，例如你原本有10w张照片，但是你只用labelme打了3w张，如果还不是按顺序进行的，这时候你会苦恼如何将标签和图片一一对应，虽然训练时图片和标签可以不用一一对应，但是10w张照片内存确实太大了，因此使用此脚本可以自动筛选，原理就是通过标签名和图片名一致来筛选
4. 包含：将彩色RGB图片转换为灰度图的python文件
5. 包含：将已拍摄好的视频，按每x帧抽取为图片并保存到一个文件夹里面的python代码，多用于拍摄制作大量数据集的时候

### 4 接口
1. 包含：使用HTTP进行数据传输的python代码
2. 包含：使用TCPIP进行数据传输的python代码

### 5 Best大全！
1. 包含：智能叉车和苹果采摘项目所训练过的模型权重文件（不全，涉及公司机密，只能将暂时废弃的发出来）
2. 包含：将yolov8模型训练的.pt权重文件，转换为.onnx文件，再由.onnx文件转换为.blob文件，附说明文档

### 6 拍照
1. 包含：使用普通单目和双目（两个单目组合）摄像机拍摄视频
2. 包含：使用Intel Realsense摄像机拍摄视频

### 7 精度测量
1. 包含：终端输入两个三维点坐标，自动计算两点欧式距离

### 8 Intel Realsense D435(i)内外参标定
1. 作用：可使识别出来的三维坐标更加精确
2. 本文档中，棋盘格适用于D435相机标定，需要ROS1环境
3. 文件还包含了D435i的一些使用Kalibr标定的结果，但是缺少标定操作，原因是当时对其标定结果并不满意，就没有继续进行下去，也许后面会重新拾起来
