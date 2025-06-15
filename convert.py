import logging
from abc_xml_converter import convert_abc2xml
from abc_xml_converter import convert_xml2abc
import os
import shutil

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Учимся работать с пулл  реквестами
# Пути к папкам
INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
SPENT_INPUT_DIR ='spent_input'

# Создаем папки, если они не существуют
if not os.path.exists(OUTPUT_DIR):
    logging.info(f'Создаем папку {OUTPUT_DIR}')
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(SPENT_INPUT_DIR):
    logging.info(f'Создаем папку {SPENT_INPUT_DIR}')
    os.makedirs(SPENT_INPUT_DIR)
if not os.path.exists(os.path.join(SPENT_INPUT_DIR,'musicxml')):
    logging.info(f'Создаем папку {os.path.join(SPENT_INPUT_DIR,"musicxml")}')
    os.makedirs(os.path.join(SPENT_INPUT_DIR,'musicxml'))
if not os.path.exists(os.path.join(SPENT_INPUT_DIR, 'xml')):
    logging.info(f'Создаем папку {os.path.join(SPENT_INPUT_DIR, "xml")}')
    os.makedirs(os.path.join(SPENT_INPUT_DIR, 'xml'))

def read_file(filename, errmsg='read error: '):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        logging.info(f'Прочитали файл {filename}')
        return content
    except Exception as e:
        logging.error(f'Ошибка чтения файла {filename}: {e}')
        return None

def main():
    logging.info('Начинаем обработку файлов')
    # Обрабатываем все файлы в папке input и ее подпапках
    for root, dirs, files in os.walk(INPUT_DIR):
        logging.info(f'Обрабатываем папку {root}')
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_ext = os.path.splitext(file)
            logging.info(f'Обрабатываем файл {file_path}')

            if file_ext == '.abc':
                # Конвертируем ABC в XML
                logging.info(f'Конвертируем ABC в XML: {file_path}')
                xml_content = convert_abc2xml(file_to_convert=file_path)
                if xml_content is not None:
                    output_file_path = os.path.join(OUTPUT_DIR, file_name + '.xml')
                    logging.info(f'Сохраняем XML-файл: {output_file_path}')
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(xml_content)
                    # Перемещаем обработанный файл в папку spent_input/musicxml
                    spent_file_path = os.path.join(SPENT_INPUT_DIR,'musicxml', file)
                    logging.info(f'Перемещаем файл в папку {SPENT_INPUT_DIR}/musicxml: {file_path} -> {spent_file_path}')
                    shutil.move(file_path, spent_file_path)
                else:
                    logging.error(f'Ошибка конвертации ABC в XML: {file_path}')

            elif file_ext == '.xml':
                # Конвертируем XML в ABC
                logging.info(f'Конвертируем XML в ABC: {file_path}')
                abc_content = convert_xml2abc(file_to_convert=file_path)
                if abc_content is not None:
                    output_file_path = os.path.join(OUTPUT_DIR, file_name + '.abc')
                    logging.info(f'Сохраняем ABC-файл: {output_file_path}')
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(abc_content)
                    # Перемещаем обработанный файл в папку spent_input/xml
                    spent_file_path = os.path.join(SPENT_INPUT_DIR, 'xml', file)
                    logging.info(f'Перемещаем файл в папку {SPENT_INPUT_DIR}/xml: {file_path} -> {spent_file_path}')
                    shutil.move(file_path, spent_file_path)
                else:
                    logging.error(f'Ошибка конвертации XML в ABC: {file_path}')

    logging.info('Обработка файлов завершена')

if __name__ == "__main__":
    main()