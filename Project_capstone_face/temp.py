from tkinter import *
import os
from PIL import Image
import cv2
import numpy as np
import sqlite3
from tkinter import filedialog
import tkinter.messagebox

class Face_Recog:
    def __init__(self, master):
        self.master = master
        master.title("Face Recognizer")
        #master.geometry("1280x720")
        #master.configure(background = 'blue')

        self.id_lbl = Label(self.master, text="Enter ID",
                         fg="white", bg="black", font=('comic', 15, ' bold '))
        self.id_lbl.place(x=65, y=70)

        self.id_txt = Entry(self.master, width=20, bg="black",
                         fg="white", font=('comic', 15, ' bold '))
        self.id_txt.place(x=220, y=70)

        self.nm_lbl = Label(self.master, text="Enter Name",
                             fg="white", bg="black", font=('comic', 15, ' bold '))
        self.nm_lbl.place(x=65, y=120)

        self.nm_txt = Entry(self.master,
                             fg="white", bg="black", font=('comic', 15, ' bold '))
        self.nm_txt.place(x=220, y=120)

        #self.lbl3 = Label(self.master, text="Notification : ", width=20,
        #                  fg="red", bg="yellow", height=2, font=('times', 15, ' bold underline '))
        #self.lbl3.place(x=400, y=400)

        self.message = Label(self.master, text="", bg="white", fg="red", width=30, height=1, activebackground="yellow",
                           font=('times', 15, ' bold '))
        self.message.place(x=80, y=200)

        #self.clearButton = Button(self.master, text="Clear", command=clear, fg="red", bg="yellow", width=20, height=2,
        #                        activebackground="Red", font=('times', 15, ' bold '))
        #self.clearButton.place(x=950, y=200)


        self.takeImg = Button(self.master, text="Take Images", command=self.TakeImages, fg="white", bg="black",
                            activebackground="Red", font=('times', 15, ' bold '))
        self.takeImg.place(x=65, y=280)


        self.trainImg = Button(self.master, text="Train Images", command=self.TrainImages, fg="white", bg="black",
                               activebackground="Red", font=('times', 15, ' bold '))
        self.trainImg.place(x=250, y=280)
        #trackImg = Button(self.master, text="Track Images", command=TrackImages, fg="red", bg="yellow", width=20,
        #                     height=3, activebackground="Red", font=('times', 15, ' bold '))
        #self.trackImg.place(x=800, y=500)
        #self.quitWindow = Button(self.master, text="Quit", command=self.master.destroy, fg="red", bg="yellow", width=20, height=3,
        #                       activebackground="Red", font=('times', 15, ' bold '))
        #self.quitWindow.place(x=1100, y=500)

    def insertOrUpdate(self,id, name):
        self.id = int(id)
        self.conn = sqlite3.connect("Project_DB.db")
        self.cmd = "Select * from data where id =" + str(id)
        self.cursor = self.conn.execute(self.cmd)
        self.isRecordExist = 0
        for row in self.cursor:
            self.isRecordExist = 1
        if self.isRecordExist == 1:
            # cmd = "Update Homosapiens set Name = "+str(name)+" Where id = "+str(id)
            self.cmd = "UPDATE data SET Name=' " + str(name) + " ' WHERE ID=" + str(self.id)
        else:
            # cmd = "Insert into Homosapiens(ID,Name) values("+str(id)+","+str(name)+")"
            self.cmd = "INSERT INTO data(ID,Name) Values(" + str(self.id) + ",' " + str(name) + " ' )"
        self.conn.execute(self.cmd)
        self.conn.commit()
        self.conn.close()

    def TakeImages(self):
        id = str(self.id_txt.get())
        name = str(self.nm_txt.get())
        if ( id.isnumeric() and name.isalpha() ): #check id is int
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            cap = cv2.VideoCapture(0)
            #id = input('Enter user id')  # make automatic id or check for existing id
            #name = input('Enter name')
            self.insertOrUpdate(id, name)
            samplenum = 0

            while True:
                ret, img = cap.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)  # returns coordinates

                for (x, y, w, h) in faces:
                    samplenum = samplenum + 1
                    cv2.imwrite("proj_dataSet/Users." + str(id) + "." + str(samplenum) + ".jpg",
                                gray[y:y + h, x:x + w])  # region of image
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.waitKey(100) #wait for 100 millisec

                cv2.imshow('Image', img)
                # k = cv2.waitKey(10) & 0xFF
                # if k == 27:
                #    break
                cv2.waitKey(1)
                if samplenum >= 60:
                    break

            cap.release()
            cv2.destroyAllWindows()
        else:
            if (id.isnumeric()):
                res = "Enter Alphabetical Name"
                self.message.configure(text=res)
            if (name.isalpha()):
                res = "Enter Numeric Id"
                self.message.configure(text=res)


    def TrainImages(self ):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.path = 'proj_dataSet'
        self.Ids, self.faces = self.getImageWithID(self.path)
        self.recognizer.train(self.faces, self.Ids)
        self.recognizer.save('proj_recognizer/proj_trainerData.yml')
        res = "Training Images Done!"
        self.message.configure(text=res)
        cv2.destroyAllWindows()

    def getImageWithID(self, path):
        self.imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
        self.faces = []
        self.IDs = []
        for imagepath in self.imagepaths:
            self.faceImg = Image.open(imagepath).convert('L')
            self.faceNp = np.array(self.faceImg, 'uint8')
            ID = int(os.path.split(imagepath)[-1].split('.')[1])
            self.faces.append(self.faceNp)
            self.IDs.append(ID)
            #cv2.imshow('Trainer', self.faceNp)
            #cv2.waitKey(10)

        return np.array(self.IDs), self.faces

root = Tk()
fr = Face_Recog(root)
root.geometry("720x680")
root.configure(background = 'gray')
root.mainloop()