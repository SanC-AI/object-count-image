import cv2
import numpy as np
import random

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray_scale", gray)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    cv2.imshow("blurred_image",blurred)
    return blurred



def count_objects(image_path):
    preprocessed = preprocess_image(image_path)
    edged = cv2.Canny(preprocessed, 1, 100)
    cv2.imshow("binary_image", edged)

     # Adaptive thresholding
    #_, thresh = cv2.threshold(preprocessed, 0, 20, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imshow("threshold_image", thresh)

    #contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
    
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    object_sizes = [cv2.contourArea(contour) for contour in contours]
    avg_size = sum(object_sizes) / len(object_sizes)
    
    min_area = avg_size * 0.015  # Adjust the fraction as needed
    max_distance = avg_size * -0.2  # Adjust the fraction as needed
    print(f"min_area : {min_area} max_distance : {max_distance}")

    # Print the total number of contours found
    print(f"Total contours found: {len(contours)}")

    # Merge closely located contours into a single contour
    merged_contours = []
    contour_count = 0
    for contour in contours:
        #print(f"Area of contour objects: {cv2.contourArea(contour)}")
        if cv2.contourArea(contour) > min_area:
            M = cv2.moments(contour)
            cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])  # Centroid coordinates

            #color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
            #cv2.putText(preprocessed,str(contour_count), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            #contour_count += 1

            if not merged_contours:
                merged_contours.append(contour)
            else:
                merged = False
                for index, merged_contour in enumerate(merged_contours):
                    #print(f"distande of merged contour is: {cv2.pointPolygonTest(merged_contour, (cX, cY), True)}")
                    if cv2.pointPolygonTest(merged_contour, (cX, cY), True) > max_distance:
                        merged_contours[index] = np.concatenate((merged_contour, contour))
                        merged = True
                        break
                if not merged:
                    merged_contours.append(contour)

    
    count = 0
    for contour in merged_contours:
        #print(f"Area of merged_contours objects: {cv2.contourArea(contour)}")
        if cv2.contourArea(contour) > min_area:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            color = (random.randint(30, 100), random.randint(40, 100), random.randint(50, 100))
            cv2.drawContours(preprocessed, [contour], -1, color, 2)

            # Get the center of the contour for placing the text
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.putText(preprocessed,str(count), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            count += 1
            
    return preprocessed, count


#image_path = 'my_clutterd_desk.jpeg'
image_path = '3_objects.jpeg'
#orig_image = cv2.imread(image_path)
#cv2.imshow("Original Image", orig_image)
processed_image, object_count = count_objects(image_path)

print(f"Number of objects: {object_count}")

cv2.imshow("Processed Image", processed_image)
cv2.waitKey(0)
#if cv2.waitKey(1) & 0xFF == ord('q'):
    #print("We have received the q key\n")
cv2.destroyAllWindows()
