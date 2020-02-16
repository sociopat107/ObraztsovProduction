import os

import numpy as np
import cv2
from matplotlib import pyplot as plt

resource_path = '/Users/sfilonov/PycharmProjects/PhotoLab/resources'
path = os.path.join(resource_path, 'telegram-cloud-photo-size-2-5350578246728657937-y.jpg')
img = cv2.imread(path)
mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
)

for (x, y, w, h) in faces:
    mask[cv2.GC_FGD] = (x + x + w) / 2
    extra_x = int(w * 0.15)
    extra_y = int(h * 0.30)
    rect = (x, y - extra_y, w, h + extra_y)


cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img = img * mask2[:, :, np.newaxis]

plt.imshow(img)
plt.colorbar()
plt.show()
