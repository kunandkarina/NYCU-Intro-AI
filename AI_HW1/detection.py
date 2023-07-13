import os
import cv2
import csv
import matplotlib.pyplot as plt


def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")
    # 1.Create four list(x,y,w,h) x for x cordinate, y for y cordinate, w for width, h for height
    # 2.Convert the txt file to lines in list
    # 3.Transfer input into load data
    #   1.Get the file name(s[0]) and the number of squares(s[i])
    #   2.Get every squares' parameter and convert the string into int and store into list(x,y,w,h)
    # 4.Read image in cv2 with grayscale
    # 5.Convert grayscale's image into 19*19 grayscale image with its parameter of squares
    # 6.Use clf.classfy to judge whether the image is face
    # 7.Draw green or red square with the parameter
    # 8.Store the image results in belonging file and show it
    x, y, w, h = [], [], [], []
    with open(dataPath) as f:
        while True:
            x, y, w, h = [], [], [], []
            line = f.readline()
            s = line.split(' ')
            if not line:
                break
            # int("s[1]")
            # print(type(int(s[1])))
            for i in range(int(s[1])):
                line = f.readline()
                str = line.split(' ')
                x.append(int(str[0]))
                y.append(int(str[1]))
                w.append(int(str[2]))
                h.append(int(str[3]))
            image = cv2.imread("data/detect/" + s[0])
            image_cmp = cv2.imread(
                "data/detect/" + s[0], cv2.IMREAD_GRAYSCALE)
            for i in range(int(s[1])):
                face_image = cv2.resize(
                    image_cmp[y[i]:y[i]+h[i], x[i]:x[i]+w[i]], (19, 19), interpolation=cv2.INTER_LINEAR)
                if clf.classify(face_image) == 1:
                    cv2.rectangle(image, (x[i], y[i]), (x[i] +
                                                        w[i], y[i] + h[i]), (0, 255, 0), thickness=2)
                else:
                    cv2.rectangle(image, (x[i], y[i]), (x[i] +
                                                        w[i], y[i] + h[i]), (0, 0, 255), thickness=2)
            cv2.imwrite("result/test/test_"+s[0], image)
            image = cv2.imread("result/test/test_"+s[0])
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            plt.imshow(image)
            plt.show()
    # End your code (Part 4)
