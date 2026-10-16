
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: bash $0 <csv-url>" >&2
  exit 2
fi

csv_url="$1"

command -v curl >/dev/null 2>&1 || {
  echo "Error: curl is required." >&2
  exit 1
}

command -v python3 >/dev/null 2>&1 || {
  echo "Error: python3 is required." >&2
  exit 1
}

tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT

curl --fail --location --silent --show-error \
  "$csv_url" --output "$tmp_file"

python3 - "$tmp_file" <<'PY'
import csv
import re
import sys

path = sys.argv[1]

def year_key(row):
    raw = (row.get("Founded") or "").strip()
    match = re.match(r"^(\d{4})", raw)

    if match:
        return (0, int(match.group(1)))

    return (1, 9999)

with open(path, newline="", encoding="utf-8-sig") as handle:
    reader = csv.DictReader(handle)

    required = {
        "Security",
        "Headquarters Location",
        "Founded",
    }

    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        print(
            "CSV is missing expected columns. Found: "
            + ", ".join(reader.fieldnames or []),
            file=sys.stderr,
        )
        sys.exit(1)

    rows = list(reader)

rows.sort(key=year_key)

writer = csv.writer(sys.stdout)
writer.writerow(["Company name", "Location", "Founding year"])

for row in rows:
    writer.writerow([
        (row.get("Security") or "").strip(),
        (row.get("Headquarters Location") or "").strip(),
        (row.get("Founded") or "").strip(),
    ])
PY
