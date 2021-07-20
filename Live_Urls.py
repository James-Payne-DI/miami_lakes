import csv, requests, io


def urlsToMigrate(google_sheet_id):
    pages = []
    url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(google_sheet_id)
    r = requests.get(url)
    sio = io.StringIO(r.text, newline=None)
    reader = csv.reader(sio, dialect=csv.excel)

    for row in reader:
        pages.append(row[0])

    return pages
