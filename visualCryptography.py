import numpy
import cv2
import random

def monoThresh(image): # apply thresholding
    n, m = image.shape      #get image dimensions
    monoThreshImage = numpy.zeros((n,m),dtype='int8')+255

    for i in range (n):
        for j in range(m):
            if image[i,j]>128:
                new=255
            else:
                new=0
            monoThreshImage[i,j]=new
    return monoThreshImage


def splitImage(monoThreshImage):  # split the image intp share1 and share2
    n,m = monoThreshImage.shape
    s1 = numpy.zeros((2*n,2*m),dtype = 'int8')+255    #make the new images' size double
    s2 = numpy.zeros((2*n,2*m),dtype = 'int8')+255

    white=['*','*']
    white[0]=numpy.array([[1,0],[0,1]])*255
    white[1]=numpy.array([[0,1],[1,0]])*255

    for i in range(n):
        for j in range(m):
            rand = random.randint(0,1)
            if monoThreshImage[i,j]==255:
                s1[2*i:2*i+2,2*j:2*j+2]=white[rand]
                s2[2*i:2*i+2,2*j:2*j+2]=white[rand]
            if monoThreshImage[i,j]==0:
                s1[2*i:2*i+2,2*j:2*j+2]= white[rand]
                s2[2*i:2*i+2,2*j:2*j+2]= white[1-rand]
    return s1,s2


def reconstructImage(share1,share2):  # combine the two shares to create original image .... will be slightly distorted
    if share1.shape != share2.shape:
        print('images have different dimensions')
    else:
        return numpy.minimum(share1,share2)




def main():
    print('Type encode or decode')
    
    process = input('encode or decode: ')


    
    if (process == 'encode'):
        imageName = input('Enter image name: ')
        
        image = cv2.imread(imageName,0) #read image as greyscale
        monoThreshImage = monoThresh(image)
        share1,share2 = splitImage(monoThreshImage)
        cv2.imwrite('share1.png',share1)
        cv2.imwrite('share2.png',share2)
        print('Image has been encoded. share1.png and share2.png have been created.')

        #cv2.imshow('original image',image)
        #cv2.imshow('share1',share1)
        #cv2.imshow('share2',share2)

        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


        
    if (process == 'decode'):
        share1Name = input('Enter first image name: ')
        share1 = cv2.imread(share1Name)
        share2Name = input('Enter second image name: ')
        share2 = cv2.imread(share2Name)
        reconstructed = reconstructImage(share1,share2)
        cv2.imwrite('reconstructed.png',reconstructed)
        print('Image successfully decoded. reconstructed.png has been created.')
        
        cv2.imshow('first image',share1)
        cv2.imshow('second image',share2)
        cv2.imshow('reconstructed image',reconstructed)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
 


if __name__ == "__main__":
    main()











                

