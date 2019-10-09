The project is written for Tianchi's "Digital Human Body" Visual Challenge Competition. It can be directly trained by downloading the data from the competition website and modifying the corresponding data reading address.

It's enough for you to learn the YOLOv3 algorithm, and more adjustments may be needed in the competition.

If it helps you, give me a little star.

If the project is retrained based on the results of coco data set training, you can download yolov3. weights corresponding to coco weight and put them in. / data / Darknet folder, then run convert_weight.py.

Coco weight yolov3. weights can be downloaded from my Baidu cloud at https://pan.baidu.com/s/1pDwPgFLijqgHagIDeI00LQ

The special image data reader SDK of the competition can be downloaded to. / kfbreader. There are also explanations in the folder

Picture folders and label files are downloaded from the competition website. There are 10 picture folders and one label folder.

Modify the corresponding address in lines 117 and 118 of distribution_data_ymc.py and run this file to get your usual pictures.

Start training!

Learn from each other and make progress together!
