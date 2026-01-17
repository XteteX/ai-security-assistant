# AI Security Assistant — Phishing Detection Telegram Bot

AI Security Assistant is a machine-learning–based Telegram bot designed to detect phishing messages and suspicious URLs in real time.  
The system combines classical ML models with modern NLP techniques and optionally uses large language models (LLMs) to explain *why* a message was classified as phishing or safe.

This project focuses on **practical cybersecurity**, **robust ML engineering**, and **production-ready architecture**.

---

## 🔍 What the Project Does

- Detects phishing messages and malicious URLs
- Works directly inside Telegram
- Uses an ML model trained on real phishing data
- Extracts multiple heuristic, linguistic, and URL-based features
- Optionally generates human-readable explanations using Gemini API
- Designed to work **even without external AI APIs**

---

## 🧠 Core Features

### 1. Machine Learning–Based Detection
- Classical supervised ML model (Random Forest)
- TF-IDF text vectorization
- Hand-crafted security features:
  - phishing keywords
  - URL structure analysis
  - domain-level heuristics
  - message urgency indicators

### 2. URL & Domain Analysis
- Suspicious TLD detection
- Domain length and structure
- IP-based URLs
- Link count and patterns

### 3. Optional AI Explanation Layer (Gemini API)
- Uses Google Gemini API (free tier) **only for explanations**
- Explains decisions in 2–4 concise bullet points
- Fully optional:
  - If API key is missing or quota is exceeded, the bot still works
  - No dependency on LLMs for classification

### 4. Telegram Bot Interface
- Real-time interaction
- Simple and clear responses:
  - Prediction (Safe / Phishing)
  - Confidence score
  - Optional explanation

---

## 🏗️ Architecture Overview

User Message (Telegram)
↓
Feature Extraction
(Text + URL heuristics)
↓
ML Classifier (Random Forest)
↓
Prediction + Confidence
↓
(Optional) Gemini API Explanation
↓
Telegram Response

Key design principle: **Fail-safe architecture**  
External APIs never break core functionality.

---

## 🧪 Example Output

⚠️ Result: Phishing
Confidence: 0.67

Why this message looks suspicious:
• Contains urgency and pressure language
• Requests account verification
• Includes an external link
• Typical social engineering pattern


---

## ⚙️ Technologies Used

- Python 3
- scikit-learn
- pandas, NumPy
- TF-IDF (text vectorization)
- Random Forest classifier
- Telegram Bot API
- Google Gemini API (optional, explanation only)

---

## 🔐 Security & Privacy

- No user data is stored
- No personal information is logged
- API keys are handled via environment variables
- External AI is used only for explanation, not decision-making

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-security-assistant.git
cd ai-security-assistant
```

###2. Create and activate virtual environment
```bash
python -m venv venv
```
3. Install dependencies
 ```bash
pip install -r requirements.txt
```
4.  Set environment variables
   ```
$env:TG_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"

# Optional (for explanations only):
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```
5. Run the Telegram bot
```
python app/bot/tg_bot.py
```

🎓 Educational & Practical Value
This project demonstrates:

Applied machine learning in cybersecurity

Understanding of phishing and social engineering attacks

Feature engineering beyond basic text classification

Robust system design with optional AI components

Deployment of ML systems in real user-facing applications

The system is intentionally designed to function without relying on large language models, making it suitable for security-sensitive or cost-constrained environments.

📌 Possible Future Improvements

Multilingual phishing detection

Advanced domain reputation checks

Continuous model retraining

Web dashboard for analytics

Integration with other messaging platforms

📜 License

This project is released under the MIT License.
