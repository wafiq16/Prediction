# Author : Muhammad Wafiq Kamaluddin --()-- Consiglere 2021
# python -m pip install

import paho.mqtt.client as mqtt

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5 import *

import sys
import cv2
import os
import numpy as np
import os.path
import csv
import time
import json

myData = open('data/data_alga.csv', 'w')
# writer = csv.writer(f)
csv_writer = csv.writer(myData)


class VideoThread(QThread):

    change_pixmap_signal_camera = pyqtSignal(np.ndarray)
    change_pixmap_signal_microscope = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        # cap_camera = cv2.VideoCapture('1.mkv')
        cap_microscope = cv2.VideoCapture(2)
        cap_camera = cv2.VideoCapture(0)
        # cap_microscope = cv2.VideoCapture(1)
        # cap_microscope = cap_camera
        while self._run_flag:
            # print(self.flagCapture)
            ret_camera, cv_img_camera = cap_camera.read()
            ret_microscope, cv_img_microscope = cap_microscope.read()
            if ret_camera:
                self.change_pixmap_signal_camera.emit(cv_img_camera)
            else:
                cap_camera = cv2.VideoCapture('1.mkv')
            if ret_microscope:
                self.change_pixmap_signal_microscope.emit(cv_img_microscope)
            else:
                cap_microscope = cv2.VideoCapture('2.mkv')
        cap_camera.release()
        cap_microscope.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class MQTT(QThread):
    change_RGB_Sensor_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def on_connect(self, mqttc, obj, flags, rc):
        if rc != 0:
            print("connection failed")
        print("rc: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        # str(msg.payload).encode('utf-8').strip()
        y = json.loads(msg.payload)
        self.change_RGB_Sensor_signal.emit(y)

    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(mqttc, obj, level, string):
        print(string)


class Hardware(QWidget):
    def __init__(self):
        super().__init__()
        self.sliderStateLed = 0
        self.sliderBackBotState = 0
        self.sliderBackSideState = 0
        self.sliderBackBotValue = 0
        self.sliderBackSideValue = 0

        self.myMQTT = MQTT()

        self.myMQTT.start()

        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.myMQTT.on_message
        self.mqttc.on_connect = self.myMQTT.on_connect
        self.mqttc.on_publish = self.myMQTT.on_publish
        self.mqttc.on_subscribe = self.myMQTT.on_subscribe
        # Uncomment to enable debug messages
        self.mqttc.on_log = self.myMQTT.on_log
        self.mqttc.connect("broker.hivemq.com", 1883, 60)

        self.mqttc.loop_start()

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"Widget")
        self.setObjectName("Widget")
        self.resize(606, 478)
        self.ledSourceSlider = QtWidgets.QSlider(self)
        self.ledSourceSlider.setGeometry(QtCore.QRect(200, 150, 160, 20))
        self.ledSourceSlider.setMaximum(1)
        self.ledSourceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ledSourceSlider.setObjectName("ledSourceSlider")
        self.ledSourceSlider.valueChanged.connect(self.updateSliderValue)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 151, 30))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 150, 141, 30))
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setReadOnly(True)

        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 210, 141, 30))
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setReadOnly(True)

        self.lineEdit_4 = QtWidgets.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(20, 270, 141, 30))
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setReadOnly(True)

        self.lineEdit_5 = QtWidgets.QLineEdit(self)
        self.lineEdit_5.setGeometry(QtCore.QRect(20, 330, 141, 30))
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_5.setReadOnly(True)

        self.lineEdit_6 = QtWidgets.QLineEdit(self)
        self.lineEdit_6.setGeometry(QtCore.QRect(20, 390, 141, 30))
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_6.setReadOnly(True)

        self.backBotSlider = QtWidgets.QSlider(self)
        self.backBotSlider.setGeometry(QtCore.QRect(200, 210, 160, 20))
        self.backBotSlider.setMaximum(2)
        self.backBotSlider.setOrientation(QtCore.Qt.Horizontal)
        self.backBotSlider.setObjectName("backBotSlider")
        self.backBotSlider.valueChanged.connect(self.updateSliderValue)

        self.colBotSlider = QtWidgets.QSlider(self)
        self.colBotSlider.setGeometry(QtCore.QRect(200, 270, 160, 20))
        self.colBotSlider.setMaximum(255)
        self.colBotSlider.setOrientation(QtCore.Qt.Horizontal)
        self.colBotSlider.setObjectName("colBotSlider")
        self.colBotSlider.valueChanged.connect(self.updateSliderValue)

        self.backSideSlider = QtWidgets.QSlider(self)
        self.backSideSlider.setGeometry(QtCore.QRect(200, 330, 160, 20))
        self.backSideSlider.setMaximum(2)
        self.backSideSlider.setOrientation(QtCore.Qt.Horizontal)
        self.backSideSlider.setObjectName("backSideSlider")
        self.backSideSlider.valueChanged.connect(self.updateSliderValue)

        self.colSideSlider = QtWidgets.QSlider(self)
        self.colSideSlider.setGeometry(QtCore.QRect(200, 390, 160, 20))
        self.colSideSlider.setMaximum(255)
        self.colSideSlider.setOrientation(QtCore.Qt.Horizontal)
        self.colSideSlider.setObjectName("colSideSlider")
        self.colSideSlider.valueChanged.connect(self.updateSliderValue)

        self.ledState = QtWidgets.QLineEdit(self)
        self.ledState.setGeometry(QtCore.QRect(400, 150, 141, 30))
        self.ledState.setText("")
        self.ledState.setAlignment(QtCore.Qt.AlignCenter)
        self.ledState.setObjectName("ledState")

        self.backBotState = QtWidgets.QLineEdit(self)
        self.backBotState.setGeometry(QtCore.QRect(400, 210, 141, 30))
        self.backBotState.setText("")
        self.backBotState.setAlignment(QtCore.Qt.AlignCenter)
        self.backBotState.setObjectName("backBotState")

        self.backBotValue = QtWidgets.QLineEdit(self)
        self.backBotValue.setGeometry(QtCore.QRect(400, 270, 141, 30))
        self.backBotValue.setText("")
        self.backBotValue.setAlignment(QtCore.Qt.AlignCenter)
        self.backBotValue.setObjectName("backBotValue")

        self.backSideState = QtWidgets.QLineEdit(self)
        self.backSideState.setGeometry(QtCore.QRect(400, 330, 141, 30))
        self.backSideState.setText("")
        self.backSideState.setAlignment(QtCore.Qt.AlignCenter)
        self.backSideState.setObjectName("backSideState")

        self.backSideValue = QtWidgets.QLineEdit(self)
        self.backSideValue.setGeometry(QtCore.QRect(400, 390, 141, 30))
        self.backSideValue.setText("")
        self.backSideValue.setAlignment(QtCore.Qt.AlignCenter)
        self.backSideValue.setObjectName("backSideValue")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.lineEdit.setText(_translate("Widget", "Hardware Control"))
        self.lineEdit_2.setText(_translate("Widget", "Led Source"))
        self.lineEdit_3.setText(_translate("Widget", "Backlight Bottom"))
        self.lineEdit_4.setText(_translate("Widget", "Color Bottom"))
        self.lineEdit_5.setText(_translate("Widget", "Backlight Side"))
        self.lineEdit_6.setText(_translate("Widget", "Color Side"))
        self.ledState.setPlaceholderText(_translate("Widget", "Led Source"))
        self.backBotState.setPlaceholderText(
            _translate("Widget", "BackBot State"))
        self.backBotValue.setPlaceholderText(
            _translate("Widget", "BackBot Value"))
        self.backSideState.setPlaceholderText(
            _translate("Widget", "BackSide State"))
        self.backSideValue.setPlaceholderText(
            _translate("Widget", "SideBot Value"))

    def updateSliderValue(self):
        self.sliderStateLed = self.ledSourceSlider.value()
        self.sliderBackBotState = self.backBotSlider.value()
        self.sliderBackSideState = self.backSideSlider.value()
        self.sliderBackBotValue = self.colBotSlider.value()
        self.sliderBackSideValue = self.colSideSlider.value()

        self.ledState.setText(str(self.sliderStateLed))
        self.backBotState.setText(str(self.sliderBackBotState))
        self.backBotValue.setText(str(self.sliderBackBotValue))
        self.backSideState.setText(str(self.sliderBackSideState))
        self.backSideValue.setText(str(self.sliderBackSideValue))

        # message = "wes to mosok rakenek"
        data_set = {"L": self.sliderStateLed, "M": self.sliderBackBotState,
                    "N": self.sliderBackBotValue, "O": self.sliderBackSideState, "P": self.sliderBackSideValue}

        message = json.dumps(data_set)
        self.mqttc.publish("/colour/setter", message)
        # print(self.sliderStateLed)
        # print(self.sliderBackBotState)
        # print(self.sliderBackSideState)
        # print(self.sliderBackBotValue)
        # print(self.sliderBackSideValue)


