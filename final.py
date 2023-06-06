from ttk import *
from Tkinter import *
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

class App:
    def __init__(self, window, window_title, video_source=0):
        self.total_result = ""

        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)
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

        self.window = window
        self.fr_t = Frame(self.window)
        self.fr_t.pack(side="top",fill='x', padx=3, pady=3)
        self.fr_t_l = Frame(self.fr_t)
        self.fr_t_l.pack(side="left",fill='x', padx=3, pady=3)
        self.fr_t_l_t = Frame(self.fr_t_l)
        self.fr_t_l_t.pack(side="top",fill='x', padx=3, pady=3)
        self.lb_camera = Label(self.fr_t_l_t, bg="black", fg="green", text="Streaming camera:", font=("Tahoma", 10))
        self.lb_camera.pack(side="top", fill="x")
        self.fr_t_l_b = Frame(self.fr_t_l)
        self.fr_t_l_b.pack(fill='x', padx=3, pady=3)
        self.canvas = Canvas(self.fr_t_l_b, bg='white', width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.fr_t_r = Frame(self.fr_t)
        self.fr_t_r.pack(fill='both', padx=3, pady=3)
        self.fr_option = Frame(self.fr_t_r, bg="white")
        self.fr_option.pack(fill='x', padx=3, pady=10)

        self.label_nhapmatkhau = Label(self.fr_option, text="1. Enter password       ")
        self.label_nhapmatkhau.grid(row = 0, column = 0, padx=5, pady=5)
        self.inputtxt = Text(self.fr_option, height = 1, width = 30, bg='white',fg='white')
        self.inputtxt.grid(row = 0, column =1,padx=5,pady=5)
        self.inputtxt.bind("<Return>", self.enter)
        self.label_pass = Label(self.fr_option, text="<-- required password!",bg="orange")
        self.label_pass.grid(row = 0, column = 2, padx=5, pady=5)

        self.label_chonloai = Label(self.fr_option, text="2. Choose Hing color")
        self.label_chonloai.grid(row = 1, column = 0, padx=5, pady=5)
        self.selected_loai = StringVar()
        self.cb = Combobox(self.fr_option, textvariable=self.selected_loai, font=("Tahoma", 15))
        self.cb['values'] = ["Black / Den","White / Trang"]
        self.cb['state'] = 'disabled'
        self.cb.grid(row = 1, column = 1, pady=5)
        self.label_loai2 = Label(self.fr_option, text=self.selected_loai.get())
        self.label_loai2.grid(row = 1, column = 2, padx=5, pady=5)
        
        self.fr_info = Frame(self.fr_t_r, bg="white")
        self.fr_info.pack(fill='x', padx=3)
        self.txt0 = Label(self.fr_info, text=" - Status                     :")
        self.txt0.grid(row = 0, column = 0, padx=5, pady=5)
        self.label_sts = Label(self.fr_info, text=self.status)
        self.label_sts.grid(row = 0, column = 1, padx=5, pady=5)
        self.txt1 = Label(self.fr_info, text=" - Che do check       :")
        self.txt1.grid(row = 1, column = 0, padx=5, pady=5)
        self.label_loai = Label(self.fr_info, text=self.selected_loai.get())
        self.label_loai.grid(row = 1, column = 1, padx=5, pady=5)
        self.txt2 = Label(self.fr_info, text=" - Sensor                   :")
        self.txt2.grid(row = 2, column = 0, padx=5, pady=5)
        self.label_sensor = Label(self.fr_info, text="")
        self.label_sensor.grid(row = 2, column = 1, padx=5, pady=5)

        self.label_status = Label(self.fr_t_r, text="", fg="black", bg="black", font=(
            "Helvetica", 30),height=5)
        self.label_status.pack(fill="both",padx=5, pady=10, anchor=CENTER)

        self.fr_b = Frame(self.window, bg="black")
        self.fr_b.pack(fill='both', padx=3, pady=3)
        #self.fr_b_t = Frame(self.fr_b)
        #self.fr_b_t.pack(fill='x', padx=3, pady=3)
        #self.lb_1 = Label(self.fr_b_t, text=" Left hing ", font=("Helvetica", 15),bg="grey",fg="black")
        #self.lb_1.pack(side="left",fill='y', padx=3, pady=3)
        #self.fr_Anh_trai = Frame(self.fr_b_t, bg="white")
        #self.fr_Anh_trai.pack(fill='x')
        #self.anhvuachup_trai = Label(self.fr_Anh_trai)
        #self.anhvuachup_trai.grid(row=0, column=0)
        #self.anhcrop_trai = Label(self.fr_Anh_trai)
        #self.anhcrop_trai.grid(row=0, column=1)
        #self.khuvuccheck_trai = Label(self.fr_Anh_trai)
        #self.khuvuccheck_trai.grid(row=0, column=2)
        #self.nguong_trai = Label(self.fr_Anh_trai)
        #self.nguong_trai.grid(row=0, column=3)
        self.fr_b_b = Frame(self.fr_b)
        self.fr_b_b.pack(fill='x', padx=3, pady=3)
        self.lb_2 = Label(self.fr_b_b, text="   Process >>>  ", font=("Helvetica", 10),bg="black",fg="green")
        self.lb_2.pack(side="left",fill='y', padx=3, pady=3)
        self.fr_Anh_phai = Frame(self.fr_b_b, bg="white")
        self.fr_Anh_phai.pack(fill="x")
        self.anhvuachup_phai = Label(self.fr_Anh_phai)
        self.anhvuachup_phai.grid(row=0, column=0)
        self.anhcrop_phai = Label(self.fr_Anh_phai)
        self.anhcrop_phai.grid(row=0, column=1)
        self.khuvuccheck_phai = Label(self.fr_Anh_phai)
        self.khuvuccheck_phai.grid(row=0, column=2)
        self.nguong_phai = Label(self.fr_Anh_phai)
        self.nguong_phai.grid(row=0, column=3)
        self.value = Label(self.fr_Anh_phai)
        self.value.grid(row=0, column=4)

        self.button = Button(window,text="MANUAL CHECK", font=("Tahoma", 10), command=self.xuly)
        self.button.pack()
        self.delay = 100
        self.delay_checkstatus = 5000
        self.daluong()
        self.checkcmbo()
        self.uno()

        self.window.title('CAMERA CHECK HING - Sang')
        self.window.geometry("1200x700")
        self.window.mainloop()
        
    
    def uno(self):
        tt_sensor_unit = self.sensor_unit.read()
        self.total_result = ""

        if tt_sensor_unit == 1:
            self.label_sensor.configure(text="0", foreground="white", background="red")
            self.window.update_idletasks()

        if tt_sensor_unit == 0:
            self.label_sensor.configure(text="1", foreground="black", background="green")
            self.window.update_idletasks()
            time.sleep(2)
            if self.status == 1:
                self.running = 1
                while self.running != 0:
                    time.sleep(1)
                    self.xuly()
                    self.running = 0
                    if self.total_result == "OK":
                        self.role.write(1)
                        time.sleep(5)
                    if self.total_result == "NG":
                        self.role.write(0)
                        self.coi.write(1)
                        time.sleep(1)
                        self.coi.write(0)
                        time.sleep(5)
        self.window.after(10, self.uno)

    def enter(self, *args):
        input = str(self.inputtxt.get('1.0', END))
        if "123" in input:
            self.cb['state'] = 'readonly'
            self.label_pass.configure(text="Mat khau dung!",fg="black",bg="green")
            print("Mat khau dung, hay chon ma motor...")
        else:
            print("Mat khau sai")
            self.label_pass.configure(text="Sai mat khau!", foreground="white", background="red")

    def daluong(self):
        thread = Thread(target=self.update)
        thread.start()
    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            #frame = cv2.resize(frame,(0,0), fx=0.4,fy=0.4) 
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        self.window.after(self.delay, self.update)
    def checkcmbo(self):
        if not self.selected_loai.get():
                self.status = 0
                self.label_sts.configure(text=self.status, foreground="white", background="red")
                self.label_loai.configure(text=" CHUA CHON CHE DO CHECK", foreground="white", background="red")
        else:
            if self.selected_loai.get() == "Black / Den":
                self.status = 1
                self.label_pass.configure(text=" Che do check:", foreground="black", background="white")
                self.label_sts.configure(text=self.status,fg="black",bg="green")
                self.label_loai.configure(text=" Check Hing den (Thong bao NG neu phat hien Hing mau trang)", foreground="black", background="white", font=("ubuntu mono", 10))
                self.label_loai2.configure(text="DEN",font=("ubuntu mono", 15))
                self.mode = "black"
                self.cb['state'] = 'disabled'
            if self.selected_loai.get() == "White / Trang":
                self.status = 1
                self.label_pass.configure(text=" Che do check:", foreground="black", background="white")
                self.label_sts.configure(text=self.status,fg="black",bg="green")
                self.label_loai.configure(text="Check Hing trang (Thong bao NG neu phat hien Hing mau den)", foreground="black", background="white", font=("ubuntu mono", 10))
                self.label_loai2.configure(text="TRANG",font=("ubuntu mono", 15))
                self.mode = "white"
                self.cb['state'] = 'disabled'
        self.window.after(self.delay_checkstatus, self.checkcmbo)

    def xuly(self):
        self.giatri = 0
        self.label_status.configure(text="CHECKING...", foreground="black", background="orange", font=("ubuntu mono", 30))
        self.window.update_idletasks()
        self.daluong2()
    def daluong2(self):
        thread = Thread(target=self.snapshot)
        thread.start()
    def snapshot(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.tenAnh = "anhvuachup"
            cv2.imwrite(self.tenAnh + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            self.crop_phai()
    def crop_phai(self):
        img_control = cv2.imread('img/phai.jpg', 0)
        img_query = cv2.imread('anhvuachup.jpg', 0)
        try:
            warped_image = align.get_warped_image(img_control, img_query)
            cv2.imwrite("crop_phai.jpg", warped_image)
        except:
            self.label_status.configure(text="Camera error!", foreground="white", background="red", font=("ubuntu mono", 30))
        self.show_anhvuachup()
        self.show_anhcrop_phai()
        self.catkhuvuccheck_phai()
        
    def show_anhvuachup(self):
        self.anh = cv2.imread("anhvuachup.jpg", 1)
        resized_img = cv2.resize(self.anh, (200, 200), interpolation = cv2.INTER_LINEAR)
        cv2anh = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        img1 = PIL.Image.fromarray(cv2anh)
        imgtk1 = PIL.ImageTk.PhotoImage(image=img1)
        self.anhvuachup_phai.imgtk = imgtk1
        self.anhvuachup_phai.configure(image=imgtk1)
    def show_anhcrop_phai(self):
        self.anhcropphai = cv2.imread("crop_phai.jpg", 1)
        resized_img = cv2.resize(self.anhcropphai, (400, 200), interpolation = cv2.INTER_LINEAR)
        cv2anh = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        img1 = PIL.Image.fromarray(cv2anh)
        imgtk1 = PIL.ImageTk.PhotoImage(image=img1)
        self.anhcrop_phai.imgtk = imgtk1
        self.anhcrop_phai.configure(image=imgtk1)
    def catkhuvuccheck_phai(self):
        im = PIL.Image.open('crop_phai.jpg').convert('L')
        im = im.crop((470, 20, 680, 150))
        im.save('crop_to_check_phai.jpg')
        self.show_frame_khuvuccheckphai()
        self.check()
    def show_frame_khuvuccheckphai(self):
        self.imgcroptocheck_phai = cv2.imread("crop_to_check_phai.jpg", 1)
        resized_img = cv2.resize(self.imgcroptocheck_phai, (200, 200), interpolation = cv2.INTER_LINEAR)
        cv2imgcroptocheck1 = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        imgcroptocheck1 = PIL.Image.fromarray(cv2imgcroptocheck1)
        imgtkcroptocheck1 = PIL.ImageTk.PhotoImage(image=imgcroptocheck1)
        self.khuvuccheck_phai.imgtk = imgtkcroptocheck1
        self.khuvuccheck_phai.configure(image=imgtkcroptocheck1)
    def check(self):
        self.thres_phai()
    def thres_phai(self):
        img = cv2.imread('crop_to_check_phai.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
        area = int(sum(np.sum(thresh,0))/1000)
        self.ketqua=area
        self.value.configure(text=" "+str(area) ,font=("ubuntu mono", 15))
        cv2.imwrite("thresholded_phai.jpg", thresh)
        self.show_frame_nguong_phai()
    def show_frame_nguong_phai(self):
        self.imgnguong_phai = cv2.imread("thresholded_phai.jpg", 1)
        resized_img = cv2.resize(self.imgnguong_phai, (200, 200), interpolation = cv2.INTER_LINEAR)
        cv2imgcroptocheck1 = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        imgcroptocheck1 = PIL.Image.fromarray(cv2imgcroptocheck1)
        imgtkcroptocheck1 = PIL.ImageTk.PhotoImage(image=imgcroptocheck1)
        self.nguong_phai.imgtk = imgtkcroptocheck1
        self.nguong_phai.configure(image=imgtkcroptocheck1)
        self.result()
    def result(self):
        chedo = self.mode
        if chedo == "white":
            if self.ketqua > 4000:
                self.label_status.configure(text="OK", foreground="black", background="green", font=("ubuntu mono", 30))
                self.total_result = "OK";
            if 2000< self.ketqua < 4000:
                self.label_status.configure(text="NG", foreground="white", background="red", font=("ubuntu mono", 30))
                self.total_result = "NG";
            if self.ketqua == 0:
                self.label_status.configure(text="NG", foreground="white", background="red", font=("ubuntu mono", 30))
                self.total_result = "NG";
            if self.ketqua == 4590:
                self.label_status.configure(text="OK", foreground="black", background="green", font=("ubuntu mono", 30))
                self.total_result = "OK";

        if chedo == "black":
            if self.ketqua > 4000:
                self.label_status.configure(text="NG", foreground="white", background="red", font=("ubuntu mono", 30))
                self.total_result = "NG";
            if 2000< self.ketqua < 4000:
                self.label_status.configure(text="OK", foreground="black", background="green", font=("ubuntu mono", 30))
                self.total_result = "OK";
            if self.ketqua == 0:
                self.label_status.configure(text="NG", foreground="white", background="red", font=("ubuntu mono", 30))
                self.total_result = "NG";
            if self.ketqua == 4590:
                self.label_status.configure(text="NG", foreground="white", background="red", font=("ubuntu mono", 30))
                self.total_result = "NG";
        return self.total_result
                   
class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # Get video source width and height
        #self.width = self.vid.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        #self.height = self.vid.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        #self.vid.set(3,800)
        #self.vid.set(4,600)

        self.width = 600
        self.height = 400
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(Tk(), "CAMERA CHECK HING - SANG")
