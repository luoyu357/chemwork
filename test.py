from utili.alignment import *
from utili.ocr import *
from utili.osra import *

easy = read_name_from_image_easyocr('./image/in/4.png', 0.9)
paddle = read_name_from_image_paddle('./image/in/4.png', 0.9)

easy_new = combine_separated_label_ocr(easy)
paddle_new = combine_separated_label_ocr(paddle)

unique = unique_label(easy_new, paddle_new)

final_ocr = combine_separated_label_ocr(unique)

for i in final_ocr:
    print(i)

osra = runOsraSmiles(inputPath='/Users/luoyu/PycharmProjects/chemwork/image/in', outputPath='/Users/luoyu/PycharmProjects/chemwork/image/smiles', outputName='4.smi', inputName='4.png')
osra_result = get_smiles(osra)

final_result = combine_smiles_label(osra_result, final_ocr, 0.2)
for i in final_result:
    print(i)