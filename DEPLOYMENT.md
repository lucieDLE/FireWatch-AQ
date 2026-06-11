# Deployment Runbook — FireWatch-AQ on Hugging Face Spaces

How this dashboard was deployed live at:
https://huggingface.co/spaces/LLD9/firewatch-aq

---

## What the app needs at runtime (only ~58 MB)
- `data/processed/input_report_2025.csv`
- `data/processed/fire_archive_pixels_2025_cleaned.csv`
- `data/raw/annual_conc_by_monitor_2025.csv`
- `data/raw/california-counties.geojson` (auto-downloads on first boot if missing)
The 777 MB perimeter GeoJSON and 85 MB wind file are preprocessing-only — NOT needed.

---

## One-time setup files (committed at repo root)

**1. `requirements.txt`** — pip equivalent of environment.yml (+ gunicorn). geopandas/shapely.

**2. `Dockerfile`** — HF serves on port 7860; run gunicorn against the exposed Flask server (`server = app.server` in app/app.py):
```dockerfile
FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["gunicorn", "app:server", "--chdir", "app", "-b", "0.0.0.0:7860", "--timeout", "120"]
```

**3. `.dockerignore`** — keep the 1.1 GB of raw/unused data out of the image, except the one raw file the app reads.

**4. `README.md` YAML header** — HF reads the Space config from the top of README:
```yaml
---
title: FireWatch AQ
emoji: 🔥
colorFrom: red
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
tags: [dash, plotly, air-quality, wildfire, california, geospatial, dashboard]
---
```

---

## Git LFS
HF rejects any file >10 MB that isn't tracked by Git LFS, and it scans the ENTIRE history,
not just current files. Two large CSVs and two notebooks lived in old commits as plain blobs.

Convert them across ALL history (note: plain `git lfs migrate` only touches commits not yet on
the remote — must use `--everything`). Working tree must be clean first (stash if needed):
```bash
git lfs migrate import --everything \
  --include="data/processed/input_report_2025.csv,data/raw/annual_conc_by_monitor_2025.csv,notebooks/*.ipynb"
```
Verify with `git lfs ls-files`. Check nothing >10 MB non-LFS remains:
```bash
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1=="blob" && $3>10485760 {print $3/1048576" MB  "$4}' | sort -u
```

## Removing an unused large file from history (e.g. animation_fire.mp4)
If a big file isn't needed at all, purge it instead of LFS-ing it:
```bash
pip install git-filter-repo
git filter-repo --force --invert-paths --path animation_fire.mp4 --path assets/animation_fire.mp4
# filter-repo strips remotes — re-add them:
git remote add space  https://huggingface.co/spaces/<space_name>/firewatch-aq
```
(Note: a file can exist at multiple paths across history — list every path.)

---

## Create the Space & push
1. huggingface.co → New Space → SDK **Docker** → Public.
2. Settings → Access Tokens → create a **Write** token (used as the git password).
3. Add the remote and push (history was rewritten, so `--force`):
```bash
git remote add space https://huggingface.co/spaces/<space_name>/firewatch-aq
git push space main --force          # username = HF handle, password = write token
git push origin main --force         # keep GitHub in sync
```
4. Watch the Space **Logs** tab; when the badge shows **Running**, open the URL and test all tabs.

---

## Updating the app later
Just commit changes and push — the Space rebuilds automatically:
```bash
git push space main
```