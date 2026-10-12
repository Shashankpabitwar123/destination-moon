"""Check catalogue facts against the data exported from the final workbook."""
from pathlib import Path
import csv, json
from collections import Counter
root = Path(__file__).resolve().parents[1]
catalogue = json.loads((root / 'data/catalog.json').read_text())
with (root / 'data/missions.csv').open() as f:
    exported = list(csv.DictReader(f))
assert len(catalogue) == len(exported) == 116
assert len({r['ID'] for r in exported}) == 116
assert Counter(r['Status'] for r in exported) == {'Successful': 64, 'Failed': 43, 'Partial': 9}
by_id = {r['ID']: r for r in exported}
for row in catalogue:
    for field in ['Name', 'Country', 'Status', 'MissionType', 'Purpose', 'Result', 'ReadURL']:
        assert str(row[field]) == by_id[row['ID']][field], (row['ID'], field)
    assert row['ReadURL'].startswith('https://')
print('PASS: 116 unique missions, outcome totals, source links and core facts match the final workbook export.')
