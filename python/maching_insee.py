import csv

a21 = {
    "TOT": "Ensemble",
    "B": "Industries extractives",
    "C": "Industrie manufacturière",
    "D": "Production et distribution d'électricité, de gaz, de vapeur et d'air conditionné",
    "E": "Production et distribution d'eau, assainissement, gestion des déchets et dépollution",
    "F": "Construction",
    "G": "Commerce, réparation d'automobiles et de motocycles",
    "H": "Transports et entreposage",
    "I": "Hébergement et restauration",
    "J": "Information et communication",
    "K": "Activités financières et d'assurance",
    "L": "Activités immobilières",
    "M": "Activités spécialisées, scientifiques et techniques",
    "N": "Activités de services administratifs et de soutien",
    "P": "Enseignement",
    "Q": "Santé humaine et action sociale",
    "R": "Arts, spectacles et activités récréatives",
    "S": "Autres activités de services"
}

regions = {
    "FR": "France entière",
    "01": "Guadeloupe",
    "02": "Martinique",
    "03": "Guyane",
    "04": "La Réunion",
    "06": "Mayotte",
    "11": "Île-de-France",
    "24": "Centre-Val de Loire",
    "27": "Bourgogne-Franche-Comté",
    "28": "Normandie",
    "32": "Hauts-de-France",
    "44": "Grand Est",
    "52": "Pays de la Loire",
    "53": "Bretagne",
    "75": "Nouvelle-Aquitaine",
    "76": "Occitanie",
    "84": "Auvergne-Rhône-Alpes",
    "93": "Provence-Alpes-Côte d'Azur",
    "94": "Corse"
}

with open("a21_codes.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(["A21", "sector_name"])
    for k, v in a21.items():
        w.writerow([k, v])

with open("regions_codes.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(["REG", "Region"])
    for k, v in regions.items():
        w.writerow([k, v])

print("Fichiers a21_codes.csv et regions_codes.csv créés.")
