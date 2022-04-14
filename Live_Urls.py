import csv, io, requests

def urlsToMigrate(google_sheet_id):
    pages = []
    url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(google_sheet_id)
    #urllib3.disable_warnings()
    r = requests.get(url,verify=False)
    sio = io.StringIO(r.text, newline=None)
    reader = csv.reader(sio, dialect=csv.excel)

    for row in reader:
        pages.append(row[0])

    return pages
