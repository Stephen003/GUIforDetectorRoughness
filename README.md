# 粗糙度检测 摄像头读取 图像处理GUI

2021/02/22

摄像头读取不出。对于camera.py, line 117 frame读取不到为NoneType

解决方法：在cv2.VideoCapture() 添加cv2.CAP_DSHOW 改为cv2.VideoCapture(self.CAM_NUM + cv2.CAP_DSHOW)