# SVI4Waste

Detect and analyse **fly-tipping / street waste** in Nairobi using **Street View Imagery (SVI)**. The project combines custom **YOLO** object detection, optional **Qwen-VL** vision-language filtering, and **spatial statistics** (clustering, point-process models) with a focus on **informal settlements**.

> **Scope:** ~126k panoramas / ~505k directional images → ~3,400 confirmed waste points after cleaning and validation.

---

## What this repo contains

| Tracked in Git | Kept locally only |
|---|---|
| Jupyter notebooks (`.ipynb`) | `Data/` — training images, inference CSVs |
| Python / R scripts (`.py`, `.R`, `.Rmd`) | `Del/` — archived experiments |
| Small reference CSVs (`Code/Small_data/`) | Model weights (`*.pt`) |
| MMDetection configs (`Code/RS/garbage_detection/`) | GeoTIFFs, large GeoJSON, HTML reports |
| | Google Drive mirror (see [Data](#data-not-in-git)) |

**Rule of thumb:** commit **code and small config files**; keep **data, models, and generated outputs** on disk or Google Drive.

---

## Repository layout

```
SVI_Waste/
├── Prepare/          # Build YOLO training datasets
├── Predict/          # Batch inference scripts (YOLO, Qwen-VL)
├── Code/
│   ├── SVI/          # Main analysis pipeline (see below)
│   │   ├── Informal_settlements/   # HDBSCAN / DBSCAN clustering near slums
│   │   └── Stats/                  # R point-process models (PPM, K-function)
│   ├── IDEAMaps/     # Grid maps & flood–waste overlap
│   ├── RS/           # Remote-sensing garbage detection (MMDetection fork)
│   └── Small_data/   # Small boundary / location reference tables
├── Data/             # NOT in Git — processed CSVs & YOLO training sets
└── Del/              # NOT in Git — superseded notebooks & old model weights
```

---

## Analysis pipeline

The typical workflow runs in this order:

```
1. Prepare/              Label & split training data
       ↓
2. Train YOLO            Custom waste detector (Ultralytics)
       ↓
3. Predict/              Score SVI image lists → CSV outputs
       ↓
4. SVI_1CleanImage       Harmonise Faith / ZWL / GSVI metadata
       ↓
5. SVI_2SelectImage      Filter positives; merge YOLO + Qwen outputs
       ↓
6. SVI_Val               Validation metrics & confusion matrix
       ↓
7. Spatial analysis      PPP, HDBSCAN, sub-county stats
       ↓
8. Flood_Waste           Cross-tab with flood exposure rasters
```

### Notebook guide

#### Data preparation & inference

| File | Purpose |
|------|---------|
| `Prepare/BackgroundTxt.py` | Create empty YOLO label files for background images |
| `Prepare/SplitDataToTVP.py` | Random train / val / test split lists |
| `Prepare/DataCleanStepOne.py` | Pre-filter with Detectron2 panoptic (dirt, gravel) |
| `Prepare/DataCleanStepTwoByWaste27.py` | Pre-label with early YOLO model (`waste27.pt`) |
| `Predict/PredictByCustomModel.py` | Batch YOLO inference on CSV image paths |
| `Predict/PredictByQwen.py` | Qwen-VL secondary filter ("垃圾" detection) |
| `Code/Background.ipynb` | Notebook version of background-label creation |

#### SVI cleaning & validation (`Code/SVI/`)

| File | Purpose |
|------|---------|
| `SVI_1CleanImage.ipynb` | Unify multi-source SVI metadata; deduplicate panos |
| `SVI_2SelectImage.ipynb` | Post-inference curation; copy positives to `Selected/` |
| `SVI_Val.ipynb` | YOLO validation run; confusion matrix |
| `SV_YoloResult.ipynb` | Plot training loss curves |
| `SVI_Qwen_cyb.ipynb` | Qwen-VL experiments |
| `SVI_Social_economic.ipynb` | Socio-economic covariate exploration |

#### Spatial analysis

| File | Purpose |
|------|---------|
| `SVI_PPP_SubCounty.ipynb` | Sub-county KDE, nearest-neighbour ratio, DBSCAN, Gi* hotspots |
| `Informal_settlements/SVI_HDBSCAN_only.ipynb` | HDBSCAN clustering vs slum boundaries |
| `Informal_settlements/SVI_DBSCAN_both.ipynb` | DBSCAN sensitivity comparison |
| `Informal_settlements/SVI_BufferAnalysis.ipynb` | Buffer analysis around settlements |
| `Informal_settlements/SVI_distance_use.ipynb` | Distance-to-slum metrics |
| `Stats/Stats_ppm_pop.Rmd` | Inhomogeneous K-function & PPM vs WorldPop |
| `Stats/Stats_ppm_pop_IS.Rmd` | PPM focused on informal settlements |
| `Stats/SVI_PPP_Stats_USE.ipynb` | Python-side PPP stats companion |
| `figure.R` | Shared R plotting helpers |

#### Mapping & remote sensing

| File | Purpose |
|------|---------|
| `IDEAMaps/SVI_IDEAMaps.ipynb` | IDEAMaps grid visualisation |
| `IDEAMaps/Flood_Waste.ipynb` | Waste detections × flood raster overlap |
| `ForQGIS.ipynb` | Export layers for QGIS |
| `RS/garbage_detection/` | Aerial garbage-dump detection (BCA-Net / MMDetection) |
| `Small_data/Local_authorities.ipynb` | Local authority boundary prep |
| `Small_data/Del_Slum_boundary.ipynb` | Slum boundary processing |

---

## Data (not in Git)

Large files live **outside the repository**. Update paths in notebooks/scripts to match your machine.

### Primary local data root

```
~/Downloads/PhD_UCL/Data/
├── Waste/img/                           # SVI CSVs & source images
├── Waste/Angela/slumaps_nairobi_sett/   # Slum shapefiles
├── Waste/QGIS/                          # Sub-county boundaries
├── GoogleStreetView/Train/              # YOLO training images
├── Mapillary/Self_GeoReferenced/
├── Meta/                                # Facebook crisis population data
└── RS/Pop_density/                      # WorldPop rasters
```

### In-repo data (local only, gitignored)

```
Data/
├── Train/          # YOLO snapshots (0113_135, 0116_132, 0118_198)
└── Output/
    ├── GSVI/       # Google Street View processed CSVs
    ├── Self/       # Self-collected Mapillary CSVs
    └── Combined_uni.csv
```

### Google Drive mirror

Large CSVs are also stored at:

```
/content/drive/Shareddrives/Wenlan/SVI_Waste/
```

### Dataset inventory (counts)

| Dataset | Records | Notes |
|---------|---------|-------|
| GSVI original | 113,341 | Google Street View panoramas |
| GSVI long format | 453,364 | 4 directions per pano |
| Self-collected | 2,328 | Mapillary, NaN-cleaned |
| Combined unanalysed | 455,692 | GSVI + self |
| YOLO training set | 135 images | `Waste4Yolo` |
| Confirmed waste (Nairobi) | ~3,385 | After cleaning & validation |

### Model weights

Custom YOLO weights (`waste27.pt`, `waste47.pt`, `waste_0315.pt`) are archived in `Del/Del_Yolo8/`. Base Ultralytics checkpoints (`yolov8n.pt`, etc.) can be downloaded from [Ultralytics](https://github.com/ultralytics/ultralytics).

---

## Setup

### Python (YOLO pipeline)

```bash
conda create -n svi-waste python=3.10
conda activate svi-waste
pip install -r requirements.txt
```

Key packages: `ultralytics`, `pandas`, `geopandas`, `matplotlib`, `scikit-learn`, `hdbscan`.

For Qwen-VL inference (`Predict/PredictByQwen.py`), install separately:

```bash
pip install transformers torch
```

For the remote-sensing track (`Code/RS/garbage_detection/`), follow the [MMDetection install guide](https://github.com/open-mmlab/mmdetection).

### R (spatial statistics)

```r
install.packages(c("spatstat", "sf", "ggplot2", "raster"))
```

Knit `Code/SVI/Stats/*.Rmd` to reproduce point-process analyses.

---

## Keeping the repo small

Before committing, check that you are not adding large files:

```bash
# See what would be committed
git status

# Find files over 1 MB in the staging area
git diff --cached --name-only | xargs -I{} du -h "{}" 2>/dev/null | sort -hr | head

# Clear embedded notebook outputs (recommended for notebooks > 1 MB)
pip install nbstripout
find Code -name "*.ipynb" -exec nbstripout {} \;
```

**Never commit:** `Data/`, `Del/`, `*.pt`, GeoTIFFs, generated HTML/PNG reports, zip archives.

---

## Archive folder (`Del/`)

Superseded work is kept locally under `Del/` but excluded from Git:

- `Del_Yolo8/` — old YOLO model weights
- `Del_Analysis/` — moved from `Analysis/`
- `del_Facebook/` — Meta population displacement during flood crisis
- `Detectron2/` — early Detectron2 waste experiments
- `Del——SVI/` — HDBSCAN figure exports

---

## Known confusing factors in detection

Leaves, sparse grass, informal market stalls, wet/dry dirt, gravel, and haystacks can trigger false positives. The Qwen-VL filter and manual review in `SVI_2SelectImage.ipynb` address this.

---

## License

See [LICENSE](LICENSE).
