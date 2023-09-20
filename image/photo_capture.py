import cv2

def capture_image(label_smile, save):
    image = cv2.imread(label_smile[9])

    smile_x = label_smile[1]
    smile_y = label_smile[2]
    name_x = label_smile[4]
    name_y = label_smile[5]
    x1 = int(min(min(smile_x), min(name_x)))
    x2 = int(max(max(smile_x), max(name_x)))
    y1 = int(min(min(smile_y), min(name_y)))
    y2 = int(max(max(smile_y), max(name_y)))

    y, x, c = image.shape

    if x1 < 0: x1 = 0
    if x2 > x: x2 = x
    if y1 < 0: y1 = 0
    if y2 > y: y2 = y

    crop_img = image[int(y1):int(y2), int(x1):int(x2)]
    cv2.imwrite(save, crop_img)

