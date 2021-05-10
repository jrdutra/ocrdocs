
from imageProcessor.manipulator import fourPointTransform
from imageProcessor.manipulator import outlines
        
def main():
    dir = '.\imagens\\rg2.jpg'
    supEsqDoc, infEsqDoc, infDirDoc, supDirDoc = outlines(dir, True)
    warped = fourPointTransform(dir, supEsqDoc, infEsqDoc, infDirDoc, supDirDoc, True)
    
if __name__ == "__main__":
    main()

