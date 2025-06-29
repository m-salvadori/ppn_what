#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET
import argparse
import json
import csv

parser = argparse.ArgumentParser(description="Ce script nécessite un fichier d'entrée (liste de PPn). Indiquer les champs MARCXML souhaités")
parser.add_argument("file", help="Indiquer le chemin du fichier .txt. S'il se trouve dans le même dossier que le script, entrer simplement son nom.txt")
parser.add_argument("-z", "--zones", nargs="+", required=True, help="Liste des champs MARCXML à extraire, à précéder de -z (format: zone ou zone$sous-zone, par ex. 200$a 700$f)" \
"Attention, si aucune sous-zone n'est précisée, le script récupère l'ensemble de la zone")

args = parser.parse_args()

with open(args.file, 'r') as file:
    ppns = [line.rstrip() for line in file]

print(f"{len(ppns)} PPN concaténés, requête en route vers le sudoc...")

zone_filters = []
for z in args.zones:
    zone_filters.append(z) # Transforme en liste les zones données en argument

base_url = 'https://www.sudoc.fr/'
results = {}

for ppn in ppns:
    url = f'{base_url}{ppn}.xml'
    r = requests.get(url)
    if r.status_code == 200:
        try:
            root = ET.fromstring(r.content)
            record_data = {}
            
            for zone in zone_filters:
                if '$' in zone: # sous-champs MARC précédés de $
                    tag, subfield = zone.split('$', 1)
                    values = []
                    
                    # récupère le texte de ces sous-champs $
                    for datafield in root.findall(f".//datafield[@tag='{tag}']"):
                        for sf in datafield.findall(f"subfield[@code='{subfield}']"):
                            if sf.text:
                                values.append(sf.text)
                    
                    if values:
                        record_data[zone] = "; ".join(values)
                else:
                    tag = zone
                    datafields_content = []
                    
                    # récupère le texte des autres champs non précédés de $
                    for datafield in root.findall(f".//datafield[@tag='{tag}']"):
                        subfield_texts = []
                        for sf in datafield.findall("subfield"):
                            if sf.text:
                                subfield_texts.append(f"{sf.attrib['code']}: {sf.text}")
                        if subfield_texts:
                            datafields_content.append("; ".join(subfield_texts))
                    
                    if datafields_content:
                        record_data[zone] = " | ".join(datafields_content)
            
            results[ppn] = record_data
        except ET.ParseError:
            results[ppn] = {"erreur": "échec dans le parsing du XML"}
            print(f"Echec du parsing pour le PPN: {ppn}")
    else:
        results[ppn] = {"erreur": f"HTTP {r.status_code}"}
        print(f"échec de la requête pour le PPN: {ppn}")

print("Requête terminée")

for ppn, data in results.items():
    print(f"{ppn}:")
    for field, value in data.items(): # à développer
        print(f"  {field}: {value}")
    print()

usr_input = input("Requête terminée. Sauvegarder les résultats dans un fichier csv (oui/non) ? ")

if usr_input == "oui":
    csv_fields = ["PPN"] + zone_filters  # définit les champs de la 1ère ligne du CSV
    with open("csv_from_xml.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, delimiter=';')
        writer.writeheader()

        for PPN, data in results.items():
            row = {"PPN": PPN}
            for zone in zone_filters:
                row[zone] = data.get(zone, "")  # texte vide en cas de zone non trouvée
            writer.writerow(row)
    print("Fait")

