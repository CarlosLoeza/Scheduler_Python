import pytesseract
import cv2
import numpy as np
import calendar




# countRowsAndColumns() is used to determine how many rows and columns we have in our course schedule (see images)
# inputs:
#   contours: list of contours. Each contour represents a date or assignment string
#   img: image of the course schedule
# output:
#   tuple holding the number of rows and columns (rows, columns)
def countRowsAndColumns(contours, img):
    # keep track of the number of rows and columns
    row_count = 0
    col_count = 0
    # get (x,y) points to figure out how many rows and columns we have
    # row holds the x values of our contours
    # col holds the y values of our contours
    row = []
    col = []
    new_row = []
    new_col = []

    for i in range(0, len(contours)):
        # get dimension for the rectangular box around our contour (contour: date or assigngment)
        x, y, w, h = cv2.boundingRect(contours[i])
        row.append(x)
        col.append(y)
   # sort so we can check if they are the same or different based on the difference.
    row.sort()
    col.sort()
    temp =0
    held_val =0
    # check how many items in a row (ex: 2 different x values in row means we have 2 columns
    for i in range (0, len(row)):
        if i == 0:
            # increment col_count since we are counting the number of columns in row
            col_count+=1
            held_val = row[i]
            new_row.append(row[i])
        else:
            temp = row[i]
            # if difference is greater than 5, we have another column
            if abs(held_val-temp) > 10 :
                col_count+=1
                held_val = row[i]
                new_row.append(row[i])

    # check how many items in a column (ex: 12 different y values in col means we have 12 rows
    for i in range (0, len(col)):
        if i == 0:
            row_count+=1
            held_val = col[i]
            new_col.append(col[i])
        else:
            temp = col[i]
            if abs(held_val-temp) > 10:
                row_count+=1
                held_val = col[i]
                new_col.append(col[i])

    # print("Rows: " + str(row_count))
    # print("Columns: " + str(col_count))
    return (new_row,new_col)


# start_end_pt(): gets the start points and end points of textbox and creates a tuple holding these values.
# We use the points to create the table lines in our imgToTable()
# inputs:
#   start_x & start_y: represents the start point of our text box
#   end_x & end_y: represent the end point of our text box
# output:
#   start_end_pts: tuple containing our start and end points/coordinates
def start_end_pt(start_x, start_y, end_x, end_y):
    start_x_coord = start_x
    start_y_coord = start_y
    start_pt = (start_x_coord, start_y_coord)
    # top of page
    end_x_coord = end_x
    end_y_coord = end_y
    end_pt = (end_x_coord, end_y_coord)
    # create tuple
    start_end_pts = ((start_pt),(end_pt))
    return start_end_pts


