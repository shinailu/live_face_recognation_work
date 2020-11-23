# coding:utf-8
import dlib
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import sys
import torch
import cv2
from imgaug import augmenters as iaa
import numpy as np
import  torch.nn.functional as F
from collections import  OrderedDict


RESIZE_SIZE =112



class FaceSpoofing(object):
    def __init__(self):
        from FaceBagNet_model_A import Net
        self.net = Net(num_class=2, is_first_bn=True)
        model_path = 'face_mask_detection.pth'
        if torch.cuda.is_available():
            state_dict = torch.load(model_path, map_location='cuda')
        else:
            state_dict = torch.load(model_path, map_location='cpu')
        new_state_dict = OrderedDict
        for k, v in state_dict.items():
            name = k[7:]
            new_state_dict[name] = v
        self.net.load_state_dict(new_state_dict)
        if torch.cuda.is_available():
            self.net = self.net.cuda()

    def classify(self, color):
        color = cv2.resize(color, (RESIZE_SIZE, RESIZE_SIZE))
        def color_augumentor(image, target_shape=(64, 64, 3), is_infer=False):
            if is_infer:
                augment_img = iaa.Sequential([iaa.Fliplr(0)])
            image = augment_img.augment_image(image)
            image = TTA_36_cropps(image, target_shape)
            return image

        color = color_augumentor(color, target_shape=(64, 64, 3), is_infer=True)
        n = len(color)
        color = np.concatenate(color, axis=0)
        image = color
        image = np.transpose(image, (0, 3, 1, 2))
        image = image.astype(np.float32)
        image = image / 255.0
        input_image = torch.FloatTensor(image)
        if (len(input_image.size()) == 4) and torch.cuda.is_available():
            input_image = input_image.unsqueeze(0).cuda()
        elif (len(input_image.size()) == 4) and not torch.cuda.is_available():
            input_image = input_image.unsqueeze(0)

        b, n, c, w, h = input_image.size()
        input_image = input_image.view(b * n, c, w, h)
        if torch.cuda.is_available():
            input_image = input_image.cuda()

        with torch.no_grad():
            logit, _, _ = self.net(input_image)
            logit = logit.view(b, n, 2)
            logit = torch.mean(logit, dim=1, keepdim=False)
            prob = F.softmax(logit, 1)
        return np.argmax(prob.detach().cpu().numpy())


def TTA_36_cropps(image, target_shape=(32, 32, 3)):
           image = cv2.resize(image, (RESIZE_SIZE, RESIZE_SIZE))

           width, height, d = image.shape
           target_w, target_h, d = target_shape

           start_x = (width - target_w) // 2
           start_y = (height - target_h) // 2

           starts = [[start_x, start_y],

                     [start_x - target_w, start_y],
                     [start_x, start_y - target_w],
                     [start_x + target_w, start_y],
                     [start_x, start_y + target_w],

                     [start_x + target_w, start_y + target_w],
                     [start_x - target_w, start_y - target_w],
                     [start_x - target_w, start_y + target_w],
                     [start_x + target_w, start_y - target_w],
                     ]

           images = []

           for start_index in starts:
               image_ = image.copy()
               x, y = start_index

               if x < 0:
                   x = 0
               if y < 0:
                   y = 0

               if x + target_w >= RESIZE_SIZE:
                   x = RESIZE_SIZE - target_w - 1
               if y + target_h >= RESIZE_SIZE:
                   y = RESIZE_SIZE - target_h - 1

               zeros = image_[x:x + target_w, y: y + target_h, :]

               image_ = zeros.copy()

               zeros = np.fliplr(zeros)
               image_flip_lr = zeros.copy()

               zeros = np.flipud(zeros)
               image_flip_lr_up = zeros.copy()

               zeros = np.fliplr(zeros)
               image_flip_up = zeros.copy()

               images.append(image_.reshape([1, target_shape[0], target_shape[1], target_shape[2]]))
               images.append(image_flip_lr.reshape([1, target_shape[0], target_shape[1], target_shape[2]]))
               images.append(image_flip_up.reshape([1, target_shape[0], target_shape[1], target_shape[2]]))
               images.append(image_flip_lr_up.reshape([1, target_shape[0], target_shape[1], target_shape[2]]))

           return images
