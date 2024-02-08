"""
PDF Renamer, v 0.4

Русский:

Этот скрипт предназначен для переименования и перемещения файлов PDF на основе текста определенного формата (в текущей
версии производится поиск текста выделенного жирным шрифтом), извлеченного с первой страницы с текстом каждого
PDF-файла.

Использование:
    1. Убедитесь, что в вашей системе установлен Python 3.x.
    2. Сохраните этот скрипт и файл requirements.txt в нужной вам директории.
    3. Установите необходимые зависимости, выполнив команду: python -m pip install -r requirements.txt (или pip install
    -r requirements.txt)
    4. Укажите путь к папке с PDF-файлами в переменной folder_path в скрипте.
    5. Запустите скрипт.

Функциональность:
    - Скрипт извлекает текст с первой страницы с текстом каждого PDF-файла в указанной пользователем папке. Если на
    первой странице не нашлось подходящего по формату текста, скрипт переходит к следующей странице.
    - Извлеченный текст используется для формирования нового имени файла с учетом допустимых символов.
    - Если новое имя файла уже существует и содержимое файлов совпадает, новый файл удаляется вместе с исходным
    PDF-файлом. Если содержимое разное, к имени файла добавляется индекс.
    - Переименованные файлы перемещаются в отдельную папку "Renamed", создаваемую автоматически внутри указанной папки.
    - Выводится количество успешно переименованных файлов, количество ошибок, количество файлов с
    одинаковым содержимым.

Замечания:
    - В случае ошибок при обработке текущего файла, код будет продолжать обработку следующего файла.
    - Предварительно убедитесь, что PDF-файлы имеют текст указанного выше формата для успешного извлечения и
    переименования.

Автор: Артем Шенберг (@artshenberg).
Дата последнего обновления: 08 февраля 2024 г.


English:

This script is designed to rename and move PDF files based on the text of a specific format (currently searches for text
highlighted in bold font), extracted from the first page with text of each PDF file.

Usage:
    1. Make sure Python 3.x is installed on your system.
    2. Save this script and the requirements.txt file in the desired directory.
    3. Install the necessary dependencies by running: python -m pip install -r requirements.txt (or pip install -r
    requirements.txt)
    4. Specify the path to the folder containing the PDF files in the 'folder_path' variable in the script.
    5. Run the script.

Functionality:
    - The script extracts text from the first page with text of each PDF file in the user-specified folder. If no text
    of the specified format is found on the first page, the script takes on to the next page.
    - The extracted text is used to generate a new file name, taking into account permissible characters.
    - If a new file name already exists and the file contents match, the new file is deleted along with the original PDF
    file. If the contents are different, an index is added to the file name.
    - Renamed files are moved to a separate 'Renamed' folder, created automatically within the specified folder.
    - The number of successfully renamed files, the number of errors, and the number of files with the same content are
    outputted.

Notes:
    - In case of errors processing the current file, the code will continue processing the next file.
    - Make sure that the PDF files have text in the specified format above for successful extraction and renaming.

Author: Artem Shenberg (@artshenberg).
Last update: 08 February 2024 y.

"""
import os
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.converter import PDFPageAggregator


def extract_text_from_first_page_with_text(pdf_file):
    """
    Функция для извлечения текста с первой страницы PDF-файла, содержащей текст.
    Function to extract text from the first page of a PDF file containing text.

    Args:
    pdf_file (str): Путь к PDF-файлу.
    Path to the PDF file.

    Returns:
    str: Текст с первой страницы, содержащей текст, или пустая строка, если текст не найден.
    Text from the first page containing text, or an empty string if no text is found.

    """

    # Создать менеджер ресурсов для работы с PDF.
    # Create a resource manager for working with PDFs.
    resource_manager = PDFResourceManager()
    # Создать параметры макета страницы.
    # Create page layout parameters.
    laparams = LAParams()
    # Создать агрегатор страниц для извлечения информации о макете и тексте PDF-страниц.
    # Create a page aggregator to extract layout and text information from PDF pages.
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    # Создать интерпретатор страниц для анализа содержимого PDF-страниц.
    # Create a page interpreter to analyze the content of PDF pages.
    interpreter = PDFPageInterpreter(resource_manager, device)

    with open(pdf_file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBox):
                    text = element.get_text().strip()
                    if text:
                        return text
    return ""


def sanitize_filename(filename: str) -> str:
    """
    Функция для очистки имени файла от недопустимых символов.
    Function to sanitize a filename by removing illegal characters.
    """
    return re.sub(r'[^\w\-_.()]', '_', filename)


