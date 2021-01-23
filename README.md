# PDF->XLSX

Step 1. Make sure you have python3.6+ installed!

Step 2. And install the dependencies thru:

`pip3 install requirements.txt`

Step 3. Move the PDF file you want to convert into the `pdf_folder` 

Step 4. Then replace this line in `pdf_convertor.py` with the path of PDF file you want to convert:

>`PDF_NAME = "pdf_folder/2021012201274.pdf"`

Step 5. Then you can run:

`python3 pdf_convertor.py`

Step 6. Tada! The converted output(xlsx) will show up under `xlsx_folder` with the same name as the original PDF.