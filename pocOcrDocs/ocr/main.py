import pytesseract as ocr
from PIL import Image
import cv2

def printTexto(current_dir, texto, deltaY, deltaX, h, w, passoY, passoX, x1, x2, y1, y2):
    print("\n============\nTexto Lido " + current_dir + "\n============")
    print("h: " + str(h) + " w: " +str(w) + " passoX: " + str(passoX) + " passoY: " + str(passoY))
    print("deltaY: " + str(deltaY) + " deltaX: " + str(deltaX))
    print("x1: " + str(x1) + " y1: " + str(y1))
    print("x2: " + str(x2) + " y2: " + str(y2))
    print("\nTexto: \n\n")
    print(texto)
    print("============\n")


def generate_ocr(current_dir, porcDeltaY, porcDeltaX, passoY, passoX, show):
    img = Image.open(current_dir).convert('L')
    w, h = img.size
    deltaY = int(h*porcDeltaY)
    deltaX = int(w*porcDeltaX)
    passoX = int(w*passoX)
    passoY = int(h*passoY)
    for y in range(0, h-deltaY, passoY):
        y1 = int(y)
        y2 = y1 + deltaY
        for x in range(0, w-deltaX, passoX):
            x1 = int(x)
            x2 = x1 + deltaX
            area = (x1, y1, x2, y2)
            imgCroped = img.crop(area)
            if(show): 
                imgCroped.show()
            texto = ocr.image_to_string(imgCroped, lang='por').strip()
            #if(texto.find(campoBusca) != -1):
            printTexto(current_dir, texto, deltaY, deltaX, h, w, passoY, passoX, x1, x2, y1, y2)

def main():
    generate_ocr("rg3.jpg", 0.1, 0.6, 0.1, 0.3, True)

if __name__ == "__main__":
    main()

