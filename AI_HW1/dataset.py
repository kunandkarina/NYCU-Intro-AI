import os
import cv2


def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first
    element is the numpy array of shape (m, n) representing the image.
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)

    # 1. Get folder's path (face and non-face)
    # 2. List all files in folder by os.listdir function
    # 3. Read with cv2 in grayscale
    # 4. Append (the info of image, label) into dataset, 0 with non-face / 1 with face
    # 5. Return
    dataset = []

    root = str(dataPath) + "/face/"
    # print(root)
    for image in os.listdir(root):
        dataset.append((cv2.imread(root+image, cv2.IMREAD_GRAYSCALE), 1))

    root = str(dataPath) + "/non-face/"
    for image in os.listdir(root):
        dataset.append((cv2.imread(root+image, cv2.IMREAD_GRAYSCALE), 0))
    # End your code (Part 1)
    return dataset
