Absolutely. Below is the **complete `README.md` content in proper Markdown format**, ready to copy directly into your `README.md` file.

````markdown
# 🌦️ WeatherGPT

## AI-Powered Hyperlocal Weather Risk & Decision Intelligence Platform

WeatherGPT is an AI-powered weather decision-support platform designed to go beyond simply displaying weather information.

Instead of only answering:

> **"What is the weather?"**

WeatherGPT aims to answer:

> **"Considering the weather, my activity, and the forecast, what should I do?"**

The system combines live weather data, forecast information, weather hazards, activity-specific risk analysis, and a Large Language Model (LLM) to provide understandable and actionable weather guidance.

---

## 🎯 Problem Statement

Traditional weather applications primarily present raw weather information such as:

- Temperature
- Humidity
- Wind
- Rainfall
- Forecasts
- Weather alerts

However, users often need a **decision** rather than a collection of numbers.

For example:

> "Is it safe to go cycling at 9 PM?"

> "Should I go for a run now or later?"

> "Is the weather suitable for driving?"

WeatherGPT converts weather information into an **activity-aware risk assessment and actionable recommendation**.

This project is developed for the Smart India Hackathon 2026 problem statement:

**SIH26068 — WeatherGPT: Conversational AI for Weather Forecasting, Alerts, and Climate Information**

**Organization:** Ministry of Earth Sciences (MoES)  
**Category:** Software  
**Theme:** Disaster Management

---

# 🚀 Key Features

## 1. 📍 Location-Based Weather Analysis

Users can enter a city and obtain weather intelligence for that location.

The system resolves the location and provides information such as:

- Location
- District
- State
- Country
- Latitude
- Longitude

---

## 2. 🌤️ Current Weather

WeatherGPT retrieves current weather information including:

- Temperature
- Feels-like temperature
- Humidity
- Atmospheric pressure
- Wind speed
- Wind direction
- Rainfall
- Visibility
- Cloud cover
- Weather condition

The current weather service uses **Open-Meteo** as its weather-data source.

---

## 3. ⏱️ Hourly Forecast

WeatherGPT analyzes forecast conditions hour-by-hour.

Users can specify a forecast window using:

- Start time
- End time

The system evaluates the selected forecast period instead of providing only a single weather value.

---

## 4. 📅 Daily Forecast

The platform also provides daily weather forecast information for broader planning.

This allows users to understand weather conditions beyond the immediate hours.

---

# 🧠 5. Weather Risk Intelligence

This is one of the core components of WeatherGPT.

Instead of simply displaying weather measurements, the backend converts multiple weather signals into a **risk score from 0–100**.

The risk engine considers factors including:

- Rainfall
- Wind
- Heat
- Visibility
- Weather hazards
- Weather severity
- Weather warnings
- Selected activity
- Context-specific risk

The system produces:

```text
Risk Score
Risk Level
Peak Risk
Average Risk
Risk Trend
Peak Hazard
Hourly Risk Results
```

---

# 🎯 6. Activity-Aware Risk

WeatherGPT is not designed around weather alone.

The user can select an activity such as:

- General
- Walking
- Running
- Cycling
- Bike
- Driving

The same weather conditions can have different implications depending on the activity.

For example:

```text
Weather:
Light rain + moderate wind

Walking:
Possibly manageable

Cycling:
Higher practical risk

Driving:
Different risk considerations
```

This allows WeatherGPT to provide **decision-oriented weather intelligence** instead of generic weather information.

---

# 🚦 7. Decision Intelligence

After calculating the weather risk, WeatherGPT generates a structured decision.

Example:

```text
Risk Level: Low
Risk Score: 9.74
Hazard: None
Priority: Low

Recommendation:
Weather conditions are generally suitable
for your activity.
```

The decision layer converts numerical analysis into an understandable recommendation.

Possible risk levels include:

- Low
- Moderate
- High
- Critical

---

# 📊 8. Hour-by-Hour Risk Analysis

WeatherGPT provides detailed hourly analysis.

Each forecast hour can contain:

- Time
- Overall risk
- Risk level
- Weather condition
- Rain risk
- Wind risk
- Heat risk
- Visibility risk
- Weather hazard
- Warning information
- Activity information
- Context risk

This makes it possible to identify **better or worse time windows** for an activity.

---

# ⚠️ 9. Weather Hazard & Warning Intelligence

