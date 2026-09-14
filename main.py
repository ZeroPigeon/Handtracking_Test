import cv2
import numpy as np

camera = cv2.VideoCapture(0)

def nothing(value):
    pass

#tracking bars for testing
cv2.namedWindow("Controls")

cv2.createTrackbar("H Min", "Controls", 0, 176, nothing)
cv2.createTrackbar("H Max", "Controls", 0, 176, nothing)

cv2.createTrackbar("S Min", "Controls", 0, 255, nothing)
cv2.createTrackbar("S Max", "Controls", 0, 255, nothing)

cv2.createTrackbar("V Min", "Controls", 0, 255, nothing)
cv2.createTrackbar("V Max", "Controls", 0, 255, nothing)

cv2.setTrackbarPos("H Max", "Controls", 176)
cv2.setTrackbarPos("S Max", "Controls", 255)
cv2.setTrackbarPos("V Max", "Controls", 255)

# window loop
while True:
    success, frame = camera.read()

    if not success:
        break

    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Trackbar for adjusting HSV colours

    h_min = cv2.getTrackbarPos("H Min", "Controls")
    h_max = cv2.getTrackbarPos("H Max", "Controls")

    s_min = cv2.getTrackbarPos("S Min", "Controls")
    s_max = cv2.getTrackbarPos("S Max", "Controls")

    v_min = cv2.getTrackbarPos("V Min", "Controls")
    v_max = cv2.getTrackbarPos("V Max", "Controls")

    lower_colour = np.array([h_min, s_min, v_min])
    upper_colour = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(image_hsv, lower_colour, upper_colour)

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    contours, __ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_image = frame.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 3)

    if contours:

        hand_contour = max(contours, key=cv2.contourArea)   

        M = cv2.moments(hand_contour)

        if M["m00"] != 0:
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
        else:
            center_x = 0
            center_y = 0

        cv2.circle(contour_image, (center_x, center_y), 8, (255, 255, 0), -1)

        cv2.drawContours(contour_image, hand_contour, -1, (180, 180, 180), 3)

        #Bounding box for debug
        x, y, w, h = cv2.boundingRect(hand_contour)
        cv2.rectangle(contour_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        hull = cv2.convexHull(hand_contour)
        cv2.drawContours(contour_image, [hull], -1, (255, 255, 255), 2)

        hull_indicies = cv2.convexHull(hand_contour, returnPoints=False)
        defects = cv2.convexityDefects(hand_contour, hull_indicies)

        if defects is not None:

            for defect in defects:
                start, end, farthest, distance = defect.flatten()

                actual_distance = distance / 256

                print("Distance:", actual_distance)

                if actual_distance > 30:

                    start_x, start_y = hand_contour[start][0]
                    valley_x, valley_y = hand_contour[farthest][0]
                    end_x, end_y = hand_contour[end][0]

                    cv2.circle(contour_image, (valley_x, valley_y), 7, (0, 0, 255), -1)
                    cv2.circle(contour_image, (start_x, start_y), 7, (0, 255, 0), -1)
                    cv2.circle(contour_image, (end_x, end_y), 7, (255, 0, 0), -1)

            fingertips = []

            for points in hull:
                x, y = points[0]

                dx = x - center_x
                dy = y - center_y

                distance = np.sqrt(dx**2 + dy**2)

                if distance > 80:
                    fingertips.append((x, y))

            for x, y in fingertips:
                cv2.circle(contour_image, (x, y), 8, (0, 255, 255), -1)

                cv2.putText(contour_image, f"({x}, {y})", (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    cv2.imshow("Contours", contour_image)
    cv2.imshow("Mask image", result)
    cv2.imshow("HSV image", image_hsv)
    #cv2.imshow("Normal image", frame)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()