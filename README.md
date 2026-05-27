# Data Analyzer Toolbox

An interactive Plotly Dash web application for end-to-end data analysis: exploration, cleaning, feature engineering, model training, explainability, what-if simulation, and artifact export.

## Problem

Specialists working with tabular data often focus primarily on improving model accuracy, while the impact of different data conditions and feature changes on model behavior is often overlooked. Questions such as *“How would the model perform if it were trained on a different data distribution?”* or *“How would specific feature changes affect predictions and evaluation metrics?”* are usually not explored in a systematic and interpretable way within traditional machine learning workflows.

Data Analyzer Toolbox was developed to address this limitation by integrating data exploration, preprocessing, model training, explainability analysis, and counterfactual scenario simulation into a single interactive Plotly Dash application. The platform enables users to analyze how feature-level changes influence model predictions and performance metrics, supporting a more interpretable, scenario-driven, and analysis-oriented machine learning workflow.

## Data

The application accepts two ingestion modes:

1. **Built-in Sample Datasets** - registered in `configuration/assets/datasets.json`. The default registry currently includes:
   - Chicago Traffic Crashes - classification of crash severity from weather, lighting, road, and time features.
   - Auto MPG - regression for vehicle fuel efficiency (miles-per-gallon).
   - AI4I 2020 Predictive Maintenance - binary classification of machine component failure.
2. **Arbitrary URL** - fetches a CSV from a user-supplied HTTP(S) endpoint.

To ensure smooth interaction and responsive visualization performance inside the Dash interface, datasets containing more than 2,000 rows are automatically downsampled to a maximum of 2,000 samples using random_state=42. 

## Methods

The pipeline is split across seven tabs, each backed by a dedicated component (`core/view/components/tabs/`) and a callback module (`core/callbacks/`):

| Tab | Purpose |
| --- | --- |
| **Data Explorer** | Dataset overview, schema, missing-value summary, EDA plots (distributions, correlations, scatter, box). |
| **Data Processing** | Null handling, deduplication, column rename, column drop, dtype coercion. Mutations write back to the shared store so other tabs refresh. |
| **Feature Engineering** | Encoding (one-hot, ordinal), scaling, derived features. |
| **Train-Evaluate Model** | Model selection from `configuration/assets/models.json` (Logistic/Ridge baselines, Random Forest, XGBoost - both classification and regression). Hyperparameters are exposed as UI fields and merged with sensible defaults. Train/test split, fit, and metrics (accuracy / F1 / ROC-AUC for classification; RMSE / MAE / R² for regression). |
| **Explainability** | SHAP-based global and local explanations. |
| **What-If Simulation** | Interactive prediction: edit feature values and observe how the trained model's output changes. |
| **Download** | Export the processed dataset and trained-model artifacts. |

## Capabilities

Once launched the user can, end-to-end:

- Load a CSV (Sample, or URL) and immediately see schema and missingness diagnostics.
- Clean and reshape the data with point-and-click operations that propagate to every downstream tab.
- Train a baseline, tree, or gradient-boosted model with adjustable hyperparameters and inspect classification or regression metrics on a held-out split.
- Generate SHAP explanations for the trained model and probe its behavior with what-if perturbations.
- Export the cleaned dataset and model artifacts for downstream use.

## Requirements

- Python **3.10 or 3.11** (recommended)
- Tested on Ubuntu 22.04 with Python 3.11
- `pip` and `venv` available on the path.
- Network access needed (to fetch pip wheels and, if a sample dataset is selected).

Pinned runtime dependencies live in `requirements-dev.txt` (Dash 2.18, dash-bootstrap-components 1.6, Plotly 5.22, pandas 2.2, scikit-learn 1.5, XGBoost 1.7, SHAP 0.51, python-dotenv 1.0, requests 2.32, numpy).

## Setup

After cloning, run the bundled setup script from the repo root:

```bash
git clone <repo-url>
cd data-analyzer-toolbox
./setup.sh
```

`setup.sh` performs every step needed to go from a fresh clone to a runnable app:

1. Creates a virtual environment named `venv/` (skips if it already exists).
2. Activates the environment.
3. Upgrades `pip` and installs everything in `requirements-dev.txt`.
4. Generates a `.env` file at the repo root with sensible defaults:
5. Makes `run.sh` executable.

If `setup.sh` is not marked executable yet, run `chmod +x setup.sh` first.

## Running the app

```bash
./run.sh
```

`run.sh` activates `venv/` and launches `python3 main.py`. Once the Dash server reports it is listening, open:

```
http://localhost:8050
```

To stop the server, press `Ctrl+C` in the terminal.

If `venv/` is already active in your shell, you can skip the script and run `python3 main.py` directly.

## Running with Docker

A `Dockerfile` is provided to run the application in a containerized environment without installing Python or dependencies locally. This is the recommended setup for a clean and reproducible installation.

Requirements: a working Docker installation (Docker Desktop on macOS/Windows, or Docker Engine on Linux).

**1. Build the Image** (from the repo root):

```bash
docker build -t data-analyzer-toolbox .
```

This single command performs every step needed to go from a fresh clone to a runnable image - it installs the pinned dependencies from `requirements-dev.txt` and copies the application source. No `.env` file or manual setup is required; the image bakes in sensible defaults (`HOST=0.0.0.0`, `PORT=8050`, and the bundled dataset/model registry paths).

**2. Run the Container**:

```bash
docker run --rm -p 8050:8050 data-analyzer-toolbox
```

Then open <http://localhost:8050> in your browser. Press `Ctrl+C` to stop the container.

**Overriding Settings** - custom registries:

```bash
docker run --rm -p 9000:9000 -e PORT=9000 data-analyzer-toolbox
```

You can also mount a local `.env` file instead:

```bash
docker run --rm -p 8050:8050 --env-file .env data-analyzer-toolbox
```

### Environment variables

The four variables in `.env` are required at startup - `Environment._load_required_env_variables` raises if any are missing:

| Variable | Purpose |
| --- | --- |
| `HOST` | Interface the Dash server binds to. |
| `PORT` | Port the Dash server listens on. |
| `DATASET_URL` | Path to the JSON registry of sample datasets. |
| `MODELS_URL` | Path to the JSON registry of model families and hyperparameter fields. |

Edit `.env` to bind on a different interface/port (e.g., `HOST="0.0.0.0"` for LAN access) or to point at a custom dataset/model registry.

## Project Architecture

```
.
├── main.py                          # entry point - wires Configuration + Toolbox + callbacks
├── setup.sh                         # one-shot installer (venv, deps, .env)
├── run.sh                           # activates venv and runs main.py
├── requirements-dev.txt             # pinned dependencies
├── configuration/
│   ├── configuration.py             # tab + asset registry
│   ├── environment.py               # .env loader (singleton)
│   └── assets/
│       ├── datasets.json            # sample dataset registry
│       └── models.json              # model families + hyperparameter fields
├── core/
│   ├── api/dataset.py               # dataset api fethcing
│   ├── callbacks/                   # per-tab callback modules
│   └── view/
│       ├── data_analyzer_toolbox.py # Dash app + layout
│       └── components/
│           ├── header.py 
|           ├── center.py 
|           ├── footer.py
│           └── tabs/                # one file per tab
├── utils/                           # dataframe helpers, metrics, figures, registry
```
