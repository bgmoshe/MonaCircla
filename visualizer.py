'''
 This function can get as an input
 '''

import cv2
import numpy as np
DEFAULT_FPS = 4


def visualize(frames, video_name="animated_result.avi", fps=DEFAULT_FPS):
    width, height = frames[0].size
    video = cv2.VideoWriter(video_name, 0, fps, (width, height))
    for image in frames:
        pil_image = image.convert("RGB")
        opencvimage = np.array(pil_image)
        opencvimage = opencvimage[:, :, ::-1]
        video.write(opencvimage)
    cv2.destroyAllWindows()
    video.release()