The risk system can incorporate weather hazards and warning information.

The backend includes integration for:

**India Meteorological Department (IMD)** district warning data.

This allows the platform to consider official warning information in addition to forecast weather variables.

---

# 🤖 10. Conversational WeatherGPT

WeatherGPT includes a conversational AI layer.

Users can ask questions such as:

```text
Is it safe to cycle now?

What about at 9 PM?

Will the rain affect my cycling?

Should I go later?

Why is the risk moderate?

What is causing the risk?
```

The conversational endpoint receives relevant:

- Weather information
- Forecast information
- Risk analysis
- Decision
- Activity
- User preferences

This allows follow-up questions to be answered using the current WeatherGPT analysis.

---

# 🧠 LLM Integration

WeatherGPT currently uses:

## Google Gemini

Configured model:

```text
gemini-2.5-flash-lite
```

The LLM is used primarily for:

- Natural-language explanation
- Conversational interaction
- Personalized weather guidance

The LLM does **not** directly replace the weather-risk engine.

Instead, the architecture follows:

```text
Weather Data
      ↓
Risk Engine
      ↓
Decision Intelligence
      ↓
WeatherGPT Context
      ↓
Gemini LLM
      ↓
Natural Language Explanation
```

The Gemini API key remains on the backend and is never exposed to the frontend.

---

# 💡 Why WeatherGPT Is Different

A general-purpose LLM can answer weather-related questions, but WeatherGPT is designed specifically as a **weather decision-intelligence system**.

The key distinction is:

```text
Traditional Weather App
        ↓
Weather Information


General LLM
        ↓
Natural Language Answer


WeatherGPT
        ↓
Weather Data
        ↓
Forecast
        ↓
Risk Analysis
        ↓
Activity Context
        ↓
Decision Intelligence
        ↓
LLM Explanation
```

The LLM is therefore used as the **communication and reasoning interface over structured weather intelligence**, rather than being treated as the source of weather data itself.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │        User          │
                    │    Web Dashboard     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌─────────────┐
       │ Open-Meteo │   │    IMD     │   │ Risk Engine │
       │   Weather  │   │  Warnings  │   │             │
       └──────┬─────┘   └──────┬─────┘   └──────┬──────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Decision Intelligence│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Gemini LLM       │
                    │ gemini-2.5-flash-lite│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Personalized Answer  │
                    └──────────────────────┘
