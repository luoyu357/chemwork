"""
Developer Name : Tarini Dash<tdash@iu.edu>
Date : 09/15/2021
Description : This program is responsible for reading a HTML file and extracts chemical information about of it
along with abbreviation and bibilio
Citation : Swain, M. C., & Cole, J. M. "ChemDataExtractor: A Toolkit for Automated Extraction of Chemical Information
from the Scientific Literature", J. Chem. Inf. Model. 2016, 56 (10), pp 1894–1904 10.1021/acs.jcim.6b00207
"""

import configparser
import uuid
from pprint import pprint

import cirpy
from chemdataextractor import Document
from chemdataextractor.scrape import Selector
from chemdataextractor.scrape.pub.rsc import RscHtmlDocument
import os
import tempfile
import subprocess
import pathlib
import json

from chemdataextractor.text.normalize import chem_normalize
from pymongo import MongoClient

from image.get_image_from_pdf import read_PDF
from image.photo_capture import capture_image
from mongodb.store import store
from utili.alignment import combine_smiles_label
from utili.convert_smiles_string_to_image import convert_string_to_structure
from utili.ocr import *
from utili.osra import *
from utili.pubchem import pubchem
from utili.similarity_label import similarity
from utili.utility import transform_biblio, apply_rules


def add_structures(result, label_smiles):
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        for record in result['records']:
            for name in record.get('names', []):
                tf.write(('%s\n' % name).encode('utf-8'))

    subprocess.call(
        ['java', '-jar', 'opsin-cli-2.7.0-jar-with-dependencies.jar',
         '--allowRadicals', '--wildcardRadicals',
         '--allowAcidsWithoutAcid', '--allowUninterpretableStereo', '--detailedFailureAnalysis', tf.name,
         '%s.result' % tf.name])
    '''
    subprocess.call([config.get("file", "opsin_loc"), '--allowRadicals', '--wildcardRadicals',
                     '--allowAcidsWithoutAcid', '--allowUninterpretableStereo', '--detailedFailureAnalysis', tf.name,
                     '%s.result' % tf.name])
    '''
    with open('%s.result' % tf.name) as res:
        structures = [line.strip() for line in res]
        i = 0
        smile_name_checker = pubchem()
        for record in result['records']:

            for name in record.get('names', []):
                if 'smiles' not in record:
                    if structures[i]:
                        print(name, " related smiles ", structures[i])
                        #print(f'Resolved with OPSIN: %s = %s', name, structures[i])
                        record['smiles'] = structures[i]
                    else:

                        smiles = cirpy.resolve(chem_normalize(name.rstrip("\n\r")).encode('utf-8'), 'smiles')

                        print(name, ' related smiles ', smiles)

                        if smiles:
                            record['smiles'] = smiles
                        else:
                            smiles = []
                            delete_label_smile = []
                            max_score = 0
                            for label_smile in label_smiles:
                                if len(label_smile) == 10:
                                    similarity_score = similarity(label_smile[6], name)
                                    if similarity_score >= max_score:
                                        delete_label_smile = label_smile
                                        max_score = similarity_score

                            print(delete_label_smile)
                            if len(delete_label_smile) > 0:
                                pubchem_name_text = smile_name_checker.searchCompoundName(name)
                                pubchem_name_label = smile_name_checker.searchCompoundName(delete_label_smile[6])
                                pubchem_smile = smile_name_checker.searchCompoundSmiles(delete_label_smile[0])

                                temp_name = str(uuid.uuid4()) + '.png'
                                random_file_capture_image_path = config.get('file', 'image_out_dir') + temp_name
                                capture_image(delete_label_smile, random_file_capture_image_path)

                                mongo_capture_image_id = store(config, random_file_capture_image_path)

                                remake_file_path = config.get('file', 'remake_smile_image_dir') + temp_name
                                convert_string_to_structure(delete_label_smile[0], remake_file_path)

                                mongo_remake_image_id = store(config, remake_file_path)

                                smiles.append({'alter_name': delete_label_smile[6],
                                               'alter_name_confidence': delete_label_smile[7],
                                               'alter_name_not_original': delete_label_smile[8],
                                               'pubchem_name_check': pubchem_name_text+pubchem_name_label,
                                               'alter_smiles': delete_label_smile[0],
                                               'alter_smiles_confidence': delete_label_smile[3],
                                               'pubchem_smiles_check': pubchem_smile,
                                               'sub_image_path': random_file_capture_image_path,
                                               'openbabel_image_path': remake_file_path,
                                               'sub_image_id_mongodb': str(mongo_capture_image_id),
                                               'openbabel_image_id_mongodb': str(mongo_remake_image_id)})

                                # label_smiles.remove(delete_label_smile)

                            if len(smiles) > 0:

                                record['smiles'] = smiles
                            else:
                                record['smiles_validation_failed'] = "1"
                i += 1

    os.remove(tf.name)
    os.remove('%s.result' % tf.name)
    return result


