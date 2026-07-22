<div align="center">

# 🦴 OrthoAssist AI

### AI-Powered Musculoskeletal X-Ray Analysis & Prescription Safety Validation

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![PyTorch](https://img.shields.io/badge/PyTorch-Vision-red?style=for-the-badge&logo=pytorch)
![Google Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)

A clinical decision-support prototype that combines **Computer Vision**, **Large Language Models**, and **Medical Safety Validation** to analyze orthopedic X-rays, interpret patient history, and evaluate prescription safety in a unified workflow.

</div>
---

# 🖥️ Application Preview

The screenshot below showcases the Streamlit interface of **OrthoAssist AI**, where clinicians can upload musculoskeletal X-rays, provide patient history, enter prescribed medications, and receive an AI-assisted diagnostic and prescription safety assessment.

<p align="center">
  <img src="./orthoassist-dashboard.png" alt="OrthoAssist AI Dashboard" width="90%">
</p>

---


---

# 📌 Project Overview

Healthcare professionals often need to review multiple sources of clinical information before making treatment decisions. Radiographs, patient symptoms, previous medical history, and medication plans must all be considered together.

**OrthoAssist AI** streamlines this workflow by integrating image understanding with multimodal AI reasoning. The system analyzes uploaded X-ray images, incorporates patient history, and performs prescription safety checks to generate an intelligent clinical assessment.

---

# ✨ Features

- 🦴 AI-powered X-ray interpretation
- 🤖 Vision Transformer image analysis
- 💬 Multimodal Gemini reasoning
- 📋 Patient history integration
- 💊 Prescription safety validation
- ⚠️ Dosage and contraindication detection
- ⚡ FastAPI backend APIs
- 🌐 Interactive Streamlit interface

---

# 🧠 AI Components

- **Vision Transformer (PyTorch)** – Extracts musculoskeletal patterns from radiographs.
- **Google Gemini 2.5 Flash** – Performs multimodal clinical reasoning using images and text.
- **FastAPI** – Handles asynchronous backend inference.
- **Streamlit** – Provides an intuitive web-based interface.

---

# ⚙️ System Architecture

```text
                          🩻 Patient X-Ray
                                 │
                                 ▼
                 ┌─────────────────────────┐
                 │ Streamlit Web Interface │
                 └─────────────────────────┘
                                 │
                                 ▼
                  ┌────────────────────────┐
                  │ FastAPI Backend Server │
                  └────────────────────────┘
                                 │
             ┌───────────────────┴───────────────────┐
             ▼                                       ▼
┌────────────────────────┐             ┌────────────────────────┐
│ Vision Transformer AI  │             │ Patient History Parser │
└────────────────────────┘             └────────────────────────┘
             │                                       │
             └───────────────────┬───────────────────┘
                                 ▼
                  ┌────────────────────────┐
                  │ Google Gemini 2.5 AI   │
                  └────────────────────────┘
                                 │
                                 ▼
          ┌─────────────────────────────────────────┐
          │ Diagnosis + Medication Safety Report    │
          └─────────────────────────────────────────┘
```

---

# 📂 Project Structure

```text
ortho-assist-ai/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── model_loader.py
│   └── llm_service.py
│
├── frontend/
│   └── app.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd ortho-assist-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file and add your API credentials.

```text
GOOGLE_API_KEY=your_api_key_here
```

### 4. Start Backend

```bash
uvicorn backend.main:app --reload
```

### 5. Launch Frontend

```bash
streamlit run frontend/app.py
```

---

# 🔬 Workflow

1. Upload an orthopedic X-ray.
2. Enter patient symptoms and medical history.
3. Provide proposed medications.
4. Vision Transformer extracts image features.
5. Gemini analyzes visual and textual context.
6. Prescription safety is evaluated.
7. A complete AI-generated clinical report is returned.

---

# 📊 Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Computer Vision | PyTorch Vision Transformer |
| AI Reasoning | Google Gemini 2.5 Flash |
| API Communication | REST APIs |
| Environment | python-dotenv |

---

# 🎯 Potential Applications

- Orthopedic clinics
- Radiology departments
- Medical education
- Clinical decision support
- Prescription validation
- Healthcare AI research

---

# 📈 Future Improvements

- DICOM image support
- PACS integration
- Multi-disease orthopedic detection
- Explainable AI heatmaps
- Electronic Health Record (EHR) integration
- PDF clinical report generation
- Authentication and patient management
- Docker deployment
- Cloud inference support

---

# 📜 License

This repository is intended for educational and research purposes only and should **not** be used as a replacement for professional medical diagnosis or treatment.
