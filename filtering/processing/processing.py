import os

import numpy as np
import cv2

# from django.conf import settings

# resource_path = settings.RESOURCES_PATH

resource_path = '/Users/sfilonov/PycharmProjects/PhotoLab/resources'

video_path = os.path.join(resource_path, 'neon.mp4')

cap = cv2.VideoCapture(video_path)

while cap:
    # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

