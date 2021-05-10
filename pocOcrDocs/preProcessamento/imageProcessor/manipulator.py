import cv2
import numpy as np
import imutils
import math
from imutils.perspective import four_point_transform
from skimage.filters import threshold_local

def fourPointTransform(dir, supEsqDoc, infEsqDoc, infDirDoc, supDirDoc, show = False):
    image = cv2.imread(dir)
    #ratio = image.shape[0] / 500.0
    screenCnt = _toNpArray(supEsqDoc,infEsqDoc,infDirDoc,supDirDoc)
    warped = four_point_transform(image, screenCnt.reshape(4, 2) * 1)
    
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset= 9, method="gaussian")
    warped = (warped > T).astype("uint8") * 255
    
    if(show):
        cv2.imshow("Transformada", imutils.resize(warped, height=650))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return warped

def outlines(dir, show = False):
    image = cv2.imread(dir)
    edged = _edgeDetector(dir, False)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:30]

    screenCnt = []
    pontos = []

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        pontos += approx.tolist()
        
    altura, largura = image.shape[:2]
    
    supEsqDoc,infEsqDoc,infDirDoc,supDirDoc = _corners(pontos, altura, largura)
    
    screenCnt = _toNpArray(supEsqDoc,infEsqDoc,infDirDoc,supDirDoc)
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 10)
    if(show):
        cv2.imshow("Contorno", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return supEsqDoc, infEsqDoc, infDirDoc, supDirDoc

def _blur(dir):
    img = cv2.imread(dir, 0)
    # resize image
    img = cv2.resize(img,None,None,fx=1,fy=1, interpolation=cv2.INTER_CUBIC)
    # remove noise / close lines
    kernel = np.ones((30,30))
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    # find contours
    contours, hier = cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # if the contour is square-ish and has a minimum size, draw contours in gray
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        if abs((w/h)-1) < 0.2 and area > 2500:
            cv2.drawContours(img,[cnt],0,(127),-1)
    return img

def _edgeDetector(dir, show = False):
    image = cv2.imread(dir)
    gray = _blur(dir)  
    edged = cv2.Canny(gray, 60, 110)

    if(show):
        cv2.imshow('Imagem', image)
        cv2.imshow('Contorno', gray)
        cv2.imshow('Arestas', edged)
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return edged

def _corners(allPointsVector, height, width):
    topLeftRef = [0,0]
    bottonLeftRef = [0, height]
    topRightRef = [width, 0]
    bottonRightRef = [width, height]
    #Pega o ponto mais proximo do canto superior esquerdo
    supEsqDoc = _evaluateClosestCorner(allPointsVector, topLeftRef)
    #Pega o ponto mais proximo do canto superior direito
    supDirDoc = _evaluateClosestCorner(allPointsVector, topRightRef)
    #Pega o ponto mais proximo do canto inferior esquerdo
    infEsqDoc = _evaluateClosestCorner(allPointsVector, bottonLeftRef)
    #Pega o ponto mais proximo do canto inferior direito
    infDirDoc = _evaluateClosestCorner(allPointsVector, bottonRightRef)
        
    return supEsqDoc, infEsqDoc, infDirDoc, supDirDoc

def _toNpArray(supEsqDoc,infEsqDoc,infDirDoc,supDirDoc):
    return np.array([[supEsqDoc],[infEsqDoc],[infDirDoc],[supDirDoc]])

def _evaluateClosestCorner(mainVector, cornerRefer):
     #Pega o ponto mais proximo do canto inferior direito
    x, y = mainVector[0][0][0], mainVector[0][0][1]
    dist = _dotsModule(x, cornerRefer[0], y, cornerRefer[1])
    docCorner = [x, y]
    for i in range(len(mainVector)):
        x, y = mainVector[i][0][0], mainVector[i][0][1]
        aux = _dotsModule(x, cornerRefer[0], y, cornerRefer[1])
        if(dist > aux):
            dist = aux
            docCorner = [x, y]
    return docCorner

def _dotsModule(x1, x2, y1, y2):
    return math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))