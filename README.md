# WalletGuard: AI-Powered Fraud Detection
**Final Year Project: AI in Business**

## 🛡️ Project Overview
WalletGuard is a proactive fraud detection prototype designed for the Pakistani mobile wallet ecosystem (JazzCash & Easypaisa). It moves beyond reactive security by implementing real-time anomaly analytics and an automated risk-scoring engine.

## 🚀 Key Features
- **Real-Time Simulation:** Generates synthetic Pakistani transaction data (Karachi, Lahore, etc.).
- **Multi-Factor Risk Engine:** Scores transactions based on Timing, Amount, Device, Location, Frequency, and Demographics.
- **Interactive Response Window:** Simulates a 30-second window for bank operators to "Confirm Safe" or "Block & Report" flagged anomalies.
- **Business Dashboard:** Visualizes system performance metrics and risk profiles using Plotly Radar Charts.
- **Audit Logging:** Generates SBP-compliant audit logs for forensic analysis.

## 🛠️ Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure
- `app.py`: Main Streamlit application and GUI.
- `model.py`: Core Risk Scoring Engine and transaction generator.
- `create_dataset.py`: Script to generate the 100,000-row synthetic dataset.
- `business_report.md`: Comprehensive academic-grade business report.
- `audit_log.csv`: (Auto-generated) Security logs for flagged transactions.

## 📈 Methodology
Risk Score = (Timing × 0.25) + (Amount × 0.20) + (Device × 0.20) + (Location × 0.15) + (Frequency × 0.12) + (Demographics × 0.08)

Transactions with a score > 70 are flagged as anomalies requiring immediate intervention.
