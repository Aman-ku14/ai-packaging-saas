# AI Packaging Recommendation SaaS

An AI-powered SaaS for packaging recommendations.

## Tech Stack
- **Backend**: Python + FastAPI
- **Frontend**: Next.js (planned)
- **AI**: Integrated into backend (MVP)

## Getting Started

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Project Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── api/v1/          # API routes
│   ├── ai/              # AI recommendation engine
│   ├── core/            # Config & settings
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   └── services/        # Business logic
└── tests/               # Test suite
```
