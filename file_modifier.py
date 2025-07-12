import csv

def get_file(csv_file, fieldnames, state_to_scrape):
    filtered_rows = []
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['State'] not in state_to_scrape:
                    filtered_rows.append(row)
    except FileNotFoundError:
        pass  

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)
    return csv_file

def write_file(csv_file,fieldnames, data):
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for row in data:
            writer.writerow(row)