def process(collection, config):
    for path in pathlib.Path(config.get("file", "input_dir")).iterdir():
        if path.is_file() and not path.stem.startswith('.'):
            f_name = path.stem
            with open(path, 'rb') as f_input:
                htmlstring = f_input.read()
                # scrape for biblio
                sel = Selector.from_html_text(htmlstring)
                scrape = RscHtmlDocument(sel)
                biblio = scrape.serialize()

                f_input.seek(0)
                doc = Document.from_file(f_input)

                # download images from the pdf
                pdf_path = config.get('file', 'pdf_dir') + f_name + '.pdf'
                image_in_path = config.get('file', 'image_in_dir')
                read_PDF(pdf_path, image_in_path)

                # read image and smiles
                final_result = []

                for image_path in pathlib.Path(image_in_path).iterdir():
                    if image_path.is_file() and not path.stem.startswith('.'):
                        easy = read_name_from_image_easyocr(str(image_path), 0.9)
                        paddle = read_name_from_image_paddle(str(image_path), 0.9)

                        easy_new = combine_separated_label_ocr(easy)
                        paddle_new = combine_separated_label_ocr(paddle)

                        unique = unique_label(easy_new, paddle_new)

                        final_ocr = combine_separated_label_ocr(unique)

                        for i in final_ocr:
                            print(i)

                        osra = runOsraSmiles(inputPath=image_in_path,
                                             outputPath=config.get('file', 'smiles_dir'),
                                             outputName=image_path.stem+'.smi', inputName=image_path.stem+'.png')
                        osra_result = get_smiles(osra)

                        result = combine_smiles_label(osra_result, final_ocr, 0.2, str(image_path))

                        final_result+=result

                for i in final_result:
                    print(i)
                records = apply_rules(doc.records.serialize(), config)

                # records = natsort.natsorted(records,
                #                             lambda x: x.get('labels', ['ZZZ%s' % (99 - len(x.get('names', [])))])[0])
                # scrape for abbreviation
                # abbreviations = doc.abbreviation_definitions
                # result = {'abbreviations': abbreviations, 'biblio': biblio, 'records': records}
                result = {'biblio': transform_biblio(biblio), 'records': records}
                result = add_structures(result, final_result)
                final = [result]
                pprint(final)

                with open(config.get("file", "output_dir") + f_name + '.json', 'w', encoding='utf-8') as f_output:
                    json.dump(final, f_output)

                print('wrote to json file successfully')
                collection.insert_one(result)
                print('wrote to mongodb successfully')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")
    # cirpy.API_BASE = 'https://cactus.nci.nih.gov/chemical/structure'
    client = MongoClient(config.get("database", "mongodb_uri"))
    db = client[config.get("database", "db")]
    serverStatusResult = db.command("serverStatus")
    #print(serverStatusResult)
    collection = db[config.get("database", "collection")]
    process(collection_name=collection,config = config)
    client.close()
