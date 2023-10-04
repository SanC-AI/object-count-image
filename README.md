# object-count-image
count the number of objects from given image, using OpenCV

There are below task involved in any object detection prjects.
1. Converting colour image to gray image
2. applying the blur filter. Mainly Gaussian Blur.
3. converting the blur image into binary image.
4. finding the countours in the image.
5. Optional step: Merging the countours. This is optional because, many a times single object may create multiple countours. We need to take the median and find if it lies in or touching other countours. If so merge these two.
6. Draw the final countour or draw the box.
7. increment the object count.


# Importent notes
1. you need to adjust the min_area of countour to consider it an object.
2. You need to adjust the size of kernel in GaussianBlur to adjust the blur effect. Smaller values will result in less blurring, while larger values will increase the blurriness.


# Learning
1. There are multiple parameters which can create the problems. Two are mentioned above.
2. findCountours() function also has different parameters, if change it has given whole different results.
3. Another problem area is merging countours using pointPolygonTest() method. where mean distance of countour from current countour needs to be adjusted. If adjusted properly, countours are merged otherwise you will increase the object count. (counting same object multiple times)
4. This code is very light weight interms of CPU and RAM utlization, when compared with standard CV  models.
