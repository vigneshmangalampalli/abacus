
🚀 Features
🔹 Interactive Streamlit Dashboard

Upload or use sample billing data

Explore service-wise time-series charts

Filter insights dynamically

Simple, clean UI

🔹 Anomaly Detection Engine

Detects abnormal cost spikes

Flags unusual behavior in EC2, RDS, S3, Lambda, EKS

Uses statistical outlier detection

🔹 AI-Ready Summary Generator

Auto-generates cloud cost insights

Highlights top contributors

Suggests optimization areas

Easy to extend with LLMs

🔹 Modular & Developer Friendly

Separated into scripts:

streamlit_app.py

detect_anomalies.py

generate_summary.py

Uses mock data for offline testing

Clean architecture for scaling

🧠 Innovations

✨ Lightweight Cloud Analytics — No external cloud APIs required
✨ Real-world simulation — Mock 90-day dataset modeled after actual AWS billing patterns
✨ Extendable anomaly engine — Build custom detection rules
✨ LLM-ready insights — Designed to integrate with AI summarizers
✨ Portable & Offline — Works with local data only

📂 Project Structure
abacus/
│
├── streamlit_app.py              # Dashboard
├── detect_anomalies.py           # Cost anomaly detection
├── generate_summary.py           # Summary/insights engine
├── mock_billing_90d.csv          # 90-day mock dataset
│
├── plots/                        # Visualizations
│   ├── EC2_timeseries.png
│   ├── RDS_timeseries.png
│   ├── S3_timeseries.png
│   ├── Lambda_timeseries.png
│   └── EKS_timeseries.png
│
└── venv/                         # Virtual environment (ignored)

⚙️ Installation
1️⃣ Clone the Repository
git clone git@github.com:vigneshmangalampalli/abacus.git
cd abacus

2️⃣ Create a Virtual Environment
python -m venv venv

3️⃣ Activate It

Windows:

.\venv\Scripts\Activate.ps1

4️⃣ Install Requirements
pip install -r requirements.txt

▶️ Run the Dashboard
streamlit run streamlit_app.py


Opens automatically in your browser.

🧪 Run Analysis Scripts
🔍 Detect anomalies
python detect_anomalies.py

📝 Generate summary
python generate_summary.py
