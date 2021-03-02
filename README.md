# 粗糙度检测 摄像头读取 图像处理GUI

2021/02/22

摄像头读取不出。对于camera.py, line 117 frame读取不到为NoneType

解决方法：在cv2.VideoCapture() 添加cv2.CAP_DSHOW 改为cv2.VideoCapture(self.CAM_NUM + cv2.CAP_DSHOW)

2021/03/02

添加程序，能够读取图片，用于测试。

今日实现：固定label界面大小，能够计算得出粗糙度值(不一定对，计算过程之后再调整)

未实现功能：视频同步处理