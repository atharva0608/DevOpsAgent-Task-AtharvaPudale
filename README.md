﻿
# DevOpsAgent-Task-AtharvaPudale

This project is a Proof of Concept (POC) for a self-healing AI-powered DevOps agent. It monitors CPU usage using Prometheus, analyzes logs using a local LLM (`tinyllama` via Ollama), and performs automatic remediation like restarting a Docker container. It also includes a simple Streamlit dashboard to visualize data.

---

## 📦 Features

- Monitor CPU usage using Prometheus Node Exporter
- Analyze logs using local LLM (TinyLLaMA via Ollama)
- Automatically restart misbehaving Docker container
- Send email notifications for incidents
- Log all actions in a file
- Basic web dashboard with Streamlit

---

## 🛠 Prerequisites

- Ubuntu (Tested on t3.large EC2 instance)
- Python 3.10+
- Docker and Docker Compose
- Prometheus + Node Exporter
- Ollama installed (for TinyLLaMA)
- Gmail account with App Password (for alerts)

---
## ☁️ EC2 Setup (Ubuntu 22.04)

### 1. Launch an EC2 instance using:
   - **AMI**: Ubuntu 22.04
   - **Instance Type**: `t3.large`
   - **Storage**: 20 GB minimum
   - **Key Pair**: Select or create one

### 2. Add the following inbound rules to your EC2 Security Group:

| Type            | Port | Source    | Description              |
|-----------------|------|-----------|--------------------------| 
| SSH             | 22   | Your IP   | SSH                      | 
| Custom TCP      | 9090 | Anywhere  | Prometheus               |
| Custom TCP      | 9100 | Anywhere  | Prometheus Node Exporter |
| Custom TCP      | 8501 | Anywhere  | Streamlit                |
| Custom TCP      | 11434| Anywhere  | LLM API                  |

### 3. Connect via SSH:

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```
### 4.  Install System Packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose git curl python3 python3-pip python3-venv
```
### 5. Add your current user to the docker group
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 🔧 Step-by-Step Setup

### 1. Clone the project

``` bash
git clone https://github.com/atharva0608/DevOpsAgent-Task-AtharvaPudale.git
cd DevOpsAgent-Task-AtharvaPudale
```

### 2. Set up Python environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 3. Start Prometheus + Node Exporter (Monitoring Stack)
```bash
docker-compose up -d
```
Make sure Prometheus is running on:
`http://<ec2-public-ip>:9090`
### 4. Start Ollama with TinyLLaMA (LLM Runtime)
```bash
chmod +x llm-setup.sh
./llm-setup.sh
```
### 5. Run a test container to simulate CPU spike
```bash
chmod +x test-app.sh
./test-app.sh
```
### 6. Run the monitoring agent
```bash
python3 monitor.py
```
This will:

- Continuously check CPU usage via Prometheus
- Trigger analysis using LLM when threshold exceeded
- Restart the container if needed
- Send email alerts
- Save logs to `remediation_log.txt` (auto genrated)
### 7. Launch the Streamlit dashboard (optional)
```bash
streamlit run app.py
```
Visit `http://<ec2-public-ip>:9090`
You’ll see:
- Live CPU usage
- Last LLM analysis
- Full remediation history


