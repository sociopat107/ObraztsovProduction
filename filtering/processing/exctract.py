import os

import cv2
import sys

resource_path = '/Users/sfilonov/PycharmProjects/PhotoLab/resources'
path = os.path.join(resource_path, 'telegram-cloud-photo-size-2-5350578246728657937-y.jpg')
image = cv2.imread(path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
)

print("[INFO] Found {0} Faces.".format(len(faces)))

for (x, y, w, h) in faces:
    extra_x = int(w * 0.15)
    extra_y = int(h * 0.30)
    cv2.rectangle(image, (x - extra_x, y - extra_y), (x + w + extra_x, y + h + extra_y), (0, 255, 0), 2)
    roi_color = image[y - extra_y:y+extra_y + h, x-extra_x:x + w+extra_x]
    print("[INFO] Object found. Saving locally.")
    cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)

status = cv2.imwrite('faces_detected.jpg', image)