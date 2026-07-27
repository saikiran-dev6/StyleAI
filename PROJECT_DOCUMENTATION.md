# Style AI - AI-Powered Fashion Styling Advisor with Groq

---

## 1. Project Description

StyleAI is an intelligent fashion styling platform that leverages Groq's LLaMA 3.3 70B AI model to provide comprehensive personal styling recommendations. The platform addresses the challenge of personalized fashion guidance by delivering AI-powered styling insights, skin tone analysis, outfit recommendations, and curated shopping links.

Using Groq's advanced language model, StyleAI analyzes user photos, detects skin tone, and generates gender-specific fashion recommendations tailored to individual profiles. The system ensures fast response times through Groq's optimized API while maintaining high-quality styling advice through sophisticated image processing and AI analysis.

StyleAI transforms personal styling into an intelligent, user-friendly experience through its modern interface, comprehensive feature set, and AI-powered analysis that provides personalized fashion guidance while considering skin tone, gender preferences, and current fashion trends.

### Scenarios

- **Scenario 1: Skin Tone Analysis & Initial Styling**  
  A user uploads a clear facial photograph to StyleAI. The system detects their skin tone category (Fair, Medium, Olive, Deep), analyzes the facial region for accurate color detection, and provides initial personalized styling recommendations. The AI suggests color palettes, outfit combinations, and accessories that complement their specific skin tone.

- **Scenario 2: Gender-Specific Fashion Recommendations**  
  A female user uploads her photo and indicates her gender preference. StyleAI generates tailored recommendations including:
  - Suitable dress codes (Formal, Business, Casual, Party)
  - Gender-specific outfit descriptions with tops, bottoms, and shoes
  - Hairstyle suggestions with maintenance tips
  - Accessory recommendations (earrings, necklaces, bracelets, watches)
  - Color palette guidance (primary, secondary, accent colors)
  - Detailed explanation of why recommendations work for her skin tone

- **Scenario 3: Curated Shopping Experience**  
  After receiving styling recommendations, the user accesses curated product links from major Indian retailers (Amazon.in, Myntra, Zara). Products are specifically selected based on the user's skin tone and gender, including direct shopping links for shirts, pants, shoes, and accessories from verified e-commerce platforms.

---

## 2. Architecture Overview

StyleAI is built as a modular platform combining a Flask backend with Groq's AI API for intelligent styling. The architecture prioritizes accuracy, speed, and user experience by leveraging advanced image processing and AI-driven recommendations.

### Core Technologies

- **Flask**: Lightweight Python web framework for routing and request processing.
- **Groq API**: Cloud-based AI inference using LLaMA 3.3 70B model.
- **OpenCV**: Advanced image processing and face detection (Haar Cascade classifier).
- **PIL (Pillow)**: Image manipulation, color extraction, and EXIF stripping.
- **NumPy**: Numerical computation for skin RGB statistics and percentile trimming.
- **HTML5 / CSS3 / JavaScript (ES6+)**: Modern, responsive luxury frontend with glassmorphism design and micro-animations.

### Pre-requisites

