import easyocr
from paddleocr import PaddleOCR


# pip install paddleocr --upgrade
# pip install paddlepaddle


def read_name_from_image_easyocr(file_path, lowest_accuracy=0.9):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path)
    output = []
    for item in result:

        coordinate = item[0]
        x1 = int(coordinate[0][0])
        x2 = int(coordinate[1][0])
        y1 = int(coordinate[1][1])
        y2 = int(coordinate[2][1])
        name = item[1]
        accuracy = item[2]

        if accuracy < lowest_accuracy:
            continue
        output.append([[x1, x2], [y1, y2], name, accuracy])

    return output


def read_name_from_image_paddle(file_path, lowest_accuracy=0.9):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to download and load model into memory
    img_path = file_path
    result = ocr.ocr(img_path, cls=True)
    output = []
    for item in result[0]:
        coordinate = item[0]
        x1 = int(coordinate[0][0])
        x2 = int(coordinate[1][0])
        y1 = int(coordinate[1][1])
        y2 = int(coordinate[2][1])
        name = item[1][0]
        accuracy = item[1][1]

        if accuracy < lowest_accuracy:
            continue
        output.append([[x1, x2], [y1, y2], name, accuracy])
    # [[276, 316], [252, 282], '16', 0.9146661332719246, 'False']
    return output

# step
# 1. combine_separated_label_ocr: combine labels for one output of OCR
# 2. unique_label: for several OCR outputs
# 3. combine_separated_label_ocr: combine several outputs of different OCR


# combine the separated labels according to coordinates
# if left and right combination, no special symbols
# if up and down combination, ';' is added
# 'True' means the output is combined from other outputs
# 'False' means nothing happened
def combine_separated_label_ocr(input):
    output = []

    for item in input:
        x1 = item[0][0]
        x2 = item[0][1]
        y1 = item[1][0]
        y2 = item[1][1]

        name = item[2]
        accuracy = item[3]

        if len(output) != 0:
            done = True
            for temp in output:

                x = temp[0]
                y = temp[1]

                # check two labels overlap on x-axis
                # 1. values of y-axis are in the same range (>=50%)
                # 2.1 values of x-axis are partially overlapped (-20% <= overlap <= 50%)
                # 2.2 determine the order of labels ()left, right)

                if ((y[0] >= y1 and y2 >= y[1]) or
                        (y1 >= y[0] and y[1] >= y2) or
                        (y[0] <= y1 <= y[1] and ((y[1] - y1) / min((y2 - y1), (y[1] - y[0])) >= 0.5)) or
                        (y[0] <= y2 <= y[1] and ((y2 - y[0]) / min((y2 - y1), (y[1] - y[0])) >= 0.5))):

                    if x[1] <= x2:
                        if -0.2 <= (x[1] - x1) / (x2 - x[0]) <= 0.5:
                            if name in temp[2]:
                                temp[2] = temp[2]
                            elif temp[2] in name:
                                temp[2] = name
                            else:
                                temp[2] = temp[2] + name
                            temp[0][0], temp[0][1] = min(x1, x[0]), max(x2, x[1])
                            temp[1][0], temp[1][1] = min(y1, y[0]), max(y2, y[1])
                            temp[4] = 'True'
                            done = False
                            break

                    if x1 <= x[0]:
                        if -0.2 <= (x2 - x[0]) / (x[1] - x1) <= 0.5:
                            if name in temp[2]:
                                temp[2] = temp[2]
                            elif temp[2] in name:
                                temp[2] = name
                            else:
                                temp[2] = name + temp[2]
                            temp[0][0], temp[0][1] = min(x1, x[0]), max(x2, x[1])
                            temp[1][0], temp[1][1] = min(y1, y[0]), max(y2, y[1])
                            temp[4] = 'True'
                            done = False
                            break

                # check two labels overlap on y-axis
                # 1. values of x-axis are in the same range (>=50%)
                # 2.1 values of y-axis are partially overlapped (-20% <= overlap <= 50%)
                # 2.2 determine the order of labels (up, down)

                if ((x[0] >= x1 and x2 >= x[1]) or
                        (x1 >= x[0] and x[1] >= x2) or
                        (x[0] <= x1 <= x[1] and (x[1] - x1) / min((x2 - x1), (x[1] - x[0])) >= 0.5) or
                        (x[0] <= x2 <= x[1] and (x2 - x[0]) / min((x2 - x1), (x[1] - x[0])) >= 0.5)):

                    if y[1] <= y2:
                        if -0.2 <= (y[1] - y1) / (y2 - y[0]) <= 0.5:
                            if name in temp[2]:
                                temp[2] = temp[2]
                            elif temp[2] in name:
                                temp[2] = name
                            else:
                                temp[2] = temp[2] + ";" + name
                            temp[0][0], temp[0][1] = min(x1, x[0]), max(x2, x[1])
                            temp[1][0], temp[1][1] = min(y1, y[0]), max(y2, y[1])
                            temp[4] = 'True'
                            done = False
                            break

                    if y1 <= y[0]:
                        if -0.2 <= (y2 - y[0]) / (y[1] - y1) <= 0.5:
                            if name in temp[2]:
                                temp[2] = temp[2]
                            elif temp[2] in name:
                                temp[2] = name
                            else:
                                temp[2] = name + ";" + temp[2]
                            temp[0][0], temp[0][1] = min(x1, x[0]), max(x2, x[1])
                            temp[1][0], temp[1][1] = min(y1, y[0]), max(y2, y[1])
                            temp[4] = 'True'
                            done = False
                            break

            if done:
                if len(item) > 4:
                    output.append([[x1, x2], [y1, y2], name, accuracy, item[4]])
                else:
                    output.append([[x1, x2], [y1, y2], name, accuracy, 'False'])
        else:
            if len(item) > 4:
                output.append([[x1, x2], [y1, y2], name, accuracy, item[4]])
            else:
                output.append([[x1, x2], [y1, y2], name, accuracy, 'False'])

    return output


