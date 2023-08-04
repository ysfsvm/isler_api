#!/bin/bash

check_command() {
    command -v "$1" >/dev/null 2>&1
}

check_and_install() {
    local command_name="$1"
    local package_name="$2"
    
    if ! check_command "$command_name"; then
        echo "Uyarı: '$command_name' komutu bulunamadı. '$package_name' paketini yükleyerek eksik komutu ekleyebilirsiniz."
        read -p "Devam etmek için ENTER tuşuna basın veya çıkmak için Ctrl+C tuşlarını kullanın."
        if check_command "apt"; then
            sudo apt install -y "$package_name"
        elif check_command "yum"; then
            sudo yum install -y "$package_name"
        elif check_command "brew"; then
            brew install "$package_name"
        elif check_command "pacman"; then
            pacman -S "$package_name"
        else
            echo "Uyarı: Paket yöneticisi bulunamadı. Lütfen '$package_name' paketini manuel olarak yükleyin."
        fi
    fi
}

check_and_install "tput" "ncurses-bin"
check_and_install "parallel" "parallel"
check_and_install "inkscape" "inkscape"
check_and_install "pdftk" "pdftk"
check_and_install "date" "coreutils"

books_dir="books"

# COLORS!
BOLD=$(tput bold)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
RESET=$(tput sgr0)

select_course() {
    courses=("$books_dir"/*/)

    for ((i = 0; i < ${#courses[@]}; i++)); do
        courses[i]=$(basename "${courses[i]%/}")
    done

    PS3="${BOLD}Lütfen bir ders seçin: ${RESET}"
    select course in "${courses[@]}"; do
        if [[ -n "$course" ]]; then
            select_category "$books_dir/$course/"
            break
        else
            echo "${RED}Geçerli bir ders seçeneği seçilmedi.${RESET}"
        fi
    done
}


select_category() {
    local course_dir="$1"
    categories=("$course_dir"/*/)

    for ((i = 0; i < ${#categories[@]}; i++)); do
        categories[i]=$(basename "${categories[i]%/}")
    done

    PS3="Lütfen bir kategori seçin: "
    select category in "${categories[@]}"; do
        if [[ -n "$category" ]]; then
            select_book "$course_dir/$category/"
            break
        else
            echo "Geçerli bir kategori seçeneği seçilmedi."
        fi
    done
}

select_book() {
    local category_dir="$1"
    books=("$category_dir"/*.swf)
    
    for ((i = 0; i < ${#books[@]}; i++)); do
        books[i]=$(basename "${books[i]}" .swf)
    done

    PS3="Lütfen bir kitap seçin: "
    select book in "${books[@]}"; do
        if [[ -n "$book" ]]; then
            convert_book "$category_dir/$book.swf"
            break
        else
            echo "Geçerli bir kitap seçeneği seçilmedi."
        fi
    done
}


convert_book() {
    local input_file="$1"
    local output_dir="out"
    
    file_name=$(basename "$input_file")
    file_name_without_extension="${file_name%.*}"
    
    output_folder="$output_dir/$file_name_without_extension"
    mkdir -p "$output_folder"
    
    ./ffdec_*/ffdec.sh -format sprite:svg -export sprite "$output_folder" "$input_file"

    if [[ $? -ne 0 ]]; then
        echo "Hata: FFDec işlemi başarısız oldu."
        exit 1
    fi

    echo "SWF dosyasından sprite görüntüleri SVG olarak çıkarıldı."

    ls "$output_folder/DefineSprite_1_stage_fla.Symbol1_1"/*.svg | parallel -j$(nproc) '
        file={};
        inkscape --export-filename="${file%.svg}.pdf" --export-type=pdf --export-dpi=120 --vacuum-defs "$file" && rm "$file";
    '

    if [[ $? -ne 0 ]]; then
        echo "Hata: Inkscape işlemi başarısız oldu."
        exit 1
    fi

    echo "SVG dosyaları dönüştürüldü ve silindi."

    output_pdf="${output_dir}/${file_name_without_extension}.pdf"
    pdftk $(ls -v "$output_folder/DefineSprite_1_stage_fla.Symbol1_1"/*.pdf) cat output "$output_pdf"

    if [[ $? -ne 0 ]]; then
        echo "Hata: PDF birleştirme işlemi başarısız oldu."
        exit 1
    fi

    echo "PDF dosyaları birleştirildi: $output_pdf"

    rm -r "$output_folder"
}

start_time=$(date +%s)
select_course

end_time=$(date +%s)
total_time=$((end_time - start_time))
echo "${GREEN}Toplam dönüşüm süresi: $(date -u -d @$total_time +'%H saat %M dakika %S saniye')${RESET}"