```

---

# 🛠️ Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- Pydantic Settings
- SQLAlchemy
- Alembic
- Uvicorn

## Weather & External Data

- Open-Meteo Weather API
- Open-Meteo Geocoding API
- IMD weather warning data

## Artificial Intelligence

- Google Gemini
- `gemini-2.5-flash-lite`

## Frontend

- HTML5
- CSS3
- JavaScript

The frontend is served directly through the FastAPI application from the backend's static directory.

## Database

- SQLite
- SQLAlchemy ORM
- Alembic migrations

## Deployment

The project contains deployment-oriented configuration for:

- Docker
- Docker Compose
- Render

---

# 📂 Project Structure

```text
WeatherGPT/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   ├── health.py
│   │   │   ├── risk.py
│   │   │   └── weather.py
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── data/
│   │   │   └── collectors/
│   │   │       └── open_meteo.py
│   │   │
│   │   ├── risk/
│   │   │   ├── context_risk.py
│   │   │   └── forecast_risk.py
│   │   │
│   │   ├── services/
│   │   │   ├── forecast_service.py
│   │   │   ├── imd_warning_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── location_service.py
│   │   │   ├── risk_service.py
│   │   │   └── weather_service.py
│   │   │
│   │   └── static/
│   │       ├── css/
│   │       │   └── dashboard.css
│   │       │
│   │       ├── js/
│   │       │   └── dashboard.js
│   │       │
│   │       └── index.html
│   │
│   ├── migrations/
│   ├── test/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic.ini
│
├── docs/
│
├── .env.example
├── .gitignore
├── README.md
├── docker-compose.yml
└── render.yaml
```

---

# 🔌 API Endpoints

WeatherGPT currently exposes the following main endpoints.

## Health Check

```http
GET /health/
```

Checks whether the backend service is running.

---

## Current Weather

```http
GET /api/weather/current
```

Example:

```http
GET /api/weather/current?city=Hyderabad
```

---

## Hourly Forecast

```http
GET /api/weather/hourly
```

Provides hourly forecast information.

---

## Daily Forecast

```http
GET /api/weather/daily
```

Provides daily forecast information.

---

## Forecast Risk

```http
GET /api/risk/forecast
```

Example:

```http
GET /api/risk/forecast?city=Hyderabad&start_time=2026-09-04T17:09:00&end_time=2026-09-05T19:09:00&activity=cycling
```

The response contains:

```text
Location
Activity
Risk Summary
Hourly Risk Results
Decision
```

---

## Explain Weather

```http
POST /api/chat/explain
```

Generates an LLM-powered explanation of the supplied weather and risk assessment.

---

## Conversational Chat

```http
POST /api/chat/message
```

Allows users to ask follow-up questions using conversation context.

Example:

```json
{
  "message": "What about at 9 PM?",
  "conversation_id": "conversation-id",
  "city": "Hyderabad",
  "activity": "Cycling"
}
```

The frontend sends the relevant weather, hourly forecast, risk, decision, and user preferences along with the question.

---

## Clear Conversation

```http
DELETE /api/chat/conversation/{conversation_id}
```

Clears a conversation context.

---

# 🖥️ Dashboard

The current dashboard provides the following functionality.

## Weather Analysis

Users can select:

- Location
- Activity
- Start time
- End time

and click:

**Analyze Weather Risk**

---

## Current Conditions

The dashboard displays:

- Temperature
- Feels-like temperature
- Humidity
- Wind
- Rainfall
- Visibility
- Weather condition

---

## Decision Intelligence

The dashboard displays:

- Overall risk
- Risk score
- Risk level
- Recommendation
- Priority
- Main hazard

---

## Forecast Analysis

The dashboard displays:

- Hours analyzed
- Average risk
- Peak risk
- Risk trend
- Hour-by-hour risk

---

## AI Weather Assistant

Users can:

- Ask follow-up questions
- Ask whether a later time is better
- Ask why the risk exists
- Ask for activity-specific guidance
- Start a new conversation

The dashboard communicates with the backend conversational API and maintains the returned conversation ID.

---

# 🔐 Security

Sensitive credentials are kept on the backend.

The Gemini API key is loaded through environment configuration:

```text
GEMINI_API_KEY
```

The frontend never receives the API key.

The communication flow is:

```text
Frontend
    ↓
FastAPI Backend
    ↓
Gemini API
```

This keeps the API credential away from the client-side code.

---

# ⚙️ Environment Configuration

Create a `.env` file inside the `backend` directory.

Example:

```env
APP_NAME=WeatherGPT
APP_VERSION=1.0.0
DEBUG=False

DATABASE_URL=sqlite:///./weathergpt.db

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
```

> **Important:** Never commit the actual `.env` file or API keys to GitHub.

Use:

```text
.env.example
```

as the template for environment configuration.

---

# ▶️ Running Locally

## 1. Clone the Repository

```bash
git clone https://github.com/mohammednouman555/WeatherGPT.git
```

```bash
cd WeatherGPT
```

---

## 2. Create a Virtual Environment

Navigate to the backend:

```bash
cd backend
```

### Windows

```bash
py -3.10 -m venv .venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```text
backend/.env
```

Add the required configuration.

At minimum:

```env
GEMINI_API_KEY=your_api_key
```

---

## 5. Start the FastAPI Server

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The backend should start at:

```text
http://127.0.0.1:8000
```

---

# 🌐 Access the Dashboard

Open:

```text
http://127.0.0.1:8000/dashboard/
```

The FastAPI application serves the frontend directly from the backend's static directory.

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

The Swagger documentation allows developers to test:

- Health API
- Weather APIs
- Risk API
- Chat APIs
- Conversation management

without requiring a separate API client.

---

# 🐳 Docker

The project also contains Docker configuration for containerized deployment.

Build and run using:

```bash
docker compose up --build
```

After the containers start, access the application through the configured service port.

---

# ☁️ Deployment

The project is structured for cloud deployment.

Deployment-related files include:

```text
backend/Dockerfile
docker-compose.yml
render.yaml
```

Environment variables such as the Gemini API key should be configured through the deployment platform's environment-variable or secret settings.

They should **not** be committed to GitHub.

---

# 🧪 Testing

Backend tests are maintained under:

