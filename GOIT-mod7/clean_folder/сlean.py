import os
import shutil
import sys

def normalize(filename):
    translit_mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia'
    }
    
    normalized_name = ''
    for char in filename:
        char_lower = char.lower()
        if char_lower.isalnum() or char == '.':
            normalized_name += char_lower
        elif char_lower in translit_mapping:
            normalized_name += translit_mapping[char_lower]
        else:
            normalized_name += '_'

    return normalized_name

def sort_folder():
 

    if len(sys.argv) != 2:
        print("Використання: clean-folder <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    base_folder = os.path.abspath(folder_path)
    
    # Список ігнорованих категорій
    ignored_categories = ['archives', 'video', 'audio', 'documents', 'images', 'other']

    # Зберігаємо інформацію про файли у кожній категорії
    file_info = {category: [] for category in ignored_categories}

    for root, dirs, files in os.walk(folder_path):
        # Виключаємо теки, які входять до списку ігноруваних
        dirs[:] = [d for d in dirs if d not in ignored_categories]

        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].upper()[1:]

            category_folder = None
            if file_extension in ['JPEG', 'PNG', 'JPG', 'SVG']:
                category_folder = 'images'
            elif file_extension in ['AVI', 'MP4', 'MOV', 'MKV']:
                category_folder = 'video'
            elif file_extension in ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']:
                category_folder = 'documents'
            elif file_extension in ['MP3', 'OGG', 'WAV', 'AMR']:
                category_folder = 'audio'
            elif file_extension in ['ZIP', 'GZ', 'TAR']:
                category_folder = 'archives'
                archive_path = os.path.join(base_folder, category_folder, os.path.splitext(file)[0])
                shutil.unpack_archive(file_path, archive_path)
                os.remove(file_path)  # Видалення архіву після розпакування
                continue
            else:
                category_folder = 'other'

            # Заповнюємо інформацію про файли
            file_info[category_folder].append(normalize(file))

            category_path = os.path.join(base_folder, category_folder)
            os.makedirs(category_path, exist_ok=True)

            new_filename = normalize(file)
            new_filepath = os.path.join(category_path, new_filename)
            shutil.move(file_path, new_filepath)

    # Видаляємо порожні папки
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    # Виводимо інформацію в консоль
    print("Файли в категоріях:")
    for category, files in file_info.items():
        print(f"{category}: {files}")

    # Відомі розширення
    known_extensions = set()
    for files in file_info.values():
        known_extensions.update([os.path.splitext(file)[1].upper()[1:] for file in files])

    print("\nВідомі розширення:")
    print(known_extensions)

    # Невідомі розширення
    all_extensions = set()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].upper()[1:]
            all_extensions.add(file_extension)

    unknown_extensions = all_extensions - known_extensions

    print("\nНевідомі розширення:")
    print(unknown_extensions)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Використання: python sort.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    sort_folder(folder_path)