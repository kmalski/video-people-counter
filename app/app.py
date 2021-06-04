from detection import ImageDetector, VideoDetector
import argparse


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", default=None, help="Path to image")
    ap.add_argument("-v", "--video", default=None, help="Path to video")
    return vars(ap.parse_args())


def main():
    args = parse_args()

    image_path = args["image"]
    video_path = args["video"]

    if image_path is not None:
        ImageDetector().detect(image_path)

    if video_path is not None:
        VideoDetector().detect(video_path)


if __name__ == '__main__':
    main()