#### Software Requirements
- **Python 3.8+**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Groq API Key**: Obtain from [https://console.groq.com/](https://console.groq.com/)
- **Git**: [https://git-scm.com/downloads](https://git-scm.com/downloads)
- **Code Editor**: Visual Studio Code, PyCharm, or any preferred IDE

#### Knowledge Prerequisites
- **Python Basics**: Functions, classes, exception handling, data structures
- **Flask Framework**: Routing, application context, blueprints, request handling
- **HTML/CSS**: Semantic markup, Flexbox, CSS Grid, custom properties, animations
- **JavaScript**: DOM manipulation, async/await, Fetch API, FormData
- **Image Processing**: Color spaces (RGB, HSV), face detection, luminance calculation

---

## 3. Project Workflow

```
[Phase 1: Setup & API Config] ➔ [Phase 2: Core Backend] ➔ [Phase 3: Frontend UI] ➔ [Phase 4: Deployment] ➔ [Phase 5: Testing]
```

### Phase 1: Environment Setup & Groq API Configuration
- **Activity 1.1**: Set up Python environment and install dependencies (`requirements.txt`).
- **Activity 1.2**: Obtain and configure Groq API key (`.env`).
- **Activity 1.3**: Test Groq API connectivity and fallback mechanisms.

### Phase 2: Core Backend Development
- **Activity 2.1**: Set up Flask application structure and blueprints.
- **Activity 2.2**: Implement image upload, format validation, and security sanitization.
- **Activity 2.3**: Implement skin tone detection algorithm using OpenCV Haar Cascade and NumPy percentile statistics.
- **Activity 2.4**: Integrate Groq API for structured JSON styling recommendations.
- **Activity 2.5**: Develop retailer search link building system for Amazon India, Myntra, and Zara.

### Phase 3: Frontend Development
- **Activity 3.1**: Design responsive HTML templates with glassmorphism CSS aesthetics.
- **Activity 3.2**: Implement drag-and-drop image upload interface with preview.
- **Activity 3.3**: Create dynamic JavaScript styling recommendations and progress indicator modal.

### Phase 4: Deployment
- **Activity 4.1**: Configure local development server (`python app.py`) and Vercel serverless functions (`api/index.py`, `vercel.json`).

### Phase 5: Testing & Optimization
- **Activity 5.1**: Execute automated test suite (`pytest`) covering upload validation, skin classification, route handlers, and end-to-end integration.

---

## 4. Technical Architecture & Project Structure Setup

### Project Directory Structure

```text
agentic ai/
├── api/
│   └── index.py                # Vercel Serverless Function Handler
├── styleai/
│   ├── data/
│   │   └── haarcascade_frontalface_default.xml # OpenCV Haar Cascade Classifier
│   ├── services/
│   │   ├── groq_client.py       # Groq LLaMA 3.3 70B AI Integration
│   │   ├── image_analyzer.py    # OpenCV Face ROI & NumPy RGB Skin Analysis
│   │   ├── prompt_builder.py    # Structured Prompt Construction & Fallbacks
│   │   ├── recommendation_parser.py # JSON Parser & Type Normalizer
│   │   └── shopping_links.py    # Amazon, Myntra & Zara Search Link Generator
│   ├── utils/
│   │   ├── color_utils.py       # Luminance & Luma Skin Classification
│   │   ├── file_utils.py        # Ephemeral File & Stream Handling
│   │   └── security.py          # Upload Validation & Filename Sanitization
│   ├── config.py                # App & Environment Configuration
│   ├── logging_config.py        # Structured Logging Configurator
│   └── routes.py                # Flask Web Routes & API Handlers
├── static/
│   ├── css/styles.css           # Responsive Luxury Dark Mode Stylesheet
│   └── js/app.js                # Frontend Async Processing & Dynamic DOM
├── templates/
│   ├── base.html                # Master HTML5 Layout
│   └── index.html               # Main Styling Advisor Dashboard
├── tests/                       # Pytest Automated Test Suite (46 Test Cases)
├── .env                         # Local Environment Variables
├── .env.example                 # Environment Template
├── vercel.json                  # Vercel Serverless Rewrite Config
├── requirements.txt             # Production Dependencies
├── app.py                       # Local Application Launcher
└── wsgi.py                      # Production WSGI Server Launcher
```

---

## 5. Milestone 1: Environment Setup & Groq API Configuration

Establish the cloud AI infrastructure by configuring Groq API access and validating connectivity. This milestone ensures the AI backend is properly configured for generating styling recommendations.

### Activity 1.1: Install Dependencies & Setup Environment

Create `requirements.txt`:

```text
Flask
Flask-CORS
Pillow
opencv-python
groq
python-dotenv
Werkzeug
openai>=1.12.0
gunicorn>=21.2.0
numpy>=1.26.0
pytest>=8.0.0
pytest-cov>=4.1.0
ruff>=0.2.0
```

### Activity 1.2: Configure Groq API Key

Create `.env` file:

```env
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production-12345
MAX_CONTENT_LENGTH_MB=10
UPLOAD_TMP_DIR=/tmp/styleai

# Groq API Configuration
GROQ_API_KEY=gsk_your_groq_api_key_here
PI_KEY=gsk_your_groq_api_key_here
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TIMEOUT_SECONDS=90
GROQ_MAX_OUTPUT_TOKENS=1200
GROQ_TEMPERATURE=0.7

APP_HOST=0.0.0.0
APP_PORT=8080
LOG_LEVEL=INFO
```

#### Steps to Obtain Groq API Key:
1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up or log in.
3. Create an API key in the console under **API Keys**.
4. Copy key and paste into `.env` file under `GROQ_API_KEY` and `PI_KEY`.

---

## 6. Milestone 2: Core Backend Development

Build the Flask-based backend infrastructure that handles image uploads, performs skin tone detection, and coordinates AI requests to Groq. This milestone creates the foundation for all StyleAI features.

### Core Modules

1. **Flask Application Factory (`styleai/__init__.py`)**
   Configures CORS, global security headers (CSP, X-Frame-Options), error handlers for 413 and 500, and blueprint routes.

2. **Facial ROI & Skin Tone Analyzer (`styleai/services/image_analyzer.py`)**
   - Detects facial regions using Haar Cascade (`haarcascade_frontalface_default.xml`).
   - Extracts cheek and forehead region of interest (ROI).
   - Filters out shadows (`V < 45` or `V > 245`) and saturation noise (`S < 10`).
   - Uses NumPy 20th–80th percentile trimming on RGB channels.
   - Computes luminance:  
     $$\text{Luminance } (Y) = 0.299 \times R + 0.587 \times G + 0.114 \times B$$
   - Categorizes skin tone into **Fair**, **Medium**, **Olive**, or **Deep**.

3. **Groq LLaMA 3.3 70B Client (`styleai/services/groq_client.py`)**
   Formulates strict JSON system and user prompts, calls Groq API endpoint, and falls back to structured templates if API is unreachable.

4. **Recommendation Parser (`styleai/services/recommendation_parser.py`)**
   Validates root keys (`palette`, `outfits`, `hairstyle`, `accessories`, `rationale`, `shopping_queries`) and normalizes list/string types.

5. **Curated Retailer Search Link Builder (`styleai/services/shopping_links.py`)**
   Constructs encoded search links for Amazon India, Myntra, and Zara based on query items.

---

## 7. Milestone 3: Frontend Development - UI/UX Design

Create a modern, responsive user interface using HTML5, CSS3, and JavaScript that provides smooth image upload, real-time processing feedback, and styled recommendation display.

### Key Features
- Image upload form with drag-and-drop support
- Gender selection (Male/Female)
- Real-time upload progress indicator modal
- Styled results display with recommendations and shopping links
- Responsive design for desktop and mobile
- Modern CSS with glassmorphism, gradients, and micro-animations

### Component Breakdown
- **Upload Section**: File input with client-side format and size validation.
- **Processing Section**: Progress modal with step description during AI analysis.
- **Results Section**:
  - Detected skin tone display with RGB values, HEX swatch, and confidence metric.
  - AI-generated styling rationale and recommended color palettes.
  - 4-Category outfit combinations (Formal, Business, Casual, Party).
  - Hairstyle and maintenance tips.
  - Accessory chips.
  - Retailer product search cards for Amazon.in, Myntra, and Zara.

---

## 8. Milestone 4: Deployment

### Activity 4.1: Local & Production Deployment

#### Running Locally:
```bash
# Option 1: Direct Python Execution
python app.py

# Option 2: Shell script
bash scripts/dev.sh
```

Server binds to `http://127.0.0.1:8080` (or `0.0.0.0:8080`).

#### Vercel Serverless Deployment:
Configured via `vercel.json` and serverless entrypoint `api/index.py`:

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/api/index.py"
    }
  ]
}
```

---

## 9. Milestone 5: Testing & Optimization

### Activity 5.1: Functional Testing

#### Test Suite Execution:
```bash
python -m pytest
```

Result: **46 out of 46 Test Cases PASSED (100% Pass Rate)**

#### Test Case Coverage:
- **Test Case 1: Image Upload Validation** (`tests/test_upload_validation.py`)
  - Validates file selection, extension filtering (PNG, JPG, JPEG, GIF, WEBP), size caps, and filename sanitization.
- **Test Case 2: Skin Tone Detection & Recommendations** (`tests/test_image_analyzer.py` & `tests/test_skin_tone_classifier.py`)
  - Validates facial ROI detection, luminance calculation, color thresholding, JSON parser resilience, and shopping link construction.

### System Configuration Parameters

| Parameter | Configured Value | Description / Purpose |
|---|---|---|
| `MAX_FILE_SIZE` | `10MB` | Maximum allowed photo upload size |
| `ALLOWED_EXTENSIONS` | `png, jpg, jpeg, gif, webp` | Approved image format whitelist |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | High-performance AI styling model |
| `MAX_TOKENS` | `1200` | Token limit for structured styling JSON |
| `TIMEOUT` | `90 seconds` | API call timeout threshold |
| `TEMPERATURE` | `0.7` | Creative sampling temperature |

### Potential Enhancements
- Continuous skin tone color mapping beyond 4 categories.
- Inclusive gender options (non-binary, prefer not to say).
- Database integration for dynamic product catalogs.
- User accounts and saved styling history.
- Multi-photo upload for lighting-averaged color profiling.
- Virtual try-on augmented reality preview.
- Seasonal fashion trend integration.
- Personalized style preference learning.

---

## 10. Conclusion

This is the final section of a project report that summarizes the key work completed, highlights the main outcomes and findings, and provides closure to the document by reflecting on the project's overall success.

StyleAI successfully delivers an intelligent personal styling assistant that combines advanced image processing with cutting-edge AI analysis. By leveraging Groq's LLaMA 3.3 70B model, the system provides fast, accurate, and personalized fashion recommendations based on skin tone analysis and user preferences. The platform demonstrates the viability of AI-powered fashion guidance, making personalized styling accessible to everyone while maintaining high performance and accuracy.
