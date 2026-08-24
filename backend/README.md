# API

Instalação local:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints do MVP:

- `GET /health`
- `POST /api/v1/readings`
- `GET /api/v1/readings?limit=100`
- `GET /api/v1/latest`

Antes do uso em campo, substituir o armazenamento em memória por PostgreSQL/TimescaleDB e implementar autenticação do dispositivo.
