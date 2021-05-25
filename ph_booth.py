from __future__ import print_function
from photoapp import PhotoApp
from imutils.video import VideoStream
import argparse
import time
 
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default='../data/faces/folder',
	help="path to output directory to store snapshots")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-n", "--nameofp", required=True, help="name of person")
args = vars(ap.parse_args())
 
# initialize the video stream and allow the camera sensor to warmup
# print("[INFO] warming up camera...")
#vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
# time.sleep(1.0)
 
# start the app
pba = PhotoApp(args["output"], args["nameofp"])
pba.root.mainloop()