```text
backend/test/
```

Run the test suite using:

```bash
pytest
```

---

# 🔄 End-to-End Workflow

The complete WeatherGPT workflow is:

```text
1. User selects location
             ↓
2. User selects activity
             ↓
3. User selects forecast window
             ↓
4. Backend resolves location
             ↓
5. Weather data is collected
             ↓
6. Forecast data is collected
             ↓
7. Weather warnings are considered
             ↓
8. Risk engine evaluates weather factors
             ↓
9. Activity context is applied
             ↓
10. Overall risk score is generated
             ↓
11. Decision intelligence is generated
             ↓
12. Results are displayed
             ↓
13. User can ask WeatherGPT a question
             ↓
14. Weather + risk + decision context
    is sent to Gemini
             ↓
15. Gemini generates a natural-language explanation
             ↓
16. WeatherGPT displays the response
```

---

# 🧩 Design Philosophy

WeatherGPT follows a separation-of-responsibilities architecture.

## Weather Data Layer

Responsible for retrieving:

- Current weather
- Forecast data
- Location information
- Weather warnings

---

## Risk Intelligence Layer

Responsible for calculating:

- Weather risk
- Activity-related risk
- Hazard impact
- Forecast risk

---

## Decision Layer

Responsible for converting the risk analysis into:

- Risk level
- Recommendation
- Priority
- Main hazard
- Decision intelligence

---

## LLM Layer

Responsible for:

- Natural-language explanation
- Conversational interaction
- Follow-up questions
- User-friendly communication

This separation prevents the LLM from becoming the sole source of weather-risk calculations.

---

# 📌 Current Prototype Status

The current prototype successfully demonstrates:

- ✅ FastAPI backend
- ✅ Health check
- ✅ Current weather API
- ✅ Hourly forecast API
- ✅ Daily forecast API
- ✅ Forecast risk analysis
- ✅ Activity-aware risk
- ✅ Risk score and risk level
- ✅ Hourly risk breakdown
- ✅ Decision intelligence
- ✅ Weather hazard identification
- ✅ IMD warning integration
- ✅ Gemini LLM integration
- ✅ Weather explanation
- ✅ Conversational WeatherGPT endpoint
- ✅ Conversation IDs
- ✅ Conversation clearing
- ✅ User preferences
- ✅ Web dashboard
- ✅ Backend-served frontend
- ✅ Interactive Swagger API documentation
- ✅ Docker deployment configuration
- ✅ Render deployment configuration

---

# 🚧 Future Enhancements

Potential future improvements include:

- 📍 GPS-based location detection
- 🗺️ Interactive weather-risk maps
- 🔔 Real-time severe weather alerts
- 📱 Progressive Web App / mobile application
- 🌧️ More advanced rainfall prediction
- 🛰️ Satellite and radar data integration
- 🌍 Multilingual conversational support
- 📈 Historical weather-risk analytics
- 👤 Persistent user profiles
- 🔔 Personalized risk notifications
- 🧠 More advanced predictive risk models
- ☁️ Production-grade database deployment
- 📊 Analytics dashboard
- 🏛️ Integration with additional official Indian meteorological data sources

---

# 🏆 Why WeatherGPT Matters

WeatherGPT is not intended to be another weather dashboard.

Its core idea is:

> **Convert weather information into decisions.**

Instead of forcing users to interpret multiple weather measurements themselves, WeatherGPT combines:

- Weather conditions
- Forecasts
- Hazards
- Activity context
- Risk analysis
- Decision intelligence
- Conversational AI

to provide an understandable recommendation.

The final concept is:

```text
Weather Data
      +
Forecast
      +
Risk Intelligence
      +
Activity Context
      +
Conversational AI
      =
Actionable Weather Decisions
```

---

# 👥 Team

Developed as a team project for:

## Smart India Hackathon 2026

**Problem Statement:**  
SIH26068 — WeatherGPT: Conversational AI for Weather Forecasting, Alerts, and Climate Information

**Organization:**  
Ministry of Earth Sciences (MoES)

**Category:**  
Software

**Theme:**  
Disaster Management

---

# 📄 License

This project is currently developed as an academic and hackathon prototype.

An appropriate open-source license can be added if the project is later intended for public redistribution.

---

# ⭐ WeatherGPT

### From "What is the weather?"

### To "What should I do because of the weather?"
````