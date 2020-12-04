"""
#  Copyright (c) 2020. antonio-sc66

This file is part of PyHomeSurveillance.

PyHomeSurveillance is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyHomeSurveillance is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyHomeSurveillance.  If not, see <https://www.gnu.org/licenses/>.
"""

# TODO start recording a few seconds before detecting movements. Create a temp buffer to achieve that
# TODO test in multiple environments

import cv2
import time
from datetime import datetime

import imutils
from imutils.video import WebcamVideoStream, FileVideoStream

# Constants
IN_FPS = 30
INPUT_RES = (1280, 720)  # pixels
OUTPUT_RES = (1280, 720)  # pixels
_PROCESSING_RES = (640, 360)  # pixels
_DIFF_THRESH = 8
_MIN_AREA = 5500
CAP_TIME_AFTER = 15  # seconds
EXP_FILENAME = 'mov_video'
EXP_FORMAT = 'mp4'
EXP_CODEC = 'mp4v'
EXP_PATH = '../'
CAM_ID = 0
SHOW_CAMERA = True

USE_INPUT_VIDEO = False
DEBUG_VID_PATH = "../test_dataset/VIRAT_S_000200_01_000226_000268.mp4"

fourcc = cv2.VideoWriter_fourcc(*EXP_CODEC)
video_writer = cv2.VideoWriter(EXP_PATH + EXP_FILENAME + '.' + EXP_FORMAT, fourcc, IN_FPS, OUTPUT_RES)


def main():
    try:
        if USE_INPUT_VIDEO:
            video_stream = FileVideoStream(DEBUG_VID_PATH)
        else:
            video_stream = WebcamVideoStream(CAM_ID)
            video_stream.stream.set(cv2.CAP_PROP_FPS, IN_FPS)
            video_stream.stream.set(cv2.CAP_PROP_FRAME_WIDTH, INPUT_RES[0])
            video_stream.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, INPUT_RES[1])
        video_stream.start()
    except Exception as e:
        print(e)
        print("\nExiting program\n")

    # Sleep to allow the camera to warm up
    if not USE_INPUT_VIDEO:
        time.sleep(5)

    text_cl = "Clear"
    text_occ = "Occupied"

    # Detection based on:
    # https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
    img_avg = None
    while True:
        start_t = time.time()
        next_it_t = start_t + 1 / IN_FPS
        timestamp = datetime.now()
        frame = video_stream.read()
        if frame is None:
            break
        res_frame = cv2.resize(frame, _PROCESSING_RES)
        gray = cv2.cvtColor(res_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Initialize background with the first img. The background will be updated via image average
        if img_avg is None:
            # print("[INFO] start background definition")
            img_avg = gray.copy().astype("float32")
            continue

        # Accumulate intensity averages
        cv2.accumulateWeighted(gray, img_avg, 0.5)
        # Calculate the difference between current img and average img
        frame_diff = cv2.absdiff(gray, cv2.convertScaleAbs(img_avg))

        thresh = cv2.threshold(frame_diff, _DIFF_THRESH, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        movement = False
        # loop over the contours
        for c in contours:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < _MIN_AREA:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            movement = True

        if movement:
            colour = (0, 0, 255)
            text = text_occ
        else:
            colour = (0, 255, 0)
            text = text_cl
        # draw the text and timestamp on the frame
        ts = timestamp.strftime("%A %d %B %Y--%I:%M:%S%p")
        cv2.putText(frame, "{}".format(text), (15, 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, colour, 2)
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 255, 255), 1)

        out_frame = cv2.resize(frame, OUTPUT_RES)
        video_writer.write(out_frame)

        if SHOW_CAMERA:
            cv2.imshow("Video stream", out_frame)
            cv2.waitKey(1)

        time_to_sleep = next_it_t - time.time()
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    video_stream.stop()
    video_writer.release()


if __name__ == "__main__":
    main()
