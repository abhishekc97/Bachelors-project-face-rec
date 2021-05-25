from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import subprocess

class PhotoApp:
	def __init__(self, outputPath, nameofp):
		#self.vs = vs
		self.outputPath = outputPath
		self.nameofp = nameofp
		self.frame = None

		#self.directory = ''#tki.StringVar(Tk())

		#self.directory = directory
		# self.thread = None
		# self.stopEvent = None
		#fname = getname()
 
		self.root = tki.Tk()
		self.root.geometry("500x300")
		self.panel = None

		lforb1 = tki.Label(self.root, text='Enter name')
		lforb1.grid(column =0, row=0)

		entry1 = tki.Entry()
		entry1.grid(column=1,row=0)
		#name = str(entry1.get())

		#btn0 = tki.Button(self.root, text ='submit name', command = )

		b1 = tki.Button(self.root, text = 'Add new user', command = lambda:self.newuser(self.nameofp,self.outputPath), width = 10, height=5)
		b1.grid(column=2 , row=0)

		btn = tki.Button(self.root, text="Click a picture", command=lambda:self.takeSnapshot(self.nameofp, self.outputPath), width =10, height = 5) #, self.directory
		#btn.pack( padx=10, pady=10)
		btn.grid(column =0, row=1)

		btn2 = tki.Button(self.root, text="Train", command=self.addfacerunner, width =10, height = 5)
		#btn2.pack( padx=10, pady=10)
		btn2.grid(column =1, row=1)

		btn3 = tki.Button(self.root, text="Recognize", command=self.recog, width =10, height = 5)
		btn3.grid(column =2, row=1)  		#btn3.pack( padx=10, pady=10) # side="bottom", fill="both", expand="yes",
 		
		

		#display = tki.Text(self.root, width =10,height = 5)
		#display.grid(column=0,row=2)
 		#self.stopEvent = threading.Event()
		#self.thread = threading.Thread(target=self.videoLoop, args=())
		#self.thread.start()
		self.root.wm_title("PhotoBooth")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

		# self.frame = self.vs.read()
		# self.frame = imutils.resize(self.frame, width=300)
		
		# image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
		# image = Image.fromarray(image)
		# image = ImageTk.PhotoImage(image)
		
		# videopanel = tki.Label(self.root, image =image)
		# videopanel.grid(row = 2)

	def newuser(self,nameofp,outputPath):
		#nameforfolder = str(entry1.get())
		#global directory
		ogpath = '/home/abhishek/Desktop/master/data/faces'
		newdirectorystring = os.path.join(ogpath,self.nameofp) #nameforfolder
		os.mkdir(newdirectorystring)
		print('folder created at {} '.format(newdirectorystring))
		#directory.set(fo)
		#copydir(directory)

	#def copydir(directory):
		#finaldir = self.directory
		#return 

	def getname():
		nameforfolder = str(entry1.get())
		return nameforfolder



	def takeSnapshot(self, nameofp, outputPath):   #, directory
		#ts = datetime.datetime.now()
		#filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
		#os.mkdir(self.outputPath,self.nameofp)
		#newloc = 
		

		#filename = "{}.jpg".format(self.nameofp)
		#p = os.path.sep.join((self.outputPath, filename))
 
		# save the file
		#cv2.imwrite(p, self.frame.copy())
		#print("[INFO] saved {}".format(filename))
		#subprocess.call(['python','takesnap.py','-n','abh'])
		
		self.nameofp = nameofp
		self.outputPath = outputPath
		#self.directory = directory
		cam = cv2.VideoCapture(0)

		cv2.namedWindow("Camera")

		img_counter = 0

		while True:
			ret, frame = cam.read()
			cv2.imshow("Camera", frame)
			if not ret:
				break
			k = cv2.waitKey(1)
			if k%256 == 27:
				print("Escape hit, closing...")
				break
			elif k%256 == 32:
				# SPACE pressed
				img_name = "{}.jpg".format(self.nameofp)

				path = self.outputPath #self.directory
				#xpath = os.path.join(path,img_name)
				cv2.imwrite(os.path.join(path,img_name), frame)

				#cv2.imwrite(img_name, frame)

				print("{} stored !".format(img_name))
				img_counter += 1
		cam.release()

		cv2.destroyAllWindows()
	def addfacerunner(self):
		#self.stopEvent = threading.Event()
		subprocess.call(['python','addface.py'])

	def recog(self):
		subprocess.call(['python','testVideo.py'])

	def onClose(self):
		print("[INFO] closing...")
		self.root.quit()

	#def createFolder(self):
