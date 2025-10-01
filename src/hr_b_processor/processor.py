import time
from pathlib import Path
import csv, json

# Etsi repo root ja sftp-kansio sen alta
BASE_DIR = Path(__file__).resolve().parents[2]  # mene src/hr_b_processor -> src -> root
SFTP_DIR = BASE_DIR / "sftp"
SFTP_DIR.mkdir(exist_ok=True)

print("HR B processor watching:", SFTP_DIR)

def normalize_key(row, *names):
    for n in names:
        if n in row:
            return row[n]
        if n.lower() in row:
            return row[n.lower()]
        if n.upper() in row:
            return row[n.upper()]
    return None

def process_once():
    for p in list(SFTP_DIR.glob("*.csv")):
        print("Found csv:", p.name)
        results = []
        with p.open(newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                idv = normalize_key(row, 'id', 'Id', 'ID')
                if idv is None:
                    continue
                results.append({"id": int(idv), "status": "synced"})
        resp = {"results": results}
        respname = p.name + ".response.json"
        with (SFTP_DIR / respname).open('w', encoding='utf-8') as rf:
            json.dump(resp, rf)
        print("Wrote response:", respname)
        p.unlink() 

if __name__ == "__main__":
    try:
        while True:
            process_once()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped")
