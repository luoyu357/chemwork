
def combine_smiles_label(osra, ocr, overlap, image_path):
    for index in range(len(osra)):
        y_distance = 1000000000
        temp_label = []
        for label in ocr:
            # if the max x of label is less than min x of smile or
            # if the min x of label is larger than max x of smile or
            # means the label is not on the same column of the smile
            # if the min y of label is less than min y of smile (label is higher than smile)
            # then ignore

            if label[0][1] <= osra[index][1][0] or \
                    label[0][0] >= osra[index][1][1] or \
                    label[1][0] <= osra[index][2][0]:
                continue

            # new distance: check the min y of label to the max y of smile
            temp_y_distance = abs(osra[index][2][1] - label[1][0])
            # make sure the temp_y_distance is less than overlap rate (10%) of the min y of smile
            # and max y of label
            total_distance = abs(osra[index][2][0] - label[1][1])
            if temp_y_distance / total_distance > overlap:
                continue

            if temp_y_distance <= y_distance:
                y_distance = temp_y_distance
                temp_label = label

        if len(temp_label) > 1:
            osra[index] += temp_label
            osra[index].append(image_path)
            ocr.remove(temp_label)

    # [smile, smile_x_coor, smile_y_coor, smile_confidence, label_x_coor, label_y_coor, label, label_confidence, image_path]
    # ['Cn1c2cccc3c2[Co]2c4c1cccc4oc1c2c(o3)ccc1', [183, 625], [1, 508], 4.07015, [276, 316], [252, 282], '16', 0.9146661332719246, 'False' , '/image']
    # ** convert smiles string to structure again and then present all of them***
    return osra
