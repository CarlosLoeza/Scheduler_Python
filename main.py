import pytesseract
import cv2
import numpy as np
import datefinder



def getText(contour,mask1,img):
    # get path to file that can read text in images
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
    # get dimension for the rectangular box around our contour (contour: date or assigngment)
    x, y, w, h = cv2.boundingRect(contour)
    # get the text inside our rectangular box
    result = img[y:y+h,x:x+w]
    # convert image to string
    test = pytesseract.image_to_string(result)
    # remove \n from our string
    test = test.replace("\n", "")
    # test: print text in our image
    print(test)
    # return text in the form of string
    return result


def main():
    # get path to file that can read text in images
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
    # get image
    img = cv2.imread('Schedule.png')
    # create an array of all zeros aka all black image
    mask1 = np.zeros(img.shape, np.uint8)
    # convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # Create rectangular structuring element and use it for dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(thresh, kernel, iterations=4)
    # contours will find dates and assignments in our image
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # cycle through our contours (dates and assignments) to read text in image
    for i in range(0,len(contours)):
        result = getText(contours[i], mask1, img)

    #test: show image of the desired result
    cv2.imshow('Box Image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
main()