# find any duplicate values based on coordinates
# then check the name
def unique_label(ocr, paddle):
    output = []
    ocr_copy = [i for i in ocr]
    for item_ocr in ocr_copy:
        x_ocr = item_ocr[0]
        y_ocr = item_ocr[1]
        for item_paddle in paddle:
            x_paddle = item_paddle[0]
            y_paddle = item_paddle[1]

            center_ocr = [sum(x_ocr) / 2, sum(y_ocr) / 2]
            center_paddle = [sum(x_paddle) / 2, sum(y_paddle) / 2]

            # center of box must be in the range of other
            if (x_paddle[0] <= center_ocr[0] <= x_paddle[1] and y_paddle[0] <= center_ocr[1] <= y_paddle[1]) or \
                    (x_ocr[0] <= center_paddle[0] <= x_ocr[1] and y_ocr[0] <= center_paddle[1] <= y_ocr[1]):

                name_ocr = item_ocr[2].replace(' ', '')
                name_paddle = item_paddle[2].replace(' ', '')

                if name_ocr == name_paddle:
                    new_name = item_ocr[2]
                elif name_ocr in name_paddle:
                    new_name = item_paddle[2]
                elif name_paddle in name_ocr:
                    new_name = item_ocr[2]
                elif len(name_ocr) >= len(name_paddle):
                    new_name = item_ocr[2] + '(' + item_paddle[2] + ')'
                else:
                    new_name = item_paddle[2] + '(' + item_ocr[2] + ')'

                # remove the duplicate
                new_item = [[min(x_ocr[0], x_paddle[0]), max(x_ocr[1], x_paddle[1])], \
                            [min(y_ocr[0], y_paddle[0]), max(y_ocr[1], y_paddle[1])], new_name,
                            min(item_ocr[3], item_paddle[3]), (item_ocr[4] or item_paddle[4])]
                output.append(new_item)
                ocr.remove(item_ocr)
                paddle.remove(item_paddle)

                break
    return output + ocr + paddle


if __name__ == '__main__':
    easy = read_name_from_image_easyocr('../image/in/8.png', 0.9)
    paddle = read_name_from_image_paddle('../image/in/8.png', 0.9)

    easy_new = combine_separated_label_ocr(easy)
    paddle_new = combine_separated_label_ocr(paddle)

    unique = unique_label(easy_new, paddle_new)

    final = combine_separated_label_ocr(unique)

    for i in final:
        print(i)