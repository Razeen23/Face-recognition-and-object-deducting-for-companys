import cv2 as cv

cap = cv.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# img_background = cv.imread('Resources/background.png')
img_background = cv.imread('Resources/MacBook Air - 1.jpg')

while True:
    success, webcam = cap.read()

    img_background[273:273 + 480, 103:103 + 640] = webcam

    cv.imshow('face attendance', img_background)
    # cv.imshow('web cam', webcam)
    cv.waitKey(1)
