import pytesseract
import cv2
import numpy as np
import datefinder



def getText(contour,mask1,img):
    # get path to file that can read text in images
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

    # get dimension for text box of dates
    x, y, w, h = cv2.boundingRect(contour)
    # create a mask to match location of text box
    for i in range(x, (x + w)):
        for j in range(y, y + h):
            mask1[j][i] = 255
    # combine date and assignment text box into one rectangle
    cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)
    # only focus on what is inside rectangle (see image)
    result = cv2.bitwise_and(img, mask1)

    # read text in box and print
    test = pytesseract.image_to_string(result)
    print(test)

    return result


def main():
    # get path to file that can read text in images
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

    img = cv2.imread('Schedule.png')
    image = cv2.imread('Schedule.png')

    # create an array of all zeros aka all black image
    mask1 = np.zeros(img.shape, np.uint8)

    # convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and use it for dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    # # Find contours and draw rectangle around text found in image(dates & assignment names)
    # cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    #
    #
    # # cycle through our rectangles so we can read text using tesseract
    # for i in range (0, len(cnts)):
    # #if(True):
    #     i=0
    #     print(len(cnts))
    #     # create a mask to isolate text
    #     mask1 = np.ones(img.shape, np.uint8)*255
    #
    #     # even index represent starting point of text box
    #     # odd index represents end point
    #     # This allows us to combine date with assignment name
    #     if i%2 == 1:
    #         print('1')
    #         result = getText(cnts[i], mask1, img)
    #         # read text in box and print
    #         # test = pytesseract.image_to_string(result)
    #         # print(test)
    #
    #     elif i%2 == 0:
    #         print('000')
    #         result = getText(cnts[i], mask1, img)
    #         # read text in box and print
    #         # test = pytesseract.image_to_string(result)
    #         # print(test)


    cv2.imshow('Box Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()