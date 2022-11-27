def getNumberPlateText(img_path):
    import numpy as np
    import cv2
    import imutils 
    import easyocr

    img = cv2.imread(img_path)  
    img = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)
    img = cv2.edgePreservingFilter(img, flags=1, sigma_s=64, sigma_r=0.2)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    Filter = cv2.bilateralFilter(gray, 11, 17, 17)      # noise reduction
    edged = cv2.Canny(Filter, 200, 250)    # Edge Detection

    keys = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    contours = imutils.grab_contours(keys) 
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None 
    for contour in contours: 
        approx = cv2.approxPolyDP(contour, 10, True) 
        if len(approx) == 4:  
            location = approx 
            break

    mask = np.zeros(gray.shape, np.uint8) 
    new_img = cv2.drawContours(mask, [location], 0, 255, -1) 
    new_img = cv2.bitwise_and(img, img, mask=mask) #use to findout the segment of number plate.

    (x,y) = np.where(mask==255) 
    (x1, y1) = (np.min(x), np.min(y)) 
    (x2, y2) = (np.max(x), np.max(y)) 

    cropped_img = gray[x1:x2+1, y1:y2+1]

    reader = easyocr.Reader(['en']) 
    result = reader.readtext(cropped_img)

    text = ""
    for i in result:
        text += i[-2] + " "   # we are taking the 2nd element from the last of the 2d array.
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0), 3)

    return text