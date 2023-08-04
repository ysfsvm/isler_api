import os
import json
import requests

def list_available_courses():
    if not os.path.exists("data") or not os.listdir("data"):
        print("Uyarı: 'data' klasörü bulunamadı veya boş. Lütfen download_book_data.py kullanarak ders verilerini indirin!")
        return []
    
    course_files = [filename for filename in os.listdir("data") if filename.startswith("data_") and filename.endswith(".json")]
    course_names = [filename[len("data_"):-len(".json")] for filename in course_files]
    return course_names


def process_selected_json(ders_adi):
    json_filename = f"data/data_{ders_adi}.json"
    
    if not os.path.exists(json_filename):
        print(f"{ders_adi} adında bir JSON dosyası bulunamadı.")
        return
    
    with open(json_filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        
        print("Mevcut kategoriler:")
        for index, category in enumerate(data["categories"], start=1):
            print(f"{index}. {category['Name']}")
        
        selected_category_index = int(input("Lütfen bir kategori numarası seçin: ")) - 1
        
        if selected_category_index < 0 or selected_category_index >= len(data["categories"]):
            print("Geçersiz kategori numarası.")
            return
        
        selected_category = data["categories"][selected_category_index]
    
    kategori_klasor_adi = selected_category["Name"].replace(" ", "-")

    for book in selected_category["Books"]:
        book_name = book["bookName"]
        swf_file_url = book["swfFile"]
        
        ders_klasor_adi = ders_adi.replace(" ", "-")
        kitap_klasor_yolu = os.path.join("books", ders_klasor_adi, kategori_klasor_adi)
        os.makedirs(kitap_klasor_yolu, exist_ok=True)
        
        swf_file_name = f"{book_name}.swf"
        swf_file_path = os.path.join(kitap_klasor_yolu, swf_file_name)
        
        print(f"{book_name} indiriliyor...")
        response = requests.get(swf_file_url)
        with open(swf_file_path, "wb") as swf_file:
            swf_file.write(response.content)
        
        print(f"{book_name} kaydedildi: {swf_file_path}")

        

available_courses = list_available_courses()
print("Mevcut ders adları:", available_courses)

ders_adi = input("Lütfen bir ders adı seçin: ")

if ders_adi in available_courses:
    process_selected_json(ders_adi)
else:
    print("Geçersiz ders adı.")
