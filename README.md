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
