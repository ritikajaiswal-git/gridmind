# ⚡ GridMind: Smart Microgrid AI 🌍

![GridMind Banner](https://img.shields.io/badge/Status-Hackathon_Ready-success?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/AI-XGBoost-blue?style=for-the-badge)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge)
![Frontend](https://img.shields.io/badge/Frontend-React.js-61DAFB?style=for-the-badge)
![Blockchain](https://img.shields.io/badge/Security-SHA--256-purple?style=for-the-badge)

## 📌 The Problem
Traditional power grids and basic solar/battery systems are **reactive**. They drain battery reserves during minor daytime demand spikes, leaving the system completely empty when the real evening peak arrives. This forces reliance on heavily polluting government grids (coal-powered) precisely when electricity is most expensive and carbon-intensive. 

## 💡 Our Solution
**GridMind** is an intelligent, forecast-aware microgrid controller. Instead of blindly reacting to current demand, it uses Machine Learning to look into the future. By predicting upcoming weather and load, it proactively "pre-charges" or "holds" battery reserves for evening peak hours, ensuring zero grid reliance when it matters most.

## ✨ Key Features
*   🧠 **AI Forecasting Engine:** Uses **XGBoost** with time-cyclical features (sin/cos) and historical lag data to predict solar generation accurately.
*   🔋 **Smart Pre-Charge Brain:** Time-aware logic that halts battery discharge during the afternoon, saving capacity for the 18:00–22:00 high-demand window.
*   🔗 **Tamper-Proof Carbon Ledger:** A cryptographic blockchain implementation using **SHA-256 hashing**. It accurately logs every kg of CO2 saved (using India's 0.71 kg/kWh grid emission factor) and links records via previous hashes, rendering greenwashing impossible.
*   📊 **Real-Time Polling Dashboard:** A React-based interactive UI with live Recharts, a dynamic circular battery gauge, and a real-time Carbon Blockchain feed.
*   🕹️ **Interactive AI Toggle:** A live "AI ON/OFF" switch to visually demonstrate to operators (and judges) how the system fails without AI and thrives with it.

## 🛠️ Technology Stack
*   **AI/ML:** Python, Pandas, NumPy, XGBoost, Scikit-learn
*   **Backend & Simulation:** FastAPI, Uvicorn, Python Asyncio
*   **Frontend UI:** React.js, Vite, Axios, Recharts, Lucide-React
*   **Security/Blockchain:** Python Hashlib (SHA-256)

## 🚀 How to Run Locally

**1. Clone the repository:**
```bash
git clone [https://github.com/ritikajaiswal-git/gridmind.git](https://github.com/ritikajaiswal-git/gridmind.git)
cd gridmind