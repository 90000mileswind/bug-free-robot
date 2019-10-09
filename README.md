该项目是为天池的“数字人体”视觉挑战赛写的，只需要把比赛网站上的数据下载下来，修改一下对应的数据读取地址就可以直接训练。

我本地训练跑出来的mAP在40左右，各位同学拿来学习一下YOLOv3算法也够用，参赛可能就还需要更多调整了。

项目基于coco数据集训练结果再训练的，也可以下载对应coco权重yolov3.weights放在./data/darknet文件夹下，后运行convert_weight.py

coco权重yolov3.weights  可以到我的百度云里下载：https://pan.baidu.com/s/1pDwPgFLijqgHagIDeI00LQ

该比赛的特殊图片数据读取器SDK，下载到./kfbreader中即可。文件夹内也有解释

从比赛网站上下载了图片文件夹和标签文件，图片文件夹有10个，一个标签文件夹
修改distribution_data_ymc.py中117、118行中对应的地址，运行这个文件就可以获得你常见的图片了。

开始训练吧！


相互学习共同进步！
