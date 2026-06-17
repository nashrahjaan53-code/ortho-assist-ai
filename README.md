# OrthoAssist AI: Musculoskeletal Vision and Prescription Safety Validator

OrthoAssist AI is a clinical decision-support prototype designed for orthopedic clinicians and radiologists. The application combines a computer vision pipeline with a multimodal Large Language Model (LLM) to extract visual diagnostic patterns from uploaded X-ray images, cross-reference them with a patient's historical text logs, and run an automated safety evaluation against prescribed medications to detect wrong dosages or clinical contraindications.

## System Architecture

The application utilizes a decoupled client-server architecture to separate user interaction from heavy inference workloads:

1. Frontend UI (Streamlit): Captures user inputs including medical radiograph uploads, localized symptoms, and proposed drug prescriptions. It transmits data via multi-part form payloads.
2. Backend API (FastAPI): Exposes asynchronous endpoints to receive case data. It processes image files through a localized PyTorch Vision Transformer pipeline to parse structure, converts images to base64 encoding strings, and handles connection states to cloud inference engines.
3. Intelligence Layer (Google Gemini 2.5 Flash): Interprets the combined visual pixel data and text history simultaneously under a strict system prompt to output zero-shot medical analysis reports.

## Project Structure

```text
ortho-assist-ai/
│
├── backend/
│   ├── __init__.py
│   ├── main.py            # FastAPI application routing and endpoints
│   ├── model_loader.py    # PyTorch Vision Transformer configuration
│   └── llm_service.py     # Gemini API integration and strict prompt layering
│
├── frontend/
│   └── app.py             # Streamlit web dashboard interface
│
├── .env                   # Local environment configuration keys (Git ignored)
├── .gitignore             # Exclusion rules for local models, caches, and secrets
├── README.md              # Project documentation
└── requirements.txt       # Frozen application dependencies