def rename_pdfs(folder_path: str):
    """
    Функция для переименования и перемещения файлов PDF в указанную папку.
    Function to rename and move PDF files in the specified folder.

    Args:
    folder_path (str): Путь к папке с PDF файлами.
    Path to the folder containing PDF files.

    """
    if not os.path.isdir(folder_path):
        print(f"Папка '{folder_path}' не существует.")
        print(f"Folder '{folder_path}' does not exist.")
        return

    # Создать папку 'Renamed' для перемещения переименованных файлов
    # Create a 'Renamed' folder to move renamed files
    renamed_folder_path = os.path.join(folder_path, "Renamed")
    os.makedirs(renamed_folder_path, exist_ok=True)

    # Счетчик успешно переименованных файлов
    # Counter for successfully renamed files
    renamed_count = 0
    # Счетчик неуспешных попыток переименования
    # Counter for unsuccessful renaming attempts
    fails_count = 0
    # Счетчик файлов с одинаковым содержимым
    # Counter for files with identical content
    same_content_count = 0

    # Словарь для хранения содержимого файлов с одинаковым именем
    # Dictionary to store content of files with the same name
    file_contents = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(folder_path, file_name)
            first_page_text = extract_text_from_first_page_with_text(file_path)
            if not first_page_text:
                print(f"Не удалось найти текст на первых страницах файла: {file_name}. " 
                      f"Продолжение со следующим файлом.")
                print(f"Failed to find text on the first pages of the file: {file_name}. "
                      f"Continuing with the next file.")
                continue
            # Удалить недопустимые символы
            # Remove illegal characters
            new_file_name = sanitize_filename(first_page_text.strip())
            # Сократить имя файла до допустимой длины
            # Shorten the filename to a permissible length
            new_file_name = new_file_name[:255]
            new_file_name = new_file_name + '.pdf'
            new_file_path = os.path.join(folder_path, new_file_name)

            # Проверить, существует ли файл с таким именем
            # Check if a file with the same name exists
            if os.path.exists(new_file_path):
                # Генерирует уникальный суффикс
                # Generate a unique suffix
                count = 1
                while os.path.exists(new_file_path):
                    base_name, extension = os.path.splitext(new_file_name)
                    new_file_name = f"{base_name}_{count}{extension}"
                    new_file_path = os.path.join(folder_path, new_file_name)
                    count += 1

            try:
                # Проверить, существует ли уже файл с таким именем в словаре
                # Check if a file with the same name already exists in the dictionary
                if new_file_name in file_contents:
                    # Сравнить содержимое текущего и существующего файла
                    # Compare the content of the current and existing file
                    current_content = open(file_path, 'rb').read()
                    existing_content = file_contents[new_file_name]

                    if current_content == existing_content:
                        # Содержимое совпадает, удалить новый файл
                        # Content matches, delete the new file
                        os.remove(file_path)
                        # Увеличить счетчик файлов с одинаковым содержимым
                        # Increment the counter for files with identical content
                        same_content_count += 1
                        print(
                            f"Файл {file_name} удален, так как содержимое совпадает с файлом {file_name} в папке "
                            f"'Renamed'.")
                        print(
                            f"File {file_name} deleted, as its content matches the file {file_name} in the 'Renamed' "
                            f"folder.")
                        continue
                    else:
                        # Содержимое не совпадает, добавить к имени файла индекс
                        # Content does not match, add an index to the filename
                        base_name, extension = os.path.splitext(new_file_name)
                        new_file_name = f"{base_name}_{count}{extension}"
                        new_file_path = os.path.join(folder_path, new_file_name)
                        count += 1

                os.rename(file_path, new_file_path)
                print(f"Файл переименован: {file_name} -> {new_file_name}")
                print(f"File renamed: {file_name} -> {new_file_name}")

                # Переместить переименованный файл в папку 'Renamed'
                # Move the renamed file to the 'Renamed' folder
                renamed_file_path = os.path.join(renamed_folder_path, new_file_name)
                os.replace(new_file_path, renamed_file_path)

                # Добавить содержимое файла в словарь
                # Add the file's content to the dictionary
                file_contents[new_file_name] = open(renamed_file_path, 'rb').read()

                # Увеличить счетчик успешно переименованных файлов
                # Increment the counter for successfully renamed files
                renamed_count += 1
            except Exception as e:
                # Увеличить счетчик неуспешных попыток переименования
                # Increment the counter for unsuccessful renaming attempts
                fails_count += 1
                print(f"Ошибка при обработке файла {file_name}: {e}. Продолжение с следующим файлом.")
                print(f"Error processing file {file_name}: {e}. Continuing with the next file.")
                continue

    # Вывод количество успешно переименованных файлов
    # Output the number of successfully renamed files
    print(f"Успешно переименовано {renamed_count} файлов.")
    print(f"Successfully renamed {renamed_count} files.")
    # Вывод количество неуспешных попыток переименования
    # Output the number of unsuccessful renaming attempts
    if fails_count > 0:
        print(f"Не удалось переименовать {fails_count} файлов.")
        print(f"Failed to rename {fails_count} files.")
    # Вывод количество файлов с одинаковым содержимым
    # Output the number of files with identical content
    if same_content_count > 0:
        print(f"Удалено {same_content_count} файлов с одинаковым содержимым.")
        print(f"Deleted {same_content_count} files with identical content.")


if __name__ == "__main__":
    # Ввод путь к вашей папке с PDF файлами
    # Input the path to your folder with PDF files
    folder_path = input("Введите путь к вашей папке с PDF файлами: \n" 
                        "Enter the path to your folder with PDF files: ")
    rename_pdfs(folder_path)