if __name__=="__main__":
    # 初始化人脸检测模型
    detector = dlib.get_frontal_face_detector()
    ## 填空 初始化活体检测模型
    face_spoofing = FaceSpoofing()
    # 初始化关键点检测模型
    predictor = dlib.shape_predictor(r'./shape_predictor_68_face_landmarks.dat')
    # 初始化人脸特征模型
    recognition = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    face_feature_zmm = dlib.vector([-0.107805, 0.0533189, 0.0738411, -0.00247142, -0.0780798, -0.0856904, 0.021062, -0.141694, 0.129174, -0.103851, 0.297461, -0.0970184, -0.227256, -0.126665, -0.00331379, 0.181802, -0.107472, -0.119393, -0.0616112, 0.0131635, 0.0843931, -0.0221636, 0.0352314, 0.02019, -0.0664978, -0.331813, -0.109752, -0.0937842, -0.00590822, -0.0519546, -0.082456, 0.0678473, -0.164168, -0.138727, 0.0175497, 0.0612009, -0.0310678, -0.0434677, 0.225786, -0.0525931, -0.222896, -0.0113799, 0.0183438, 0.250612, 0.106143, 0.0319014, 0.0472741, -0.139323, 0.0688046, -0.149782, 0.0692678, 0.116915, 0.111519, 0.0260728, -0.0027499, -0.137331, 0.0125463, 0.0837388, -0.0996596, 0.00247323, 0.115559, -0.0600351, -0.0514504, -0.071504, 0.243651, 0.0370934, -0.110954, -0.125839, 0.103903, -0.0721743, -0.0614288, 0.038291, -0.210036, -0.184005, -0.315377, 0.0437733, 0.418258, 0.0147277, -0.231583, 0.0272667, -0.0833461, 0.00939051, 0.152288, 0.152995, 0.0159023, 0.0533869, -0.115206, 0.0158737, 0.178567, -0.135734, -0.0382685, 0.187186, 0.0112544, 0.0785103, 0.0320245, 0.0142644, -0.00127718, 0.0480519, -0.127891, 0.0294824, 0.10632, -0.023961, -0.0272707, 0.110732, -0.148478, 0.0798191, 0.0280322, 0.0498265, 0.0476104, -0.0355732, -0.107883, -0.12456, 0.107062, -0.187653, 0.148096, 0.17608, 0.011524, 0.0993421, 0.102652, 0.0936368, 0.0146759, 0.0243123, -0.241052, 0.0157876, 0.154274, 0.0359561, 0.0525588, 0.0118183])
    # 从摄像头读取图像, 若摄像头工作不正常，可使用：cv2.VideoCapture("week20_video3.mov"),从视频中读取图像
    cap = cv2.VideoCapture(0)
    while 1:
        # 初始化人脸相似度为-1
        similarity=-1
        # 读取图片
        ret, frame_src = cap.read()
        # 将图片缩小为原来大小的1/3
        x, y = frame_src.shape[0:2]
        frame = cv2.resize(frame_src, (int(y / 3), int(x / 3)))
        face_align = frame
        # 使用检测模型对图片进行人脸检测
        dets = detector(frame, 1)
        #import pdb
        #pdb.set_trace()
        # 便利检测结果
        for det in dets:
            # 对检测到的人脸提取人脸关键点
            shape=predictor(frame, det)
            #print("x=%s,y=%s,w=%s,h=%s"%(det.left(),det.top(),det.width(),det.height()))
            # 在图片上绘制出检测模型得到的矩形框,框为绿色
            frame=cv2.rectangle(frame,(det.left(),det.top()),(det.right(),det.bottom()),(0,255,0),2)
            #import pdb
            #pdb.set_trace()
            # 人脸对齐
            face_align=dlib.get_face_chip(frame, shape, 150,0.1)
            is_attack_str ='live'
            ## 活体检测
            if not face_spoofing.classify(face_align):
                 print(" not humman\n ")
                # 框为红色
                 frame=cv2.rectangle(frame,(det.left(),det.top()),(det.right(),det.bottom()),(0,0,255),2)
            # 提取人脸特征
            face_feature=recognition.compute_face_descriptor(face_align)
            print('face_feature:',face_feature)
            # 计算人脸相似度
            similarity=1-np.linalg.norm(np.array(face_feature)-np.array(face_feature_zmm))
            # 将关键点绘制到人脸上，
            for i in range(68):
                cv2.putText(frame, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_DUPLEX, 0.3, (0, 255, 255), 1,cv2.LINE_AA)
                cv2.circle(frame, (shape.part(i).x, shape.part(i).y), 1, (0, 0, 255))
        #print(dets.rectangles)
        # 为了显示出相似度，我们将相似度写到图片上，
        cv2.putText(frame,"similarity=%s,%s"%(similarity,is_attack_str),(100,200),cv2.FONT_HERSHEY_DUPLEX, 0.3, (0, 255, 255), 1,cv2.LINE_AA)
        # 显示图片，图片上有矩形框，关键点，以及相似度
        cv2.imshow("capture", cv2.resize(frame,(y,x)))
        #cv2.imshow("face_align",face_align)
        if cv2.waitKey(100) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()