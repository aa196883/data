#!/usr/bin/env python3
import zipfile
import xml.etree.ElementTree as ET
import os
import sys

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
excel_file = os.path.join(script_dir, 'Skrid-Cadic.xlsx')
output_file = os.path.join(script_dir, 'cadic_metadata.tsv')

wb = zipfile.ZipFile(excel_file)
sheet = ET.fromstring(wb.read('xl/worksheets/sheet1.xml'))
strings = ET.fromstring(wb.read('xl/sharedStrings.xml'))
string_list = [s.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t').text for s in strings.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si')]

rows = []
for row in sheet.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
    row_data = []
    for cell in row.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
        cell_value = cell.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
        if cell_value is not None:
            if cell.get('t') == 's':
                row_data.append(string_list[int(cell_value.text)])
            else:
                row_data.append(cell_value.text)
        else:
            row_data.append('')
    rows.append(row_data)

headers = rows[0]
fichier_col = headers.index('SKRID-FICHIER')
lien_col = headers.index('LIEN')

print(f"Total rows: {len(rows)}")

# Generate TSV file instead of bash associative array (for compatibility with older bash)
with open(output_file, 'w') as f:
    for row in rows[1:]:
        if len(row) > max(fichier_col, lien_col) and row[fichier_col] and row[lien_col]:
            fichier = row[fichier_col]
            lien = row[lien_col]
            f.write(fichier + '\t' + lien + '\n')

print(f"Generated {output_file}")