class App(QWidget):
    def __init__(self):
        super().__init__()

        # variable
        self.imageMicNow = 0
        self.imageCamNow = 0
        self.flagCaptureCam = False
        self.flagCaptureMic = False
        self.flagSaveCam = False
        self.flagSaveMic = False
        self.iCam = 0
        self.iMic = 0

        self.max_cam_R = 0
        self.max_cam_G = 0
        self.max_cam_B = 0

        self.max_cam_R = 0
        self.max_cam_G = 0
        self.max_cam_B = 0

        self.mean_mic_R = 0
        self.mean_mic_G = 0
        self.mean_mic_B = 0

        self.max_mic_R = 0
        self.max_mic_G = 0
        self.max_mic_B = 0

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        self.cap_cam_begin = QtCore.QPoint()
        self.cap_cam_end = QtCore.QPoint()
        self.cap_mic_begin = QtCore.QPoint()
        self.cap_mic_end = QtCore.QPoint()

        self.path_file = 'data/data.csv'

        self.screen_resolution = app.desktop().screenGeometry()
        self.MAX_WIDTH, self.MAX_HEIGH = self.screen_resolution.width(
        ), self.screen_resolution.height()

        self.resize(self.MAX_WIDTH, self.MAX_HEIGH)
        self.setWindowTitle('Aplikasi Monitoring Air Tambak')

        self.paintEvent(self)

        self.myMQTT = MQTT()

        self.myMQTT.start()

        mqttc = mqtt.Client()
        mqttc.on_message = self.myMQTT.on_message
        mqttc.on_connect = self.myMQTT.on_connect
        mqttc.on_publish = self.myMQTT.on_publish
        mqttc.on_subscribe = self.myMQTT.on_subscribe
        # Uncomment to enable debug messages
        mqttc.on_log = self.myMQTT.on_log
        mqttc.connect("broker.hivemq.com", 1883, 60)
        mqttc.subscribe("/colour/monitor", 0)

        mqttc.loop_start()
        # mqttc.loop_forever()

        self.myMQTT.change_RGB_Sensor_signal.connect(self.update_RGB_Sensor)

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"Widget")
        self.resize(1366, 768)
        self.widget = QWidget(self)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1366, 768))
        self.View = QPushButton(self.widget)
        self.View.setObjectName(u"View")
        self.View.setEnabled(True)
        self.View.setGeometry(QRect(20, 20, 90, 30))
        self.View.setCheckable(False)
        self.View.setChecked(False)
        self.View.setAutoDefault(False)
        self.View.setFlat(False)

        self.thread_camera = VideoThread()

        # start the thread
        self.thread_camera.start()

        self.View_Cam_1_Tittle = QPushButton(self.widget)
        self.View_Cam_1_Tittle.setObjectName(u"View_Cam_1_Tittle")
        self.View_Cam_1_Tittle.setEnabled(True)
        self.View_Cam_1_Tittle.setGeometry(QRect(40, 60, 90, 30))

        self.View_Cam_1 = QLabel(self.widget)
        self.View_Cam_1.setObjectName(u"View_Cam_1")
        self.View_Cam_1.setGeometry(QRect(40, 100, 480, 320))
        self.thread_camera.change_pixmap_signal_camera.connect(
            self.update_image_camera)

        self.View_Cam_2_Tittle = QPushButton(self.widget)
        self.View_Cam_2_Tittle.setObjectName(u"View_Cam_2_Tittle")
        self.View_Cam_2_Tittle.setGeometry(QRect(610, 60, 90, 30))
        self.View_Cam_2 = QLabel(self.widget)
        self.View_Cam_2.setObjectName(u"View_Cam_2")
        self.View_Cam_2.setGeometry(QRect(610, 100, 480, 320))
        self.thread_camera.change_pixmap_signal_microscope.connect(
            self.update_image_microscope)

        self.Controller = QPushButton(self.widget)
        self.Controller.setObjectName(u"Controller")
        self.Controller.setGeometry(QRect(1130, 20, 140, 30))

        self.Save_Cam_1 = QPushButton(self.widget)
        self.Save_Cam_1.setObjectName(u"Save_Cam_1")
        self.Save_Cam_1.setGeometry(QRect(1130, 110, 220, 30))
        self.Save_Cam_1.clicked.connect(self.captureCamEvent)

        self.Save_Cam_2 = QPushButton(self.widget)
        self.Save_Cam_2.setObjectName(u"Save_Cam_2")
        self.Save_Cam_2.setGeometry(QRect(1130, 150, 220, 31))
        self.Save_Cam_2.clicked.connect(self.captureMicEvent)

        self.Save_To_Csv = QPushButton(self.widget)
        self.Save_To_Csv.setObjectName(u"Save_To_Csv")
        self.Save_To_Csv.setGeometry(QRect(1180, 490, 120, 31))
        self.Save_To_Csv.clicked.connect(self.getParamCam)

        self.RGB_Red = QLineEdit(self.widget)
        self.RGB_Red.setObjectName(u"RGB_Red")
        self.RGB_Red.setGeometry(QRect(1130, 230, 220, 30))
        self.RGB_Sensor = QPushButton(self.widget)
        self.RGB_Sensor.setObjectName(u"RGB_Sensor")
        self.RGB_Sensor.setGeometry(QRect(1130, 190, 220, 30))
        self.RGB_Green = QLineEdit(self.widget)
        self.RGB_Green.setObjectName(u"RGB_Green")
        self.RGB_Green.setGeometry(QRect(1130, 270, 220, 30))
        self.RGB_Blue = QLineEdit(self.widget)
        self.RGB_Blue.setObjectName(u"RGB_Blue")
        self.RGB_Blue.setGeometry(QRect(1130, 310, 220, 30))
        self.Class = QPushButton(self.widget)
        self.Class.setObjectName(u"Class")
        self.Class.setGeometry(QRect(1130, 350, 220, 30))
        self.Class_Type = QLineEdit(self.widget)
        self.Class_Type.setObjectName(u"Class_Type")
        self.Class_Type.setGeometry(QRect(1130, 390, 220, 30))
        self.Class_Concentration = QLineEdit(self.widget)
        self.Class_Concentration.setObjectName(u"Class_Concentration")
        self.Class_Concentration.setGeometry(QRect(1130, 430, 220, 30))
        self.Data = QPushButton(self.widget)
        self.Data.setObjectName(u"Data")
        self.Data.setGeometry(QRect(20, 450, 89, 31))
        self.Mean_Cam_1 = QPushButton(self.widget)
        self.Mean_Cam_1.setObjectName(u"Mean_Cam_1")
        self.Mean_Cam_1.setGeometry(QRect(60, 530, 90, 30))
        self.Mean_R_Cam_1 = QLineEdit(self.widget)
        self.Mean_R_Cam_1.setObjectName(u"Mean_R_Cam_1")
        self.Mean_R_Cam_1.setGeometry(QRect(160, 570, 113, 29))
        self.Mean_R_Cam_1.setReadOnly(True)
        self.pushButton_13 = QPushButton(self.widget)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setGeometry(QRect(60, 570, 90, 30))
        self.pushButton_14 = QPushButton(self.widget)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setGeometry(QRect(60, 610, 90, 30))
        self.Mean_G_Cam_1 = QLineEdit(self.widget)
        self.Mean_G_Cam_1.setObjectName(u"Mean_G_Cam_1")
        self.Mean_G_Cam_1.setGeometry(QRect(160, 610, 113, 29))
        self.Mean_G_Cam_1.setReadOnly(True)
        self.pushButton_15 = QPushButton(self.widget)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setGeometry(QRect(60, 650, 90, 30))
        self.Mean_B_Cam_1 = QLineEdit(self.widget)
        self.Mean_B_Cam_1.setObjectName(u"Mean_B_Cam_1")
        self.Mean_B_Cam_1.setGeometry(QRect(160, 650, 113, 29))
        self.Mean_B_Cam_1.setReadOnly(True)
        self.Max_Cam_1 = QPushButton(self.widget)
        self.Max_Cam_1.setObjectName(u"Max_Cam_1")
        self.Max_Cam_1.setGeometry(QRect(300, 530, 90, 30))
        self.Max_B_Cam_1 = QLineEdit(self.widget)
        self.Max_B_Cam_1.setObjectName(u"Max_B_Cam_1")
        self.Max_B_Cam_1.setGeometry(QRect(400, 650, 113, 29))
        self.Max_B_Cam_1.setReadOnly(True)
        self.pushButton_30 = QPushButton(self.widget)
        self.pushButton_30.setObjectName(u"pushButton_30")
        self.pushButton_30.setGeometry(QRect(300, 570, 90, 30))
        self.Max_R_Cam_1 = QLineEdit(self.widget)
        self.Max_R_Cam_1.setObjectName(u"Max_R_Cam_1")
        self.Max_R_Cam_1.setGeometry(QRect(400, 570, 113, 29))
        self.Max_R_Cam_1.setReadOnly(True)
        self.pushButton_31 = QPushButton(self.widget)
        self.pushButton_31.setObjectName(u"pushButton_31")
        self.pushButton_31.setGeometry(QRect(300, 610, 90, 30))
        self.Max_G_Cam_1 = QLineEdit(self.widget)
        self.Max_G_Cam_1.setObjectName(u"Max_G_Cam_1")
        self.Max_G_Cam_1.setGeometry(QRect(400, 610, 113, 29))
        self.Max_G_Cam_1.setReadOnly(True)
        self.pushButton_32 = QPushButton(self.widget)
        self.pushButton_32.setObjectName(u"pushButton_32")
        self.pushButton_32.setGeometry(QRect(300, 650, 90, 30))
        self.Camera_1_RGB = QPushButton(self.widget)
        self.Camera_1_RGB.setObjectName(u"Camera_1_RGB")
        self.Camera_1_RGB.setGeometry(QRect(40, 490, 90, 30))

        self.Camera_1_Data = QPushButton(self.widget)
        self.Camera_1_Data.setObjectName(u"Camera_1_Data")
        self.Camera_1_Data.setGeometry(QRect(220, 700, 120, 30))
        self.Camera_1_Data.clicked.connect(self.getParamCam1)

        self.Mean_B_Cam_2 = QLineEdit(self.widget)
        self.Mean_B_Cam_2.setObjectName(u"Mean_B_Cam_2")
        self.Mean_B_Cam_2.setGeometry(QRect(650, 650, 113, 29))
        self.Mean_B_Cam_2.setReadOnly(True)
        self.pushButton_53 = QPushButton(self.widget)
        self.pushButton_53.setObjectName(u"pushButton_53")
        self.pushButton_53.setGeometry(QRect(550, 570, 90, 30))
        self.pushButton_54 = QPushButton(self.widget)
        self.pushButton_54.setObjectName(u"pushButton_54")
        self.pushButton_54.setGeometry(QRect(790, 610, 90, 30))
        self.Max_R_Cam_2 = QLineEdit(self.widget)
        self.Max_R_Cam_2.setObjectName(u"Max_R_Cam_2")
        self.Max_R_Cam_2.setGeometry(QRect(890, 570, 113, 29))
        self.Max_R_Cam_2.setReadOnly(True)
        self.Mean_G_Cam_2 = QLineEdit(self.widget)
        self.Mean_G_Cam_2.setObjectName(u"Mean_G_Cam_2")
        self.Mean_G_Cam_2.setGeometry(QRect(650, 610, 113, 29))
        self.Mean_G_Cam_2.setReadOnly(True)
        self.pushButton_55 = QPushButton(self.widget)
        self.pushButton_55.setObjectName(u"pushButton_55")
        self.pushButton_55.setGeometry(QRect(550, 650, 90, 30))
        self.Max_B_Cam_2 = QLineEdit(self.widget)
        self.Max_B_Cam_2.setObjectName(u"Max_B_Cam_2")
        self.Max_B_Cam_2.setGeometry(QRect(890, 650, 113, 29))
        self.Max_B_Cam_2.setReadOnly(True)
        self.Max_G_Cam_2 = QLineEdit(self.widget)
        self.Max_G_Cam_2.setObjectName(u"Max_G_Cam_2")
        self.Max_G_Cam_2.setGeometry(QRect(890, 610, 113, 29))
        self.Max_G_Cam_2.setReadOnly(True)
        self.pushButton_56 = QPushButton(self.widget)
        self.pushButton_56.setObjectName(u"pushButton_56")
        self.pushButton_56.setGeometry(QRect(790, 530, 90, 30))
        self.pushButton_57 = QPushButton(self.widget)
        self.pushButton_57.setObjectName(u"pushButton_57")
        self.pushButton_57.setGeometry(QRect(790, 650, 90, 30))
        self.Mean_Cam_2 = QPushButton(self.widget)
        self.Mean_Cam_2.setObjectName(u"Mean_Cam_2")
        self.Mean_Cam_2.setGeometry(QRect(550, 530, 90, 30))
        self.pushButton_59 = QPushButton(self.widget)
        self.pushButton_59.setObjectName(u"pushButton_59")
        self.pushButton_59.setGeometry(QRect(790, 570, 90, 30))
        self.Mean_R_Cam_2 = QLineEdit(self.widget)
        self.Mean_R_Cam_2.setObjectName(u"Mean_R_Cam_2")
        self.Mean_R_Cam_2.setGeometry(QRect(650, 570, 113, 29))
        self.Mean_R_Cam_2.setReadOnly(True)
        self.pushButton_60 = QPushButton(self.widget)
        self.pushButton_60.setObjectName(u"pushButton_60")
        self.pushButton_60.setGeometry(QRect(550, 610, 90, 30))
        self.Camera_2_RGB = QPushButton(self.widget)
        self.Camera_2_RGB.setObjectName(u"Camera_2_RGB")
        self.Camera_2_RGB.setGeometry(QRect(530, 490, 90, 30))

        self.Camera_2_Data = QPushButton(self.widget)
        self.Camera_2_Data.setObjectName(u"Camera_2_Data")
        self.Camera_2_Data.setGeometry(QRect(720, 700, 120, 30))
        self.Camera_2_Data.clicked.connect(self.getParamCam2)

        self.Next_Data = QPushButton(self.widget)
        self.Next_Data.setObjectName(u"Next_Data")
        self.Next_Data.setGeometry(QRect(1260, 690, 89, 31))
        self.Next_Data.clicked.connect(self.nextDataEvent)
        self.Train = QPushButton(self.widget)
        self.Train.setObjectName(u"Train")
        self.Train.setGeometry(QRect(1080, 590, 89, 50))
        self.Test = QPushButton(self.widget)
        self.Test.setObjectName(u"Test")
        self.Test.setGeometry(QRect(1180, 590, 89, 50))

        self.retranslateUi()

        self.View.setDefault(False)

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(
            QCoreApplication.translate("Widget", u"Widget", None))
        self.View.setText(QCoreApplication.translate("Widget", u"View", None))
        self.View_Cam_1_Tittle.setText(
            QCoreApplication.translate("Widget", u"Camera 1", None))
        self.View_Cam_1.setText(
            QCoreApplication.translate("Widget", u"TextLabel", None))
        self.View_Cam_2_Tittle.setText(
            QCoreApplication.translate("Widget", u"Camera 2", None))
        self.View_Cam_2.setText(
            QCoreApplication.translate("Widget", u"TextLabel", None))
        self.Controller.setText(QCoreApplication.translate(
            "Widget", u"Controller", None))
        self.Save_Cam_1.setText(QCoreApplication.translate(
            "Widget", u"Save Camera 1", None))
        self.Save_Cam_2.setText(QCoreApplication.translate(
            "Widget", u"Save Camera 2", None))
        self.Save_To_Csv.setText(QCoreApplication.translate(
            "Widget", u"Save to CSV", None))
        self.RGB_Red.setPlaceholderText(
            QCoreApplication.translate("Widget", u"Red", None))
        self.RGB_Sensor.setText(QCoreApplication.translate(
            "Widget", u"RGB Sensor", None))
        self.RGB_Green.setPlaceholderText(
            QCoreApplication.translate("Widget", u"Green", None))
        self.RGB_Blue.setPlaceholderText(
            QCoreApplication.translate("Widget", u"Blue", None))
        self.Class.setText(QCoreApplication.translate(
            "Widget", u"Class", None))
        self.Class_Type.setPlaceholderText(
            QCoreApplication.translate("Widget", u"Type", None))
        self.Class_Concentration.setText("")
        self.Class_Concentration.setPlaceholderText(
            QCoreApplication.translate("Widget", u"Concentration", None))
        self.Data.setText(QCoreApplication.translate("Widget", u"Data", None))
        self.Mean_Cam_1.setText(
            QCoreApplication.translate("Widget", u"Mean RGB", None))
        self.pushButton_13.setText(
            QCoreApplication.translate("Widget", u"R", None))
        self.pushButton_14.setText(
            QCoreApplication.translate("Widget", u"G", None))
        self.pushButton_15.setText(
            QCoreApplication.translate("Widget", u"B", None))
        self.Max_Cam_1.setText(
            QCoreApplication.translate("Widget", u"Max RGB", None))
        self.pushButton_30.setText(
            QCoreApplication.translate("Widget", u"R", None))
        self.pushButton_31.setText(
            QCoreApplication.translate("Widget", u"G", None))
        self.pushButton_32.setText(
            QCoreApplication.translate("Widget", u"B", None))
        self.Camera_1_RGB.setText(
            QCoreApplication.translate("Widget", u"Camera 1", None))
        self.Camera_1_Data.setText(
            QCoreApplication.translate("Widget", u"Get Cam 1 Data", None))
        self.pushButton_53.setText(
            QCoreApplication.translate("Widget", u"R", None))
        self.pushButton_54.setText(
            QCoreApplication.translate("Widget", u"G", None))
        self.pushButton_55.setText(
            QCoreApplication.translate("Widget", u"B", None))
        self.pushButton_56.setText(
            QCoreApplication.translate("Widget", u"Max RGB", None))
        self.pushButton_57.setText(
            QCoreApplication.translate("Widget", u"B", None))
        self.Mean_Cam_2.setText(
            QCoreApplication.translate("Widget", u"Mean RGB", None))
        self.pushButton_59.setText(
            QCoreApplication.translate("Widget", u"R", None))
        self.pushButton_60.setText(
            QCoreApplication.translate("Widget", u"G", None))
        self.Camera_2_RGB.setText(
            QCoreApplication.translate("Widget", u"Camera 2", None))
        self.Camera_2_Data.setText(
            QCoreApplication.translate("Widget", u"Get Cam 2 Data", None))
        self.Next_Data.setText(QCoreApplication.translate(
            "Widget", u"Next Data", None))
        self.Train.setText(QCoreApplication.translate(
            "Widget", u"Train", None))
        self.Test.setText(QCoreApplication.translate("Widget", u"Test", None))

    def closeEvent(self, event):
        self.thread_camera.stop()
        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)

        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        qp.setBrush(br)
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        # self.thread_camera.stop()
        self.begin = event.pos()
        # self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        # pass

    def mouseReleaseEvent(self, event):
        # self.thread_camera.start()
        # self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def help_window(self, event):
        mbox = QMessageBox()

        mbox.setText("haha")
        # mbox.setDetailedText("You are now a disciple and subject of the all-knowing Guru")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        mbox.exec_()

    def captureMicEvent(self, event):
        self.flagCaptureMic = True
        self.cap_mic_begin = self.begin
        self.cap_mic_end = self.end

        # time.sleep(500)

        # print(self.flagCaptureCam)

    def captureCamEvent(self, event):
        self.flagCaptureCam = True
        self.cap_cam_begin = self.begin
        self.cap_cam_end = self.end

        # time.sleep(500)

        # print(self.flagCaptureMic)

    def nextDataEvent(self, event):
        self.flagCaptureMic = False
        self.flagCaptureCam = False
        self.flagSaveCam = False
        self.flagSaveMic = False
        cv2.destroyAllWindows()

    def getParamCam(self, event):

        sens_R = self.RGB_Red.text()
        sens_G = self.RGB_Green.text()
        sens_B = self.RGB_Blue.text()

        class_ = self.Class_Type.text()
        concentration = self.Class_Concentration.text()
        row = [self.mean_cam_R, self.mean_cam_G, self.mean_cam_B, self.max_cam_R, self.max_cam_G, self.max_cam_B,
               self.mean_mic_R, self.mean_mic_G, self.mean_mic_B, self.mean_mic_R, self.mean_mic_G, self.mean_mic_B, sens_R, sens_G, sens_B, class_, concentration]

        print(row)
        myData = open('data/data_alga.csv', 'w')
        # writer = csv.writer(f)
        csv_writer = csv.writer(myData)
        csv_writer.writerow(row)
        myData.close()

        mbox = QMessageBox()
        mbox.setText('parameter gambar dari microscope telah diambil :)')
        # mbox.setDetailedText("You are now a disciple and subject of the all-knowing Guru")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mbox.exec_()

        # mqttc.loop_start()

    def getParamCam1(self, event):
        frame = cv2.imread('image/Camera/cam'+str(self.iCam-1)+'.jpg')

        height_final_begin = int(
            (self.cap_cam_begin.y() - 100)/320 * frame.shape[0])
        width_final_begin = int(
            (self.cap_cam_begin.x() - 40)/480 * frame.shape[1])

        height_final_end = int(
            (self.cap_cam_end.y() - 100)/320 * frame.shape[0])
        width_final_end = int((self.cap_cam_end.x() - 40)/480 * frame.shape[1])

        if width_final_begin < 0:
            width_final_begin = 0
        if height_final_begin < 0:
            height_final_begin = 0

        if width_final_end > frame.shape[1]:
            width_final_end = frame.shape[1]
        if height_final_end > frame.shape[0]:
            height_final_end = frame.shape[0]

        frame = frame[height_final_begin:height_final_end,
                      width_final_begin: width_final_end]

        cv2.imshow('frame cam', frame)

        self.imageCamNow = frame

        histR = cv2.calcHist([frame], [0], None, [256], [0, 256])
        histG = cv2.calcHist([frame], [1], None, [256], [0, 256])
        histB = cv2.calcHist([frame], [2], None, [256], [0, 256])

        sumAllR = 0
        sumMulR = 0
        sumAllG = 0
        sumMulG = 0
        sumAllB = 0
        sumMulB = 0

        for i in range(0, 256):
            if(histR[i] == np.max(histR)):
                self.max_cam_R = i
                # self.inEMaR.set(i)
            sumAllR += histR[i]
            sumMulR += i*histR[i]
            if(histG[i] == np.max(histG)):
                self.max_cam_G = i
                # self.inEMaG.set(i)
            sumAllG += histG[i]
            sumMulG += i*histG[i]
            if(histB[i] == np.max(histB)):
                self.max_cam_B = i
                # self.inEMaB.set(i)
            sumAllB += histB[i]
            sumMulB += i*histB[i]

        self.mean_cam_R = int(sumMulR/sumAllR)
        self.mean_cam_G = int(sumMulG/sumAllG)
        self.mean_cam_B = int(sumMulR/sumAllB)

        self.Max_R_Cam_1.setText(str(self.max_cam_R))
        self.Max_G_Cam_1.setText(str(self.max_cam_G))
        self.Max_B_Cam_1.setText(str(self.max_cam_B))

        self.Mean_R_Cam_1.setText(str(self.mean_cam_R))
        self.Mean_G_Cam_1.setText(str(self.mean_cam_G))
        self.Mean_B_Cam_1.setText(str(self.mean_cam_B))

    def getParamCam2(self, event):
        frame = cv2.imread('image/Microscope/mic'+str(self.iMic-1)+'.jpg')

        height_final_begin = int(
            (self.cap_mic_begin.y() - 100)/320 * frame.shape[0])
        width_final_begin = int(
            (self.cap_mic_begin.x() - 610)/480 * frame.shape[1])

        height_final_end = int(
            (self.cap_mic_end.y() - 100)/320 * frame.shape[0])
        width_final_end = int(
            (self.cap_mic_end.x() - 610)/480 * frame.shape[1])

        if height_final_begin < 0:
            width_final_begin = 0
        if height_final_begin < 0:
            height_final_begin = 0

        if width_final_end > frame.shape[1]:
            width_final_end = frame.shape[1]
        if height_final_end > frame.shape[0]:
            height_final_end = frame.shape[0]

        frame = frame[height_final_begin:height_final_end,
                      width_final_begin: width_final_end]

        cv2.imshow('frame', frame)

        histR = cv2.calcHist([frame], [0], None, [256], [0, 256])
        histG = cv2.calcHist([frame], [1], None, [256], [0, 256])
        histB = cv2.calcHist([frame], [2], None, [256], [0, 256])

        sumAllR = 0
        sumMulR = 0
        sumAllG = 0
        sumMulG = 0
        sumAllB = 0
        sumMulB = 0

        for i in range(0, 256):
            if(histR[i] == np.max(histR)):
                self.max_mic_R = i
                # self.inEMaR.set(i)
            sumAllR += histR[i]
            sumMulR += i*histR[i]
            if(histG[i] == np.max(histG)):
                self.max_mic_G = i
                # self.inEMaG.set(i)
            sumAllG += histG[i]
            sumMulG += i*histG[i]
            if(histB[i] == np.max(histB)):
                self.max_mic_B = i
                # self.inEMaB.set(i)
            sumAllB += histB[i]
            sumMulB += i*histB[i]

        self.mean_mic_R = int(sumMulR/sumAllR)
        self.mean_mic_G = int(sumMulG/sumAllG)
        self.mean_mic_B = int(sumMulR/sumAllB)

        self.Max_R_Cam_2.setText(str(self.max_mic_R))
        self.Max_G_Cam_2.setText(str(self.max_mic_G))
        self.Max_B_Cam_2.setText(str(self.max_mic_B))

        self.Mean_R_Cam_2.setText(str(self.mean_mic_R))
        self.Mean_G_Cam_2.setText(str(self.mean_mic_G))
        self.Mean_B_Cam_2.setText(str(self.mean_mic_B))
    # def getParamMic(self,event):

    # frame = cv2.imread('image/Microscope/mic'+str(self.iMic-1)+'.jpg')

    # height_final_begin = int((self.begin.y() - 400)/320 * frame.shape[0])
    # width_final_begin = int((self.begin.x() - 50)/480 * frame.shape[1])

    # height_final_end = int((self.end.y() - 350)/320 * frame.shape[0])
    # width_final_end = int((self.end.x() - 50)/480 * frame.shape[1])

    # if width_final_end > frame.shape[1]:
    #     width_final_end = frame.shape[1]
    # if height_final_end > frame.shape[0]:
    #     height_final_end = frame.shape[0]

    # frame = frame[height_final_begin:height_final_end,
    #               width_final_begin: width_final_end]

    # cv2.imshow('frame', frame)

    # histR = cv2.calcHist([frame], [0], None, [256], [0, 256])
    # histG = cv2.calcHist([frame], [1], None, [256], [0, 256])
    # histB = cv2.calcHist([frame], [2], None, [256], [0, 256])

    # sumAllR = 0
    # sumMulR = 0
    # sumAllG = 0
    # sumMulG = 0
    # sumAllB = 0
    # sumMulB = 0

    # for i in range(0, 256):
    #     if(histR[i] == np.max(histR)):
    #         self.max_mic_R = i
    #         # self.inEMaR.set(i)
    #     sumAllR += histR[i]
    #     sumMulR += i*histR[i]
    #     if(histG[i] == np.max(histG)):
    #         self.max_mic_G = i
    #         # self.inEMaG.set(i)
    #     sumAllG += histG[i]
    #     sumMulG += i*histG[i]
    #     if(histB[i] == np.max(histB)):
    #         self.max_mic_B = i
    #         # self.inEMaB.set(i)
    #     sumAllB += histB[i]
    #     sumMulB += i*histB[i]

    # self.mean_mic_R = int(sumMulR/sumAllR)
    # self.mean_mic_G = int(sumMulG/sumAllG)
    # self.mean_mic_B = int(sumMulR/sumAllB)

    # self.textbox_max_R_mic.setText(str(self.max_mic_R))
    # self.textbox_max_G_mic.setText(str(self.max_mic_G))
    # self.textbox_max_B_mic.setText(str(self.max_mic_B))

    # self.textbox_mean_R_mic.setText(str(self.mean_mic_R))
    # self.textbox_mean_G_mic.setText(str(self.mean_mic_G))
    # self.textbox_mean_B_mic.setText(str(self.mean_mic_B))

    # mbox = QMessageBox()
    # mbox.setText('parameter gambar dari microscope telah diambil :)')
    # # mbox.setDetailedText("You are now a disciple and subject of the all-knowing Guru")
    # mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    # mbox.exec_()

    def runTraining(classification):
        if classification:
            pass
        else:
            pass

    @ pyqtSlot(np.ndarray)
    def update_image_camera(self, cv_img_camera):
        "Updates the image_label with a new opencv image"

        if self.flagCaptureCam:
            if not self.flagSaveCam:
                self.imageCamNow = cv_img_camera
                cv2.imwrite('image/Camera/cam'+str(self.iCam) +
                            '.jpg', self.imageCamNow)
                self.flagSaveCam = True
                self.iCam = self.iCam + 1
                # self.paintEvent(self)
                qt_img_camera = self.convert_cv_qt(self.imageCamNow)
                self.View_Cam_1.setPixmap(qt_img_camera)
        else:
            qt_img_camera = self.convert_cv_qt(cv_img_camera)
            self.View_Cam_1.setPixmap(qt_img_camera)

    @ pyqtSlot(np.ndarray)
    def update_image_microscope(self, cv_img_microscope):
        "Updates the image_label with a new opencv image"

        if self.flagCaptureMic:
            if not self.flagSaveMic:
                self.imageMicNow = cv_img_microscope
                cv2.imwrite('image/Microscope/mic' +
                            str(self.iMic)+'.jpg', self.imageMicNow)
                self.flagSaveMic = True
                self.iMic = self.iMic + 1
                qt_img_microscope = self.convert_cv_qt(self.imageMicNow)
                self.View_Cam_2.setPixmap(qt_img_microscope)
        else:
            qt_img_microscope = self.convert_cv_qt(cv_img_microscope)
            self.View_Cam_2.setPixmap(qt_img_microscope)

    @ pyqtSlot(np.ndarray)
    def convert_cv_qt(self, cv_img):
        "Convert from an opencv image to QPixmap"
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            480, 320, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    @ pyqtSlot(object)
    def update_RGB_Sensor(self, data):
        self.RGB_Red.setText(str(data["R"]))
        self.RGB_Green.setText(str(data["G"]))
        self.RGB_Blue.setText(str(data["B"]))

        # self.RGB_Red.setText(str(data["R"]))
        # self.RGB_Green.setText(str(data["G"]))
        # self.RGB_Blue.setText(str(data["B"]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.setupUi()
    a.show()
    b = Hardware()
    b.setupUi()
    b.show()
    sys.exit(app.exec_())
