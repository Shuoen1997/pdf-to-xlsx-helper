from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextBox, LAParams
import xlsxwriter

# Replace this line with the PDF file path you want to convert 
# It can be relative path (from where this file is stored)
# Or absolute path on the computer
# Both Chinese and English are supported!
PDF_NAME = "pdf_folder/2021012201275_c.pdf"

# Replace this if you want to experiment with a different line margin
# See https://pdfminersix.readthedocs.io/en/latest/reference/composable.html#api-laparams
LINE_MARGIN = 0.7

RESULT = {}
def extract_PDF_textbox():
    text_group_index = 0
    for page_layout in extract_pages(PDF_NAME, laparams=LAParams(line_margin=LINE_MARGIN)):
        for element in page_layout:
            if isinstance(element, LTTextBox):
                text_group_index += 1
                RESULT[text_group_index] = []
                for text_line in element:
                    text = text_line.get_text()
                    RESULT[text_group_index].append(text)

    print(f"Coverted {text_group_index} group of texts from PDF")

def convert_to_xlsx():
    output_file_name =  PDF_NAME.replace('pdf_folder/', 'xlsx_folder/').strip('.pdf') + '.xlsx'
    workbook = xlsxwriter.Workbook(output_file_name)
    worksheet = workbook.add_worksheet()
    # Expand the column A
    worksheet.set_column('A:A', 100)

    index = 1
    for _, text_group in RESULT.items():
        # Assign the index the text should be in
        box = 'A' + str(index)
        if is_text_group_number_only(text_group):
            continue
        
        s = ''.join(text_group)
        # We don't want page number either 
        if is_page_number_or_next_line_symbol(s):
            continue
        
        worksheet.write(box, s)
        index += 1

    workbook.close()
    print(f'Created {index} row in xlsx after stripping number only row!')

def is_page_number_or_next_line_symbol(text):
    return text[0] == '–' or text[0] == '\n'


def is_text_group_number_only(text_group):
    for v in text_group:
        if not is_number_only(v):
            return False
    return True

def is_number_only(text):
    import re 

    pattern = re.compile('[(]*([0-9]*[,%]*[0-9]*)*[)]*([\ ])*([\n])*')
    return pattern.fullmatch(text)

if __name__ == '__main__':
    if '_c' in PDF_NAME:
        print("正在轉換中文的PDF...")
    else:
        print("Converting English PDF...")
    
    extract_PDF_textbox()
    convert_to_xlsx()
    