# imgToTable(): accepts image and converts it to a table formart. We add lines based on the rows and columns we found using countRowsAndColumns()
# inputs:
#   contours: list of contours. Each contour represents a date or assignment string
#   img: image of the course schedule
#   row_col: tuple containing the number of rows and columns (rows, columns)
# output:
#   img: return the new img with lines applied
def imgToTable(contours, img, row_col):
    # find longest date and assignment string, allows us to build our table without
    # making a table cell too big or small
    max_assign_size = -1
    max_date_size = -1
    col_size = len(row_col[1])


    # cycle through all of our contours to find longest string in each column
    for i in range(0, len(contours)):
        # get dimension for the rectangular box around our contour (contour: date or assigngment)
        x, y, w, h = cv2.boundingRect(contours[i])
        # print("x: " + str(x))
        # print("y: " + str(y))
        # print()

        # save the first and last textbox coordinates so we know where the course schedule starts and ends
        # reads image bottom-up, right-to-left
        if i == 0:
            # bottom right textbox
            first_textbox = (x, y, w, h)
        # top left textbox
        elif i == len(contours) - 1:
            last_textbox = (x, y, w, h)

        # if second to last column, assignment string
        if i%col_size == (col_size-2):
            if x+w > max_assign_size:
                max_assign_tup = (x, y, w, h)
                max_assign_size = x+w
        # else, date string
        elif i%col_size == (col_size-1):
            if x+w < max_date_size:
                max_date_tup = (x, y, w, h)
                max_assign_size = x+w

    # print("first x: " + str(first_textbox[0]))
    # print("first y: " + str(first_textbox[1]))
    # print("last x: " + str(last_textbox[0]))
    # print("last y: " + str(last_textbox[1]))

    for i in range(0, len(contours)):
        # create a bounding rectangle around our text in image
        # text can be a date or assignment name
        x,y,w,h = cv2.boundingRect(contours[i])

        # if bottom right textbox aka assignment name, we will draw a left and right vertical line to create a column.
        # Also draw a horizontal line under our textbox to show where text ends ex: |_____|
        if i ==0:
            # left vertivcal line ( ex: | column1 | column2 | column3 | ... |)
            # beginning of textbox
            # get the start and end points of textbox
            # start_end_pt(start_x_coordinate, start_y_coordinate, end_x_coordinate, end_y_coordinate)
            points = start_end_pt(first_textbox[0], (first_textbox[1]+max_assign_tup[3]), first_textbox[0], last_textbox[1])
            # add vertical line to image
            thickness = 3
            img = cv2.line(img, points[0], points[1], (0, 0, 0), thickness)

            # right vertical line
            points = start_end_pt((first_textbox[0]+first_textbox[2]), (first_textbox[1] + max_assign_tup[3]), (first_textbox[0] + first_textbox[2]), last_textbox[1])
            # add vertical line to image
            img = cv2.line(img, points[0], points[1], (0, 0, 0), thickness)

            # bottom horizontal("floor" line)
            points = start_end_pt((last_textbox[0]), (first_textbox[1] + max_assign_tup[3]), (first_textbox[0] + first_textbox[2]), (first_textbox[1] + max_assign_tup[3]))
            # add bottom horizontal line to image
            img = cv2.line(img, points[0], points[1], (0, 0, 0), thickness)

        # top left textbox
        elif i == len(contours)-1:
            # left vertivcal line ( ex: | column1 | column2 | column3 | ... |)
            # beginning of textbox
            points = start_end_pt((last_textbox[0]), (last_textbox[1]), (last_textbox[0]), (first_textbox[1] + first_textbox[3]))
            # add bottom horizontal line to image
            img = cv2.line(img, points[0], points[1], (0, 0, 0), thickness)

            # bottom horizontal("floor" line)
            points = start_end_pt((last_textbox[0]), (last_textbox[1] + max_assign_tup[3]), (first_textbox[0] + first_textbox[2]), (last_textbox[1] + max_assign_tup[3]))
            # add bottom horizontal line to image
            img = cv2.line(img, points[0], points[1], (0, 0, 0), thickness)

            # top horizontal("ceiling" line)
            points = start_end_pt((last_textbox[0]), (last_textbox[1]), (first_textbox[0] + first_textbox[2]), (last_textbox[1]))
            # add bottom horizontal line to image
            img = cv2.line(img, points[0], points[1], (0, 0, 0), thickness)

        else:
            # left vertivcal line ( ex: | column1 | column2 | column3 | ... |)
            # beginning of textbox
            points = start_end_pt((x), (first_textbox[1] + max_assign_tup[3]),(x),(last_textbox[1]))
            # add vertical line to image
            img = cv2.line(img, points[0], points[1], (0, 0, 0), thickness)

            # bottom horizontal("floor" line)
            points = start_end_pt((x), (y + max_assign_tup[3]), (first_textbox[0] + first_textbox[2]), (y + max_assign_tup[3]))
            # add bottom horizontal line to image
            img = cv2.line(img, points[0], points[1], (0, 0, 0), thickness)

    return img


# getText(): gets the text in the contour and turns it into a string using tesseract
# inputs:
#   contours: list of contours. Each contour represents a date or assignment string
#   img: image of the course schedule
# output:
#   result: string of the text found in the contour
def getText(contour,img):
    # get path to file that can read text in images
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
    # get dimension for the rectangular box around our contour (contour: date or assigngment)
    x, y, w, h = cv2.boundingRect(contour)
    # get the text inside our rectangular box
    result = img[y:y+h,x:x+w]
    # convert image to string
    img_string = pytesseract.image_to_string(result)
    # remove \n from our string
    img_string = img_string.replace("\n", "")

    # return text in the form of string
    return img_string



def createEventsICS(assignments_list, dates_list):
    print(calendar)
    c = calendar
    e = events
    e.name = str(assignments_list[0])
    e.begin = str(dates_list[0])
    c.events.add(e)
    c.events
    # [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
    with open('my.ics', 'w') as my_file:
        my_file.writelines(c)



def main():
    # array to hold our assignment dates and names
    dates_list = []
    assignments_list = []
    # get path to file that can read text in images
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
    # get image
    img = cv2.imread('Schedule.png')
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
        result = getText(contours[i], img)
        # temp solution as we test:
        # if even index, result is assignment name
        if(i % 2 == 0 ):
            assignments_list.append(result)
        # if odd, result is date
        else:
            dates_list.append(result)

    # get tuple containing (rows,columns)
    row_col = countRowsAndColumns(contours, img)
    # convert image to table format
    img = imgToTable(contours,img, row_col)


    for x in assignments_list:
        print(x)

    print()
    for y in dates_list:
        print(y)


    #test: show image of the desired result
    cv2.imshow('Box Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
main()