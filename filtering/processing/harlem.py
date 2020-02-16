import itertools
import os
import random
from collections import defaultdict

import numpy as np
import cv2

from filtering.processing.photo_api import get_video

FRAMES_PER_SECOND = 12
VIDEO_LEN_SECONDS = 15

SPRITES_COUNT = 4

RESOURCE_PATH = '/Users/sfilonov/PycharmProjects/PhotoLab/resources'
DANCE_PATH = os.path.join(RESOURCE_PATH, 'dance_animations')


def _animation_yield(sprites):
    for element in itertools.cycle(sprites):
        yield element


def video_frames_iter():
    onlyfiles = [f for f in os.listdir('video')]
    for element in itertools.cycle(onlyfiles):
        yield cv2.imread(os.path.join('video', element))


def video_by_frames(url):
    vidcap = cv2.VideoCapture(url)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(f"video/frame{count}d.jpg", image)
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1


def _offsets_yield(offsets):
    for element in offsets:
        yield element


def get_file(path):
    return open(path, 'rb')


class VideoMaker:

    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(path)
        self.height, self.width, self.layers = self.img.shape
        self.face_roi = self._get_face_roi()
        self.animations = self._init_animations()
        self.offset_mapping = {
            'girl1': (50, 50),
            'mario': ('str', 50),
            'spange': (50, 'str'),
            'girl_blue': ('str', 'str')
        }

    def _get_face_roi(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            return x, y, w, h

    def __pick_random_animations(self, animations):
        if len(animations) <= SPRITES_COUNT:
            return animations.values()
        return random.choices(animations.values(), k=SPRITES_COUNT)

    def __group_animations_by_dir(self, animations):
        groups = defaultdict(list)
        for path in animations:
            folder = os.path.basename(os.path.normpath(os.path.dirname(path)))
            groups[folder].append(path)
        for key, value in groups.items():
            groups[key] = _animation_yield(value)

        return groups

    def _init_animations(self):
        animations = []
        for dirname, dirnames, filenames in os.walk(DANCE_PATH):
            for filename in filenames:
                    animations.append(os.path.join(dirname, filename))
        grouped = self.__group_animations_by_dir(animations)
        return self.__pick_random_animations(grouped)

    def get_offset_for_animation(self, path):
        return 50, 50
        folder = os.path.basename(os.path.normpath(os.path.dirname(path)))
        x, y = self.offset_mapping[folder]
        if all((isinstance(x, int), isinstance(x, int))):
            return 50, 50
        elif all((isinstance(x, str), isinstance(y, str))):
            return self.img.shape[0], self.img.shape[1]
        elif isinstance(x, int):
            return self.img.shape[0], 50
        elif isinstance(y, int):
            return 50, self.img.shape[1]
        return self.offset_mapping[folder]

    @staticmethod
    def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
        """
        @brief      Overlays a transparant PNG onto another image using CV2

        @param      background_img    The background image
        @param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
        @param      x                 x location to place the top-left corner of our overlay
        @param      y                 y location to place the top-left corner of our overlay
        @param      overlay_size      The size to scale our overlay to (tuple), no scaling if None

        @return     Background image with overlay on top
        """

        bg_img = background_img.copy()

        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

        # image to RGB(3 dimensional), extract alpha
        b, g, r, a = cv2.split(img_to_overlay_t)
        overlay_color = cv2.merge((b, g, r))

        # edge noise removal
        mask = cv2.medianBlur(a, 5)

        h, w, _ = overlay_color.shape
        roi = bg_img[y:y + h, x:x + w]

        # Black-out the area behind the logo in our original ROI
        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))

        # Mask out the logo from the logo image.
        img2_fg = cv2.bitwise_and(overlay_color, overlay_color, mask=mask)

        # Update the original image with our new ROI
        bg_img[y:y + h, x:x + w] = cv2.add(img1_bg, img2_fg)

        return bg_img

    def put_animations_over(self, img, animations, face_region=None):
        occupied = []
        for animation in animations:
            sprite_path = next(animation)
            sprite = cv2.imread(sprite_path, -1)
            x_offset, y_offset = self.get_offset_for_animation(sprite_path)
            img = self.overlay_transparent(img, sprite, x_offset, y_offset)

        return img

    def run(self):
        out = cv2.VideoWriter('project.mp4',
                              cv2.VideoWriter_fourcc(*'MP4V'),
                              FRAMES_PER_SECOND,
                              (self.width, self.height))
        file = get_file(self.path)
        video_url = get_video(file)
        video_by_frames(video_url)
        videos = video_frames_iter()
        for i in range(int(VIDEO_LEN_SECONDS * FRAMES_PER_SECOND)):
            if i > 12 * 8:
                self.img = next(videos)
                frame = self.put_animations_over(self.img, self.animations, self.face_roi)
            else:
                frame = self.img
            out.write(frame)
        out.release()


if __name__ == '__main__':
    path = os.path.join(RESOURCE_PATH, 'telegram-cloud-photo-size-2-5350578246728657937-y.jpg')
    video_maker = VideoMaker('photo_2020-02-16_16-20-29.jpg')
    video_maker.run()
