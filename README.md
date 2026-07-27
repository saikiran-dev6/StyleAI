# StyleAI - AI-Powered Fashion Styling Advisor

StyleAI is an intelligent, privacy-first personal fashion styling platform powered by OpenCV, Pillow, NumPy, Flask, and Groq `llama-3.3-70b-versatile`. It accepts user-uploaded photos, detects facial skin tones, classifies them into **Fair, Medium, Olive, or Deep**, and queries Groq for structured fashion, color palette, hairstyle, and accessory recommendations with curated Indian retailer search links (Amazon India, Myntra, Zara).

---

## 🌟 Key Features

- **Automated Face & Skin Tone Detection**: Uses OpenCV Haar Cascade classifier to isolate faces and sample cheek/forehead regions.
- **Color Extraction**: Filters out shadows/highlights (`V < 45` or `V > 245`) and non-skin noise (`S < 10`), using NumPy 20th–80th percentile trimming for skin tone classification.
- **Groq LLaMA 3.3 70B Integration**: Structured JSON recommendation engine providing outfits (Formal, Business, Casual, Party), hairstyle tips, accessories, and color palettes.
- **Curated Retailer Search Links**: Dynamically generates search links for Amazon India, Myntra, and Zara based on styling queries.
- **Modern Luxury UI**: Dark mode UI (`#0F172A`) with glassmorphism, responsive cards, micro-animations, drag-and-drop upload, and progress indicators.
- **Privacy & Security**: Ephemeral upload handling in `/tmp/styleai`, EXIF metadata stripping, strict CSP security headers.
- **Production-Ready**: WSGI (Gunicorn), Docker containerized, GitHub Actions CI/CD with Cloud Run auto-deploy and automatic rollback.

---

## 📋 Pre-requisites

Essential tools, software, and packages required before running or deploying the project:

- **Python 3.8+** – [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Flask** – [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **OpenCV** – [https://docs.opencv.org/](https://docs.opencv.org/)
- **Groq API Console (API Key)** – [https://console.groq.com/](https://console.groq.com/)
- **Git** – [https://git-scm.com/downloads](https://git-scm.com/downloads)
- **Visual Studio Code** – [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **PyCharm** – [https://www.jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)
- **NumPy** – [https://numpy.org/doc/](https://numpy.org/doc/)
- **python-dotenv** – [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)
- **pip (Python Package Installer)** – [https://pip.pypa.io/](https://pip.pypa.io/)

---

## 📁 Project Structure

```text
agentic ai/
├── api/
│   └── index.py                # Vercel Serverless Function Handler
├── styleai/
│   ├── data/
│   │   └── haarcascade_frontalface_default.xml # Bundled OpenCV Face Classifier
│   ├── services/
│   │   ├── groq_client.py       # Groq LLaMA 3.3 70B AI Integration
│   │   ├── image_analyzer.py    # OpenCV Face ROI & NumPy RGB Skin Analysis
│   │   ├── prompt_builder.py    # Structured Prompt Construction & Fallbacks
│   │   ├── recommendation_parser.py # JSON Parser & Type Normalizer
│   │   └── shopping_links.py    # Amazon, Myntra & Zara Search Link Generator
│   ├── utils/
│   │   ├── color_utils.py       # Luminance & Luma Skin Classification
│   │   ├── file_utils.py        # Ephemeral File Handling
│   │   └── security.py          # Upload Validation & Sanitization
│   ├── config.py                # App & Environment Configuration
│   ├── logging_config.py        # Structured Log Formatters
│   └── routes.py                # Flask Web Routes & API Handlers
├── static/
│   ├── css/styles.css           # Modern Dark Luxury UI Stylesheet
│   └── js/app.js                # Frontend Async Processing & Dynamic DOM
├── templates/
│   ├── base.html                # Shared Master Layout
│   └── index.html               # Main Styling Advisor Dashboard
├── tests/                       # Automated Pytest Integration & Unit Suite
├── vercel.json                  # Vercel Serverless Rewrite Config
├── requirements.txt             # Production Dependencies
├── app.py                       # Local Flask Entrypoint
└── wsgi.py                      # Production WSGI Gunicorn Launcher
```

---

## 🔌 API Endpoints

| Endpoint | Method | Input / Content-Type | Description | Response Format |
|---|---|---|---|---|
| `/` | `GET` | None | Serves main Web UI dashboard | HTML |
| `/analyze` | `POST` | `multipart/form-data` (`image`, `gender`) | Upload photo for skin tone & AI recommendations | JSON |
| `/healthz` | `GET` | None | Health check endpoint | JSON (`status: running`) |
| `/readyz` | `GET` | None | Readiness probe | JSON (`status: ready`) |
| `/version` | `GET` | None | Service version metadata | JSON |

---

## ⚡ Vercel Serverless Deployment

1. Connect your GitHub repository (`saikiran-dev6/StyleAI`) to Vercel.
2. Ensure [`vercel.json`](file:///c:/Users/SUSHMA%20SHYAMALA/OneDrive/Desktop/agentic%20ai/vercel.json) rewrites `/(.*)` to `/api/index.py`.
3. Set environment variables in Vercel Project Settings:
   - `GROQ_API_KEY`: *(Your Groq API key)*
   - `FLASK_ENV`: `production`
4. Deploy — Vercel automatically builds using `requirements.txt` and serves the app on your domain.

---

## 🏗️ Technical Architecture

```mermaid
flowchart LR
    U[User Browser] --> F[Flask App]
    F --> V[Upload Validation]
    V --> P[Pillow Preprocess & EXIF Strip]
    P --> C[OpenCV Face Detection]
    C --> S[Skin Tone Sampler]
    S --> N[NumPy RGB Stats]
    N --> K[Skin Tone Classifier]
    K --> G[Groq LLaMA 3.3 70B]
    G --> R[Structured Recommendation JSON]
    R --> L[Shopping Link Builder]
    L --> UI[Rendered Results Page]
```

---

## 🛠️ Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Required | Default / Example | Purpose |
|---|---|---|---|
| `FLASK_ENV` | Yes | `development` | Flask runtime mode |
| `SECRET_KEY` | Yes | `change-me-secret-key` | Session security |
| `MAX_CONTENT_LENGTH_MB` | Yes | `10` | Upload limit cap |
| `UPLOAD_TMP_DIR` | Yes | `/tmp/styleai` | Temporary directory |
| `GROQ_API_KEY` | Yes | `gsk_...` | Groq API Key |
| `GROQ_BASE_URL` | Yes | `https://api.groq.com/openai/v1` | Groq API Endpoint |
| `GROQ_MODEL` | Yes | `llama-3.3-70b-versatile` | LLaMA model |
| `APP_HOST` | Yes | `0.0.0.0` | Host bind address |
| `APP_PORT` | Yes | `8080` | Port bind address |

---

## 🚀 Quick Start (Local Development)

### 1. Install & Bootstrap Environment
```bash
bash scripts/bootstrap.sh
```

### 2. Run Local Development Server
```bash
bash scripts/dev.sh
# Server starts at http://localhost:8080
```

### 3. Run Test Suite & Code Quality Checks
```bash
bash scripts/test.sh
```

---

## 🐳 Docker & Containerization

Build and run locally with Docker Compose:

```bash
# Build production image
bash scripts/build.sh

# Run stack
docker-compose up --build -d

# Smoke test local stack
bash scripts/smoke_test.sh http://localhost:8080
```

---

## ☁️ Deployment & CI/CD Pipeline

The GitHub Actions workflows (`.github/workflows/ci.yml` and `cd.yml`) perform:
1. Linting & Unit/Integration testing (Coverage >= 85%)
2. Docker build & Artifact Registry push
3. Deploy to Google Cloud Run
4. Execute post-deploy smoke tests against public URL
5. Automatic rollback to previous Cloud Run revision if smoke test fails

### Manual Cloud Run Deploy
```bash
bash scripts/deploy_cloud_run.sh
```

### Manual Rollback
```bash
bash scripts/rollback_cloud_run.sh
```

---

## 🛡️ Production Runbook & Troubleshooting

1. **No Face Detected**: Ensure photo is clear, front-facing, and well-lit. The system will return a graceful 400 validation error if no face ROI is isolated.
2. **Groq API Timeout / Fallback**: If Groq API key is missing or invalid, the backend operates in mock mode for development. In production, check `LOG_LEVEL=INFO` logs for API HTTP status.
3. **Temp Directory Maintenance**: Files are processed in memory and `/tmp/styleai` and automatically deleted upon request completion.
