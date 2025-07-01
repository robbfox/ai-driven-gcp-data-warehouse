import os
import csv

def get_csv_headers(directory):
    """
    This function iterates through all the CSV files in a directory,
    extracts their headers, and stores them in a new CSV file.
    """
    with open('schemas.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['file_name', 'headers'])
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f_in:
                    reader = csv.reader(f_in)
                    try:
                        headers = next(reader)
                        writer.writerow([filename, headers])
                    except StopIteration:
                        writer.writerow([filename, []])

if __name__ == "__main__":
    get_csv_headers(r"C:\Users\robbf\Documents\ai-driven-gcp-data-warehouse\data")