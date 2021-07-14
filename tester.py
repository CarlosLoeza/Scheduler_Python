


#playing around with datefinder to see how it works
import datefinder


dates_list = []

dates_list.append("April 20")
dates_list.append("April 21")
dates_list.append("April 24")

for i in range(0, len(dates_list)):
    # a generator will be returned by the datefinder module. I'm typecasting it to a list. Please read the note of caution provided at the bottom.
    matches = list(datefinder.find_dates(dates_list[i]))

    if len(matches) > 0:
        # date returned will be a datetime.datetime object. here we are only using the first match.
        date = matches[0]
        print(date)
    else:
        print('No dates found')




















# # get path to images folder
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
#
# img = cv2.imread('CourseSched.png')
# image = cv2.imread('CourseSched.png')
#
# # create an array of all zeros aka all black image
# mask1 = np.zeros(img.shape, np.uint8)
#
# # convert image to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (7,7), 0)
# thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#
# # Create rectangular structuring element and dilate
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
# dilate = cv2.dilate(thresh, kernel, iterations=4)
#
# # Find contours and draw rectangle
# cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#
# # cycle through our rectangles so we can read text using tesseract
# for i in range (0, len(cnts)):
#     # reset mask1 to all zeros
#     mask1 = np.zeros(img.shape, np.uint8)
#
#     # even index represent starting point of text box (see images)
#     # odd index represents end point
#     #if i%2 == 0:
#         # get dimension for text box of dates
#     x,y,w,h = cv2.boundingRect(cnts[i])
#     cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)
#
#
# test = pytesseract.image_to_string(img)
# print(test)
# cv2.imshow('Box Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()