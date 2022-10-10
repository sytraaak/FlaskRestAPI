def writer_to_file(date: str, data: list):
    global data_to_file
    if os.path.exists(f"scrapped_data/{date}.xls") != True:
        with open(f"scrapped_data/{date}.xls", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, dialect="excel")
            header = ["Datum vzniku záznamu", "ORIGIN", "Zadaný odlet", "DESTINATION", "Zadaný návrat",
                      "Student Agency Cena", "Student Agency TF", "Dopravce", "Datum odletu", "Datum návratu",
                      "Letuska Cena", "Letuška TF", "Dopravce", "Datum odletu", "Datum návratu",
                      "Pelikan Cena", "Pelikan TF", "Dopravce", "Datum odletu", "Datum návratu",
                      "Fractal TF", "Fractal TF", "Dopravce", "Datum odletu", "Datum návratu"]
            writer.writerow(header)

    with open(f"scrapped_data/{date}.xls", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, dialect="excel")
        writer.writerow(data)
        data_to_file = []