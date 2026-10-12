# Open and explore

The easiest way to explore is the live Tableau Public link in the main README.

To edit locally, download `tableau/Moon_missions.twbx` and open it in Tableau Desktop or Tableau Public Desktop. The final file was saved with Tableau 2026.2.1. Its extract and image assets are included; no separate database is required. Internet access is needed for external source links.

The final workbook was tested and published by Shashank. The repository preserves the final Downloads file byte for byte. The preview is an export from the published view.

## Prepare the catalogue

From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/prepare_catalog.py
python scripts/check_data.py
```

`prepare_catalog.py` reads the included NASA table and chronology snapshots. It writes `data/catalog.json`, `data/corrections.json` and `data/exclusions.json`. The fetched index retains URL/status evidence used by the original preparation; running this script does not fetch new mission information.

`data/missions.csv` is the data exported from the final workbook. The checks compare core mission facts with the prepared catalogue. This preparation command does not regenerate the final Tableau layout or overwrite the workbook. Edit the final layout in Tableau.

## Repository folders

- `tableau/`: final packaged workbook.
- `data/`: exported mission data, catalogue and documented decisions.
- `source/`: structured snapshots used by the preparation script.
- `scripts/`: preparation and data checks.
- `docs/`: dashboard image and explanations.
