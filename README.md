# isler_api

isler_api is a Python/Bash-based script collection that allows you to convert books from İşler Zkitap app into PDF format. This project provides an efficient way to transform educational materials from İşler Zkitap into a more accessible and readable format.
  
## Installing

**To use isler_api, follow these steps:**

1.  **Clone the Repository:** Open your terminal and run the following commands to clone the repository and navigate to the project folder:
```bash
git clone https://github.com/ysfsvm/isler_api.git
cd isler_api
```

2.  **Configure API Keys and URL**: Edit the simple_keys.json file by adding your books keys and the URL. Once you've edited the file, rename `simple_keys.json` to `keys.json`. This file is crucial for the conversion process.
> **Due to potential copyright concerns, I'm unable to provide the url and keys.**

3.  **Download Book Data:** Run the download_book_data.py script to download the necessary book data:
```bash
python3 download_book_data.py
```

4.  **Download Books:** Run the download_books.py script to download the books:
```bash
python3 download_books.py
```

5. **Download FFDec:**
   - In the first step, you need to download FFDec from the GitHub Releases page. Visit the FFDec download page: [FFDec GitHub Releases](https://github.com/jindrapetrik/jpexs-decompiler/releases).
   - Locate the latest release and download the zip version.
   - Extract the downloaded file and move the ffdec_xxx a folder to project directory.

6.  **Convert Downloaded Books to PDF:** Finally, execute the book conversion process by running the `convert_book.sh` script:
```bash
./convert_book.sh
```

You've now successfully converted the books into PDF format.

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE.md file for details