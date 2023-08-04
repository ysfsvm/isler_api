import os
import requests
import json
import xml.etree.ElementTree as ET
from colorama import Fore, Back, Style
from datetime import datetime

with open('keys.json', 'r') as keys_file:
    keys_data = json.load(keys_file)
    url_template = keys_data['url']

def download_lesson_data():
    lesson_names = list(keys_data['keys'].keys())
    lesson_names_str = ", ".join(lesson_names)

    while True:
        selected_lesson = input(f"\nHangi dersin verisini indirmek istersiniz? (tümü, {lesson_names_str}): ")

        if selected_lesson.lower() == 'tümü':
            for lesson in lesson_names:
                download_lesson_file(lesson)
            break
        elif selected_lesson.lower() in keys_data['keys']:
            download_lesson_file(selected_lesson.lower())
            break
        else:
            print(Fore.RED + "Geçersiz ders adı. Lütfen listede olan bir ders adı veya 'tümü' girin." + Style.RESET_ALL)

def download_lesson_file(lesson_name):
    key = keys_data['keys'][lesson_name]
    url = url_template.replace("{key}", key)
    response = requests.get(url)

    if response.status_code == 200:
        folder_name = 'data'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_path = os.path.join(folder_name, f'data_{lesson_name}.xml')
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(Fore.GREEN + f"{lesson_name} verisi başarıyla indirildi!" + Style.RESET_ALL)

        xml_to_json(file_path, lesson_name)

        os.remove(file_path)

    else:
        print(Fore.RED + f"{lesson_name} verisi indirme işlemi başarısız oldu." + Style.RESET_ALL)

def xml_to_json(xml_file_path, lesson_name):
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    xml_data = xml_data.strip()

    root = ET.fromstring(xml_data)
    data = {}

    categories = []
    for aCategory in root.findall('categories/aCategory'):
        category = {}
        category['Name'] = aCategory.find('cName').text
        category['Id'] = int(aCategory.find('cId').text)
        category['Books'] = []
        categories.append(category)

    for pic in root.findall('pics/pic'):
        cId = int(pic.find('cId').text)
        fileName_element = pic.find('fileName')
        mSource_element = pic.find('mSource')

        if fileName_element is not None and mSource_element is not None:
            fileName = fileName_element.text
            mSource = mSource_element.text

            for category in categories:
                if category['Id'] == cId:
                    book_name = mSource.split('/')[-2] 
                    category['Books'].append({
                        'bookName': book_name,
                        'swfFile': mSource + "file-b.txt"
                    })
                    break

    data['categories'] = categories
    data['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Convert to JSON with ensure_ascii=False to handle Turkish characters
    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    json_file_path = xml_file_path.replace('.xml', '.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    print(Fore.CYAN + f"{xml_file_path} JSON olarak kaydedildi: {json_file_path}" + Style.RESET_ALL)

def check_last_updated_dates():
    folder_name = 'data'
    if os.path.exists(folder_name):
        for file_name in os.listdir(folder_name):
            if file_name.endswith('.json'):
                json_file_path = os.path.join(folder_name, file_name)

                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    json_data = json.load(json_file)

                update_date = json_data.get('update_date')
                if update_date:
                    formatted_date = datetime.strptime(update_date, '%Y-%m-%d %H:%M')
                    time_diff = datetime.now() - formatted_date

                    time_diff_str = format_timedelta(time_diff)
                    print(f"{file_name}: {Fore.BLUE}Son Güncellenme Tarihi: {update_date} ({time_diff_str} önce){Style.RESET_ALL}")
                else:
                    print(f"{file_name}: {Fore.RED}Güncellenme tarihi bulunamadı.{Style.RESET_ALL}")

def format_timedelta(td):
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days} gün"
    elif hours > 0:
        return f"{hours} saat"
    else:
        return f"{minutes} dakika"

if __name__ == "__main__":
    check_last_updated_dates()
    download_lesson_data()
