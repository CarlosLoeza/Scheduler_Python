import pytesseract
import cv2
import numpy as np
from datetime import datetime
from docx import Document
import icalendar
import calendar, events


# def createEvent(img, assignment_list, dates_list):
#     # today's date
#     today = datetime.today()
#     # img to table format to dissect easier
#     document = Document(img)
#     # get first item in table row
#     table = document.tables[0]
#     # Creating a list and a dictionary
#     data = []
#     keys = {}
#     col_titles = ('Date', 'Topic', 'Notes')
#     print("1")
#     # Looping through the each line in the Word table:
#     for i, row in enumerate(table.rows):
#         # Getting text from the cells
#         text = (cell.text for cell in row.cells)
#
#         # Getting they column names:
#         if i == 0:
#             keys = tuple(col_titles)
#             continue
#
#         # Creating a dictionary
#         row_data = dict(zip(keys, text))
#         # create start and end time for event
#         row_data[u'dtstart'] = datetime(today.year, dates_list[i])
#         row_data[u'dtend'] = datetime(today.year, dates_list[i])
#         # append event to our list
#         data.append(row_data)
#         print("2")
#     print("3")
#     cal = calendar()
#
#     for row in data:
#         event = events()
#
#         event.add('summary', row['Title'])
#         event.add('dtstart', row['dtstart'])
#         event.add('dtend', row['dtend'])
#         event.add('description', row['Title'])
#         event.add('location', row['Room'])
#         cal.add_component(event)
#
#     f = open('course_schedule.ics', 'wb')
#     f.write(cal.to_ical())
#     f.close()


def imgToTable(contours, img):
    # find longest date and assignment string, allows us to build our table without
    # making a table cell too big or small
    max_assign_size = 10000
    max_date_size = 10000


    # cycle through all of our contours to find longest string in each column
    for i in range(0, len(contours)):
        # get dimension for the rectangular box around our contour (contour: date or assigngment)
        x, y, w, h = cv2.boundingRect(contours[i])

        # if even, assignment string
        if i%2 == 0:
            if x+w < max_assign_size:
                max_assign_tup = (x,y,w,h)
        # else, date string
        else:
            if x+w < max_date_size:
                max_date_tup = (x,y,w,h)
        # save the first and last textbox coordinates so we know where the course schedule starts and ends
        # reads image bottom-up, right-to-left
        if i == 0:
            # bottom right textbox
            last_textbox = (x,y,w,h)
        # top left textbox
        elif i == len(contours)-1:
                first_textbox = (x,y,w,h)

    for i in range(0, len(contours)):
        # create a bounding rectangle around our text in image
        # text can be a date or assignment name
        x,y,w,h = cv2.boundingRect(contours[i])

        # if bottom left textbox, we will draw a left and right vertical line to create a column.
        # Also draw a horizontal line under our textbox to show where text ends
        if i ==0:
            # left vertivcal line ( ex: | column1 | column2 | column3 | ... |)
            start_x_coord = last_textbox[0]
            start_y_coord = last_textbox[1] + last_textbox[3]
            start_pt = (start_x_coord, start_y_coord)
            end_x_coord = x
            end_y_coord = first_textbox[1]
            end_pt = (end_x_coord, end_y_coord)
            # add vertical line to image
            thickness = 3
            img = cv2.line(img, start_pt, end_pt, (0, 0, 0), thickness)
            # right vertical line
            start_x_coord = last_textbox[0] + last_textbox[2]
            start_y_coord = last_textbox[1] + last_textbox[3]
            start_pt = (start_x_coord, start_y_coord)
            end_x_coord = start_x_coord
            end_y_coord = first_textbox[1]
            end_pt = (end_x_coord, end_y_coord)
            # add vertical line to image
            thickness = 3
            img = cv2.line(img, start_pt, end_pt, (0, 0, 0), thickness)
            # bottom horizontal("floor" line)
            start_x_coord = last_textbox[0] + last_textbox[2]
            start_y_coord = last_textbox[1] + last_textbox[3]
            start_pt = (start_x_coord, start_y_coord)
            end_x_coord = first_textbox[0]
            end_y_coord = start_y_coord
            end_pt = (end_x_coord, end_y_coord)
            thickness = 3
            img = cv2.line(img, start_pt, end_pt, (0, 0, 0), thickness)
        elif i == len(contours)-1:
            # vertivcal line
            start_x_coord = first_textbox[0]
            start_y_coord = first_textbox[1]
            start_pt = (start_x_coord, start_y_coord)
            end_x_coord = start_x_coord
            end_y_coord = last_textbox[1] + last_textbox[3]
            end_pt = (end_x_coord, end_y_coord)
            # add vertical line to image
            thickness = 3
            img = cv2.line(img, start_pt, end_pt, (0, 0, 0), thickness)
            # bottom horizontal("floor" line)
            start_x_coord = last_textbox[0] + last_textbox[2]
            start_y_coord = last_textbox[1] + last_textbox[3]
            start_pt = (start_x_coord, start_y_coord)
            end_x_coord = first_textbox[0]
            end_y_coord = start_y_coord
            end_pt = (end_x_coord, end_y_coord)
            thickness = 3
            img = cv2.line(img, start_pt, end_pt, (0, 0, 0), thickness)


        # draw lines in our image to create a table format
        # start point for our line
        start_x_coord = x
        start_y_coord = y
        start_pt = (start_x_coord, start_y_coord)
        # end point for our line
        end_x_coord = last_textbox[0] + last_textbox[2]
        end_y_coord = start_y_coord
        end_pt = (end_x_coord, end_y_coord)

        thickness = 3
        img = cv2.line(img, start_pt, end_pt, (0, 0, 0), thickness)

        # --------------------------------------------------
        # # draw lines in our image to create a table format
        # # start point for our line
        # start_x_coord = first_textbox[0]
        # start_y_coord = first_textbox[3]
        # start_pt = (start_x_coord, start_y_coord)
        # # end point for our line
        # end_x_coord = last_textbox[0] + last_textbox[2]
        # end_y_coord = start_y_coord
        # end_pt = (end_x_coord, end_y_coord)
        #
        # thickness = 3
        # img = cv2.line(img, start_pt, end_pt, (0,0,0), thickness)

    #test: show image of the desired result
    cv2.imshow('Box Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


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
    # array to hold our assignment dates and names
    dates_list = []
    assignments_list = []
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
        # temp solution as we test:
        # if even index, result is assignment name
        if(i % 2 == 0 ):
            assignments_list.append(result)
        # if odd, result is date
        else:
            dates_list.append(result)

    imgToTable(contours,img)
    #createEvent(img, assignments_list, dates_list)

    # #test: show image of the desired result
    # cv2.imshow('Box Image', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

main()