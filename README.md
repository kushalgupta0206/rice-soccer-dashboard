# Rice Soccer Dashboard

A Shiny for Python dashboard for analyzing Rice women's soccer team, player, opponent, and comparison data using Wyscout Event Level Data.

## Setup

1. Create and activate a virtual environment (recommended).

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

From the project root:

```bash
python -m shiny run app.py
```

Shiny will print a local URL (for example `http://127.0.0.1:8000`). Open that address in your browser to use the dashboard.

To automatically reload when you change code:

```bash
python -m shiny run --reload app.py
```
