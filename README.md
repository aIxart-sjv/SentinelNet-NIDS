🛡️ SentinelNet – AI Powered Network Intrusion Detection System

SentinelNet is a Machine Learning–based Network Intrusion Detection System (NIDS) that detects malicious network traffic in real time.
It combines offline model training with live packet capture to classify network flows as Benign or Attack.


🚀 Features

✅ Real-time network traffic monitoring using packet capture
✅ Machine learning–based intrusion detection
✅ Binary classification: Benign vs Attack
✅ High accuracy (~99%) using XGBoost
✅ Feature importance & explainability
✅ Modular project structure
✅ Live detection with console alerts


📂 Project Structure

SentinelNet-NIDS/
│
├── data/
│   ├── raw/              # Original dataset files (parquet / csv)
│   └── processed/        # Cleaned datasets (optional)
│
├── notebooks/            # Data exploration & training notebooks
│
├── src/                  # Core application code
│   ├── preprocessing.py
│   ├── train.py
│   ├── evaluate.py
│   ├── explain.py
│   ├── run_detector.py   # Offline detection
│   └── live_detector.py  # Live packet detection
│
├── models/               # Saved trained models
│
├── results/              # Plots, metrics, reports
│
├── requirements.txt
└── README.md


📊 Dataset

Dataset: CICIDS2017
Records: 2.3+ million network flows
Features: 78 network flow features
Attack Types:
DDoS
DoS (Hulk, Slowloris, GoldenEye)
Brute Force (FTP / SSH)
Port Scan
Web Attacks


🧠 Machine Learning Models

🌲 Random Forest – Baseline model
⚡ XGBoost – High‑performance optimized model


Performance:

Accuracy ≈ 99%
High precision and recall for attack detection
Low false positives and false negatives


🛠️ Tech Stack

Programming: Python
Data Processing: Pandas, NumPy
Machine Learning: Scikit-learn, XGBoost
Visualization: Matplotlib, Seaborn
Explainability: SHAP
Network Capture: Scapy, Npcap
Model Saving: Joblib
Development: Jupyter Notebook, VS Code, Git


⚙️ Installation

1️⃣ Clone Repository

git clone <your-repository-url>
cd SentinelNet-NIDS

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ (Windows Only) Install Npcap

Npcap is required for live packet capture.

Download from:
👉 https://npcap.com

During installation:
✔ Enable WinPcap compatibility mode
✔ Restart your system

▶️ Running the Project
✅ Run Offline Detection (From Dataset)
cd src
python run_detector.py
This loads a dataset file and predicts whether flows are benign or malicious.

🌐 Run Live Intrusion Detection
Run terminal as Administrator

cd src
python live_detector.py
Now generate traffic:

Open websites
Run ping commands
Download files
You will see real-time output like:

[LIVE] Flow 12: ✅ BENIGN
[LIVE] Flow 13: 🚨 ATTACK DETECTED

📈 Model Training

Training and evaluation are performed in Jupyter notebooks located in:

notebooks/

Steps include:

Data cleaning
Feature scaling
Train-test split
Model training
Evaluation
Feature importance & SHAP analysis

⚠️ Limitations

Live detection uses simplified features for demonstration.
Full CIC feature extraction in real time is computationally expensive.
Encrypted traffic limits packet visibility.
High-speed networks require stronger hardware.

🚀 Future Enhancements

Multi-class attack classification
Real-time dashboard visualization
Automatic blocking of malicious IPs
Deep learning models (LSTM, Autoencoders)
Cloud deployment

👨‍💻 Authors

Sitti Jaivardhan
Vijaya Bhaskar K P

📜 License

This project is for academic and research purposes.
