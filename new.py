from ttk import *
from Tkinter import *
import Tkinter as tk
import cv2
import PIL
import PIL.Image, PIL.ImageTk
import time
from time import strftime
import sys
import align
import util
import datetime
import numpy as np
from threading import Thread
import pyfirmata
from pyfirmata import util

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        camera_input_list = ["0", "1", "2", "3"]
        mode_check_list = ["MODEL T081 : WHITE HING", "MODEL T082 : BLACK HING"]

        board = pyfirmata.Arduino('COM3')
        board.pass_time(5)
        self.sensor_unit = board.digital[3]
        self.coi = board.digital[4]
        self.role = board.digital[6]
        it = pyfirmata.util.Iterator(board)
        it.start()
        self.sensor_unit.mode = pyfirmata.INPUT
        self.coi.mode = pyfirmata.OUTPUT
        self.role.mode = pyfirmata.OUTPUT
        self.status=0
        self.running = 0

        self.mode = ""
        self.total_result_trai = ""
        self.total_result_phai = ""
        self.total_result = ""
        self.parent = parent
        self.frtren = Frame(self.parent,borderwidth=5, relief=GROOVE)
        self.frtren.pack(side="top",pady=5,padx=5,fill="x")
        self.frseting = Frame(self.frtren)
        self.frseting.pack(side=LEFT)
        self.label_nhapmatkhau = Label(self.frseting, text="Enter password:",bg="red",fg="white",borderwidth=5, relief=SUNKEN)	
        self.label_nhapmatkhau.grid(row = 0, column = 0, padx=5, pady=5)
        self.inputtxt = Text(self.frseting, height = 1, width = 30, bg='white',fg='black',borderwidth=5, relief=SUNKEN)
        self.inputtxt.grid(row = 0, column =1,padx=5,pady=5)
        self.inputtxt.bind("<Return>", self.enter)
        self.label_chonthitruong = Label(self.frseting, text="Select model",font=("Helvetica",12,"bold"))
        self.label_chonthitruong.grid(row = 1, column = 0, padx=5, pady=5)
        self.modecheck_combobox = Combobox(self.frseting, values=mode_check_list,font=("Tahoma", 15))
        self.modecheck_combobox.grid(row = 1, column = 1, padx=5, pady=5)
        self.modecheck_combobox['state'] = 'disabled'
        self.modecheck = ""
        self.btn_confirm = Button(self.frtren,text="OK",command=self.xacnhanmode,bg="green",width=10,borderwidth=5, relief=RAISED)
        self.btn_confirm.pack(side=LEFT,fill="y",padx=2,pady=5)
        self.btn_confirm['state'] = 'disabled'
        self.btn_confirm['bg'] = 'gray'
        self.test = Button(self.frtren,command=self.check,width=2)
        self.test.pack(side=LEFT,fill="y",padx=2,pady=5)
        self.label_mode = Label(self.frtren, text="Enter password and select model!",font=("Helvetica", 30),bg="red",borderwidth=5, relief=SUNKEN)
        self.label_mode.pack(fill='both', padx=35, pady=10,anchor=CENTER)
        self.trai = Frame(self.parent)
        self.trai.pack(side=LEFT)
        self.trai_tren = Frame(self.trai,bg="white",borderwidth=5, relief=GROOVE)
        self.trai_tren.pack(side="top",padx=5)
        self.frame_trai=Frame(self.trai_tren,borderwidth=3, relief=SOLID)
        self.frame_trai.pack(side="left",padx=5,pady=10)
        self.lbcamtrai=Label(self.frame_trai,text="CAMERA CHECK LEFT HING",bg="black",fg="green")
        self.lbcamtrai.pack(side="top",fill="x")
        self.panel_cam1=Label(self.frame_trai,borderwidth=5, relief=SUNKEN)
        self.panel_cam1.pack()
        self.cam1_input_label = Label(self.frame_trai, text=" - Left Camera Input:")
        self.cam1_input_label.pack(side=LEFT)
        self.cam1_input_combobox = Combobox(self.frame_trai, values=camera_input_list)
        self.cam1_input_combobox.pack(side=LEFT)
        self.cam1_input_combobox.current(0)
        self.cam1_input_combobox['state'] = 'disabled'
        self.address_cam1 = 0
        self.btn_confirm_cam1 = Button(self.frame_trai,text="OK",command=self.change_address_cam1,bg="green",borderwidth=5, relief=RAISED)
        self.btn_confirm_cam1.pack(side=LEFT,padx=2)
        self.btn_confirm_cam1['state'] = 'disabled'
        self.btn_confirm_cam1['bg'] = 'gray'
        self.btn_test_cam1 = Button(self.frame_trai,text="TEST",command=self.test_cam1,bg="orange",borderwidth=5, relief=RAISED)
        self.btn_test_cam1.pack(side=LEFT,pady=2)
        self.cam1_diachi = Label(self.frame_trai, text= "USB-"+str(self.address_cam1), font=("Helvetica",10,"bold") ,fg="green",bg="black",borderwidth=5, relief=SUNKEN)
        self.cam1_diachi.pack(side=LEFT,padx=5,pady=2)
        self.frame_trai_duoi=Frame(self.frame_trai)
        self.frame_trai_duoi.pack(side="bottom")
        self.frame_phai=Frame(self.trai_tren,borderwidth=3, relief=SOLID)
        self.frame_phai.pack(side="left",padx=5,pady=10)
        self.lbcamphai=Label(self.frame_phai,text="CAMERA CHECK RIGHT HING",bg="black",fg="green")
        self.lbcamphai.pack(side="top",fill="x")
        self.panel_cam2=Label(self.frame_phai,borderwidth=5, relief=SUNKEN)
        self.panel_cam2.pack()
        self.cam2_input_label = Label(self.frame_phai, text=" - Right Camera Input:")
        self.cam2_input_label.pack(side=LEFT)
        self.cam2_input_combobox = Combobox(self.frame_phai, values=camera_input_list)
        self.cam2_input_combobox.pack(side=LEFT)
        self.cam2_input_combobox.current(1)
        self.cam2_input_combobox['state'] = 'disabled'
        self.address_cam2 = 1
        self.btn_confirm_cam2 = Button(self.frame_phai,text="OK",command=self.change_address_cam2,bg="green",borderwidth=5, relief=RAISED)
        self.btn_confirm_cam2.pack(side=LEFT,padx=2)
        self.btn_confirm_cam2['state'] = 'disabled'
        self.btn_confirm_cam2['bg'] = 'gray'
        self.btn_test_cam2 = Button(self.frame_phai,text="TEST",command=self.test_cam2,bg="orange",borderwidth=5, relief=RAISED)
        self.btn_test_cam2.pack(side=LEFT,pady=2)
        self.cam2_diachi = Label(self.frame_phai, text= "USB-"+str(self.address_cam2), font=("Helvetica",10,"bold") ,fg="green",bg="black",borderwidth=5, relief=SUNKEN)
        self.cam2_diachi.pack(side=LEFT,padx=5,pady=2)
        self.trai_duoi = Frame(self.trai,borderwidth=5, relief=GROOVE)
        self.trai_duoi.pack(fill="x",padx=5)
        self.frame_xulytrai=Frame(self.trai_duoi)
        self.frame_xulytrai.pack(fill="x")
        self.lb_1 = Label(self.frame_xulytrai, text=" Left ", font=("Helvetica", 10),bg="black",fg="green")
        self.lb_1.pack(side="left",fill='y', padx=3, pady=3)
        self.fr_Anh_trai = Frame(self.frame_xulytrai, bg="white")
        self.fr_Anh_trai.pack(fill="x")
        self.anhvuachup_trai = Label(self.fr_Anh_trai)
        self.anhvuachup_trai.grid(row=0, column=0)
        self.anhcrop_trai = Label(self.fr_Anh_trai)
        self.anhcrop_trai.grid(row=0, column=1)
        self.khuvuccheck_trai = Label(self.fr_Anh_trai)
        self.khuvuccheck_trai.grid(row=0, column=2)
        self.nguong_trai = Label(self.fr_Anh_trai)
        self.nguong_trai.grid(row=0, column=3)
        self.value_trai = Label(self.fr_Anh_trai,text="5000")
        self.value_trai.grid(row=0, column=4)
        self.frame_xulyphai=Frame(self.trai_duoi)
        self.frame_xulyphai.pack(fill="x")
        self.lb_2 = Label(self.frame_xulyphai, text="Right", font=("Helvetica", 10),bg="black",fg="green")
        self.lb_2.pack(side="left",fill='y', padx=3, pady=3)
        self.fr_Anh_phai = Frame(self.frame_xulyphai, bg="white")
        self.fr_Anh_phai.pack(fill="x")
        self.anhvuachup_phai = Label(self.fr_Anh_phai)
        self.anhvuachup_phai.grid(row=0, column=0)
        self.anhcrop_phai = Label(self.fr_Anh_phai)
        self.anhcrop_phai.grid(row=0, column=1)
        self.khuvuccheck_phai = Label(self.fr_Anh_phai)
        self.khuvuccheck_phai.grid(row=0, column=2)
        self.nguong_phai = Label(self.fr_Anh_phai)
        self.nguong_phai.grid(row=0, column=3)
        self.value_phai = Label(self.fr_Anh_phai,text="5000")
        self.value_phai.grid(row=0, column=4)
        self.label_status = Label(parent, text="READY", fg="white", bg="blue",font=("ubuntu mono", 50,"bold"),width=600, height=600,borderwidth=50, relief=RAISED)
        self.label_status.pack(side="right" ,fill='both', padx=5, pady=5,anchor=CENTER)
        self.show_cam_empty()
        self.show_xuly_empty()
        self.uno()

    def uno(self):
        tt_sensor_unit = self.sensor_unit.read()
        self.total_result = ""

        #if tt_sensor_unit == 1:
            #self.label_sensor.configure(text="0", foreground="white", background="red")
            #self.window.update_idletasks()

        if tt_sensor_unit == 0:
            self.label_status.configure(text="CG", foreground="white", background="orange",font=("ubuntu mono", 100,"bold"))
            root.update_idletasks()
            self.coi.write(1)
            time.sleep(0.5)
            self.coi.write(0)
            print("an nut")
            if self.status == 1:
                self.running = 1
                while self.running != 0:
                    self.check()
                    self.running = 0
                    if self.total_result == "OK":
                        self.role.write(1)
                        time.sleep(0.5)
                        self.role.write(0)
                        #time.sleep(5)
                    if self.total_result == "NG":
                        #self.role.write(0)
                        self.coi.write(1)
                        time.sleep(2)
                        self.coi.write(0)
        self.after(5, self.uno)
        
    def check(self):
        self.label_status.configure(text="CG", foreground="white", background="orange",font=("ubuntu mono", 100,"bold"))
        self.snapshot_trai()

    def snapshot_trai(self):
        diachi = int(self.address_cam1)
        print(diachi)
        cap = cv2.VideoCapture(diachi)
        cap.set(3,800)
        cap.set(4,600)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("cam1.jpg", frame)
            self.show_cam1()
            self.crop_trai()
        else:
            self.show_cam1_not_working()
    def crop_trai(self):
        chedo = self.mode
        if chedo == "white":
            img_control = cv2.imread('img/trai_81.jpg', 0)
            img_query = cv2.imread('cam1.jpg', 0)
            try:
                warped_image = align.get_warped_image(img_control, img_query)
                cv2.imwrite("crop_trai.jpg", warped_image)
            except:
                self.label_status.configure(text="LC!", foreground="white", background="red",font=("ubuntu mono", 100,"bold"))
        if chedo == "black":
            img_control = cv2.imread('img/trai.jpg', 0)
            img_query = cv2.imread('cam1.jpg', 0)
            try:
                warped_image = align.get_warped_image(img_control, img_query)
                cv2.imwrite("crop_trai.jpg", warped_image)
            except:
                self.label_status.configure(text="LC!", foreground="white", background="red",font=("ubuntu mono", 100,"bold"))
        self.show_anhvuachup_trai()
        self.show_anhcrop_trai()
        self.catkhuvuccheck_trai()
        
    def show_anhvuachup_trai(self):
        ui1 = cv2.imread("cam1.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.anhvuachup_trai.imgtk = imgtk1
        self.anhvuachup_trai.configure(image=imgtk1)

    def show_anhcrop_trai(self):
        ui1 = cv2.imread("crop_trai.jpg", 1)
        r= cv2.resize(ui1, (300, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.anhcrop_trai.imgtk = imgtk1
        self.anhcrop_trai.configure(image=imgtk1)

    def catkhuvuccheck_trai(self):
        chedo = self.mode
        if chedo == "white":
            im = PIL.Image.open('crop_trai.jpg').convert('L')
            im = im.crop((185, 33, 327, 94))
            im.save('crop_to_check_trai.jpg')
        if chedo == "black":
            im = PIL.Image.open('crop_trai.jpg').convert('L')
            im = im.crop((263, 19, 585, 224))
            im.save('crop_to_check_trai.jpg')
        self.show_frame_khuvucchecktrai()
        self.thres_trai()

    def show_frame_khuvucchecktrai(self):
        ui1 = cv2.imread("crop_to_check_trai.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.khuvuccheck_trai.imgtk = imgtk1
        self.khuvuccheck_trai.configure(image=imgtk1)
        self.label_status.configure(text="CL", foreground="white", background="orange",font=("ubuntu mono", 100,"bold"))

    def thres_trai(self):
        img = cv2.imread('crop_to_check_trai.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        chedo = self.mode
        if chedo == "white":
            _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
            area = int(sum(np.sum(thresh,0))/1000)
        if chedo == "black":
            _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
            area = int(sum(np.sum(thresh,0))/10000)
        print("area trai la: " + str(area))
        self.ketqua_trai=area
        self.value_trai.configure(text=" "+str(area) ,font=("ubuntu mono", 15))
        cv2.imwrite("thresholded_trai.jpg", thresh)
        self.show_frame_nguong_trai()
    
    def show_frame_nguong_trai(self):
        ui1 = cv2.imread("thresholded_trai.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.nguong_trai.imgtk = imgtk1
        self.nguong_trai.configure(image=imgtk1)
        self.result_trai()
        self.snapshot_phai()

    def result_trai(self):
        chedo = self.mode
        if chedo == "white":
            if self.ketqua_trai > 2000:
                self.total_result_trai = "OK"
            if self.ketqua_trai < 2000:
                self.total_result_trai = "NG"
            if self.ketqua_trai == 0:
                self.total_result_trai = "NG"
            if self.ketqua_trai == 2208:
                self.total_result_trai = "OK"
        if chedo == "black":
            if self.ketqua_trai > 1500:
                self.total_result_trai = "NG"
            if self.ketqua_trai < 1500:
                self.total_result_trai = "OK"
            if self.ketqua_trai == 0:
                self.total_result_trai = "OK"
           #if self.ketqua_trai == 2208:
            #    self.total_result_trai = "NG"
        print(chedo)
        print("total result trai la: " + str(self.total_result_trai))
        return self.total_result_trai
        
    def snapshot_phai(self):        
        diachi = int(self.address_cam2)
        print(diachi)
        cap = cv2.VideoCapture(diachi)
        cap.set(3,800)
        cap.set(4,600)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("cam2.jpg", frame)
            self.show_cam2()
            self.crop_phai()
        else:
            self.show_cam2_not_working()

    def crop_phai(self):
        img_control = cv2.imread('img/phai.jpg', 0)
        img_query = cv2.imread('cam2.jpg', 0)
        try:
            warped_image = align.get_warped_image(img_control, img_query)
            cv2.imwrite("crop_phai.jpg", warped_image)
        except:
            self.label_status.configure(text="RC!", foreground="white", background="red",font=("ubuntu mono", 100,"bold"))
        self.show_anhvuachup_phai()
        self.show_anhcrop_phai()
        self.catkhuvuccheck_phai()

    def show_anhvuachup_phai(self):
        ui1 = cv2.imread("cam2.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.anhvuachup_phai.imgtk = imgtk1
        self.anhvuachup_phai.configure(image=imgtk1)
    
    def show_anhcrop_phai(self):
        ui1 = cv2.imread("crop_phai.jpg", 1)
        r= cv2.resize(ui1, (300, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.anhcrop_phai.imgtk = imgtk1
        self.anhcrop_phai.configure(image=imgtk1)
    
    def catkhuvuccheck_phai(self):
        im = PIL.Image.open('crop_phai.jpg').convert('L')
        im = im.crop((281, 12, 413, 83))
        im.save('crop_to_check_phai.jpg')
        self.show_frame_khuvuccheckphai()
        self.thres_phai()
    
    def show_frame_khuvuccheckphai(self):
        self.label_status.configure(text="CR", foreground="white", background="orange",font=("ubuntu mono", 100,"bold"))
        ui1 = cv2.imread("crop_to_check_phai.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.khuvuccheck_phai.imgtk = imgtk1
        self.khuvuccheck_phai.configure(image=imgtk1)

    def thres_phai(self):
        img = cv2.imread('crop_to_check_phai.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        area = int(sum(np.sum(thresh,0))/1000)
        print("area phai la: " + str(area))
        self.ketqua_phai=area
        self.value_phai.configure(text=" "+str(area) ,font=("ubuntu mono", 15))
        cv2.imwrite("thresholded_phai.jpg", thresh)
        self.show_frame_nguong_phai()
    
    def show_frame_nguong_phai(self):
        ui1 = cv2.imread("thresholded_phai.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.nguong_phai.imgtk = imgtk1
        self.nguong_phai.configure(image=imgtk1)
        self.result_phai()
        self.ketqua()

    def result_phai(self):
        chedo = self.mode
        if chedo == "white":
            if self.ketqua_phai > 2000 :
                self.total_result_phai = "OK"
            if self.ketqua_phai < 2000:
                self.total_result_phai = "NG"
            if self.ketqua_phai == 0:
                self.total_result_phai = "NG"
            if self.ketqua_phai == 2389:
                self.total_result_phai = "OK"
        if chedo == "black":
            if self.ketqua_phai > 2000 :
                self.total_result_phai = "NG"
            if self.ketqua_phai < 2000:
                self.total_result_phai = "OK"
            if self.ketqua_phai == 0:
                self.total_result_phai = "OK"
            if self.ketqua_phai == 2389:
                self.total_result_phai = "NG"
        print("total result phai la: " + str(self.total_result_phai))
        return self.total_result_phai
    
    def ketqua(self):
        if self.total_result_phai ==  self.total_result_trai == "NG":
            self.label_status.configure(text="NG", foreground="white", background="red", font=("ubuntu mono", 100,"bold"))
            self.total_result = "NG"
        if self.total_result_phai == self.total_result_trai == "OK":
            self.label_status.configure(text="OK", foreground="black", background="green", font=("ubuntu mono", 100,"bold"))
            self.total_result = "OK"
        if self.total_result_phai != self.total_result_trai:
            self.label_status.configure(text="NG", foreground="white", background="red", font=("ubuntu mono", 100,"bold"))
            self.total_result = "NG"
        return self.total_result

    def enter(self, *args):
        input = str(self.inputtxt.get('1.0', END))
        if "123mfe" in input:
            self.modecheck_combobox['state'] = 'readonly'
            self.cam1_input_combobox['state'] = 'readonly'
            self.btn_confirm_cam1['state'] = 'normal'
            self.btn_confirm_cam1['bg'] = 'green'
            self.cam2_input_combobox['state'] = 'readonly'
            self.btn_confirm_cam2['state'] = 'normal'
            self.btn_confirm_cam2['bg'] = 'green'
            self.btn_confirm['state'] = 'normal'
            self.btn_confirm['bg'] = 'green'
            self.inputtxt.delete('1.0', END)
            print("Mat khau dung")
            self.label_mode.configure(text="Select model!",fg="black",bg="green")

        else:
            print("Mat khau sai")
            self.label_mode.configure(text="Wrong password!",fg="black",bg="red")

            self.inputtxt.delete('1.0', END)

    def xacnhanmode(self):
        selected_value = self.modecheck_combobox.get()
        self.modecheck = selected_value
        self.label_mode.configure(text=self.modecheck,fg="green",bg="black")
        self.modecheck_combobox['state'] = 'disabled'
        self.cam1_input_combobox['state'] = 'disabled'
        self.btn_confirm_cam1['state'] = 'disabled'
        self.btn_confirm_cam1['bg'] = 'gray'
        self.cam2_input_combobox['state'] = 'disabled'
        self.btn_confirm_cam2['state'] = 'disabled'
        self.btn_confirm_cam2['bg'] = 'gray'
        self.btn_confirm['state'] = 'disabled'
        self.btn_confirm['bg'] = 'gray'
        if self.modecheck_combobox.get() == "MODEL T081 : WHITE HING":
            self.status = 1
            self.mode = "white"
        if self.modecheck_combobox.get() == "MODEL T082 : BLACK HING":
            self.status = 1
            self.mode = "black"

    def show_cam_empty(self):
        self.show_cam1_empty()
        self.show_cam2_empty()

    def show_xuly_empty(self):
        self.show_cam1_anhvuachup_empty()
        self.show_cam1_anhcrop_empty()
        self.show_cam1_khuvuccheck_empty()
        self.show_cam1_nguong_empty()
        self.show_cam2_anhvuachup_empty()
        self.show_cam2_anhcrop_empty()
        self.show_cam2_khuvuccheck_empty()
        self.show_cam2_nguong_empty()

    def show_cam1_empty(self):
        ui1 = cv2.imread("ui/c1.jpg", 1)
        r= cv2.resize(ui1, (400, 200), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.panel_cam1.imgtk = imgtk1
        self.panel_cam1.configure(image=imgtk1)

    def show_cam2_empty(self):
        ui1 = cv2.imread("ui/c2.jpg", 1)
        r= cv2.resize(ui1, (400, 200), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.panel_cam2.imgtk = imgtk1
        self.panel_cam2.configure(image=imgtk1)

    def show_cam1_not_working(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (400, 200), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.panel_cam1.imgtk = imgtk1
        self.panel_cam1.configure(image=imgtk1)

    def show_cam2_not_working(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (400, 200), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.panel_cam2.imgtk = imgtk1
        self.panel_cam2.configure(image=imgtk1)

    def show_cam1_anhvuachup_empty(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.anhvuachup_trai.imgtk = imgtk1
        self.anhvuachup_trai.configure(image=imgtk1)

    def show_cam1_anhcrop_empty(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (300, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.anhcrop_trai.imgtk = imgtk1
        self.anhcrop_trai.configure(image=imgtk1)

    def show_cam1_khuvuccheck_empty(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.khuvuccheck_trai.imgtk = imgtk1
        self.khuvuccheck_trai.configure(image=imgtk1)

    def show_cam1_nguong_empty(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.nguong_trai.imgtk = imgtk1
        self.nguong_trai.configure(image=imgtk1)

    def show_cam2_anhvuachup_empty(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.anhvuachup_phai.imgtk = imgtk1
        self.anhvuachup_phai.configure(image=imgtk1)

    def show_cam2_anhcrop_empty(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (300, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.anhcrop_phai.imgtk = imgtk1
        self.anhcrop_phai.configure(image=imgtk1)

    def show_cam2_khuvuccheck_empty(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.khuvuccheck_phai.imgtk = imgtk1
        self.khuvuccheck_phai.configure(image=imgtk1)

    def show_cam2_nguong_empty(self):
        ui1 = cv2.imread("ui/webcam-not-working.jpg", 1)
        r= cv2.resize(ui1, (150, 150), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.nguong_phai.imgtk = imgtk1
        self.nguong_phai.configure(image=imgtk1)
   
    def test_cam1(self):        
        diachi = int(self.address_cam1)
        print(diachi)
        cap = cv2.VideoCapture(diachi)
        cap.set(3,1280)
        cap.set(4,960)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("cam1.jpg", frame)
            self.show_cam1()
        else:
            self.show_cam1_not_working()
        
    def show_cam1(self):
        ui1 = cv2.imread("cam1.jpg", 1)
        r= cv2.resize(ui1, (400, 200), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.panel_cam1.imgtk = imgtk1
        self.panel_cam1.configure(image=imgtk1)

    def test_cam2(self):        
        diachi = int(self.address_cam2)
        print(diachi)
        cap = cv2.VideoCapture(diachi)
        cap.set(3,1280)
        cap.set(4,960)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("cam2.jpg", frame)
            self.show_cam2()
        else:
            self.show_cam2_not_working()
        
    def show_cam2(self):
        ui1 = cv2.imread("cam2.jpg", 1)
        r= cv2.resize(ui1, (400, 200), interpolation = cv2.INTER_LINEAR)
        c = cv2.cvtColor(r, cv2.COLOR_BGR2RGB)
        i1 = PIL.Image.fromarray(c)
        imgtk1 = PIL.ImageTk.PhotoImage(image=i1)
        self.panel_cam2.imgtk = imgtk1
        self.panel_cam2.configure(image=imgtk1)

    def change_address_cam1(self):
        selected_value = self.cam1_input_combobox.get()
        self.address_cam1 = selected_value
        self.cam1_diachi.configure(text="USB-"+ str(self.address_cam1))

    def change_address_cam2(self):
        selected_value = self.cam2_input_combobox.get()
        self.address_cam2 = selected_value
        self.cam2_diachi.configure(text="USB-"+ str(self.address_cam2))

if __name__ == "__main__":
    root = tk.Tk()
    root.title('CAMERA CHECK HING - SANG')
    root.geometry("1300x920")
    MainApplication(root).pack(side="top", fill="both")
    root.mainloop()
