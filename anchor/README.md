# Anchor

**A companion that holds memory for people who are losing theirs.**

Patient-facing Alzheimer's/dementia companion built for the Global AI HackTour London 2026 by team 404-Team-Not-Found.

## Setup

```bash
cd anchor
cp .env.example .env   # Add your API keys
uv sync                # Install dependencies
uv run uvicorn backend.main:app --reload --port 8000
```

Open http://localhost:8000 for the patient interface, http://localhost:8000/carer for the carer notification view.

## Reset between demos

```bash
curl -X POST http://localhost:8000/api/reset
```

## Privacy disclaimer

HACKATHON PROTOTYPE — NOT FOR USE WITH REAL PATIENT DATA. Margaret is a fictional persona. In production, this system handles UK GDPR Article 9 special-category health data, requiring explicit consent, encryption at rest and in transit, UK ICO registration, and data-processing agreements with LLM providers.

*Anchor doesn't help Margaret remember. It remembers for her, so she can keep being herself.*