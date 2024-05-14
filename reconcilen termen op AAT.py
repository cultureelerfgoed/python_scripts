import requests
import openpyxl
import urllib
import xml.etree.ElementTree as ET
import re
from fuzzywuzzy import fuzz
from operator import itemgetter


# Functie om trefwoorden te reconciliëren met de Getty API op basis van AAT-zoekopdrachten
def reconcile_AAT_keyword(keyword):
    url = "http://vocabsservices.getty.edu/AATService.asmx/AATGetTermMatch?term="
    try:
        response = requests.get(url + urllib.parse.quote(keyword) + '&logop=and&notes=')
        results = ET.fromstring(response.content)
        resources = []
        for child in results.iter('Preferred_Parent'):
            try:
                name = re.sub(r'\[.+?\]', '', child.text.split(',')[0]).strip()
                page_link = re.search(r"\[(.+?)\]", child.text.split(',')[0]).group(1)
                uri = "http://vocab.getty.edu/page/aat/" + page_link
                score = fuzz.token_sort_ratio(keyword, name)
                if score > 95:
                    match = True
                else:
                    match = False
                resource = {
                    "uri": uri,
                    "name": name,
                    "score": score,
                    "match": match
                }
                resources.append(resource)
            except AttributeError:
                pass
        sorted_resources = sorted(resources, key=itemgetter('score'), reverse=True)
        return sorted_resources[:10]
    except Exception as e:
        print("Error:", e)
        return None

# Functie om het Excel-bestand te lezen en een nieuw bestand te maken met gereconcilieerde URI's en trefwoorden
def reconcile_and_export_excel(input_file_path, output_file_path, column_name):
    workbook = openpyxl.load_workbook(input_file_path)
    sheet = workbook.active
    max_row = sheet.max_row

    column_index = None
    for cell in sheet[1]:
        if cell.value == column_name:
            column_index = cell.column
            break

    if column_index is None:
        print(f"Kolom '{column_name}' niet gevonden in het Excel-bestand.")
        return

    new_workbook = openpyxl.Workbook()
    new_sheet = new_workbook.active

    new_sheet.cell(row=1, column=1, value="Gereconcilieerde URI")
    new_sheet.cell(row=1, column=2, value=column_name)

    for row_num in range(2, max_row + 1):
        keyword = sheet.cell(row=row_num, column=column_index).value
        if keyword:
            reconciled_resources = reconcile_AAT_keyword(keyword)
            if reconciled_resources:
                for index, resource in enumerate(reconciled_resources, start=2):
                    new_sheet.cell(row=row_num, column=1, value=resource["uri"])
                    new_sheet.cell(row=row_num, column=index, value=resource["name"])

    new_workbook.save(output_file_path)

# Pad naar het invoer- en uitvoerbestand
input_excel_file_path = "/Users/patrickmout/Downloads/cht_procedureentechniek.xlsx"
output_excel_file_path = "/Users/patrickmout/Downloads/cht_procedureentechniek_match_AAT.xlsx"
# Kolomnaam waarin trefwoorden worden opgeslagen
column_name = "cht_concept"

# Reconcilieer het Excel-bestand en exporteer naar een nieuw bestand
reconcile_and_export_excel(input_excel_file_path, output_excel_file_path, column_name)
