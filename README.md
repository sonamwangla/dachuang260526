# Signal Visualization Project

This repository contains a Flask backend and a Vue/Vite frontend for signal visualization and optimization.

## Backend

```powershell
cd SignalBackend
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\python init_db.py
.\venv\Scripts\python inject_professional_data.py
.\venv\Scripts\python app.py
```

## Frontend

```powershell
cd SignalVisualization
npm install
npm run dev
```

Generated folders, logs, virtual environments, build output, and local SQLite databases are intentionally ignored by Git.
