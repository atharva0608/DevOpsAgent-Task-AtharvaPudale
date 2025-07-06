import time
from prometheus_api_client import PrometheusConnect
import subprocess
import smtplib
from email.mime.text import MIMEText
from llm_analyzer import analyze_logs_with_llm

prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)
CPU_THRESHOLD = 80.0
CHECK_DURATION = 120

def get_cpu():
    try:
        query = '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
        result = prom.custom_query(query=query)
        if result:
            return float(result[0]['value'][1])
    except Exception as e:
        print("Error getting CPU:", e)
    return 0.0

def read_logs(container="test-app"):
    try:
        result = subprocess.run(["docker", "logs", "--tail", "50", container], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error reading logs: {e}"

def restart():
    print("Restarting container...")
    subprocess.run(["docker", "restart", "test-app"])

def notify(subject, message):
    sender = "your-email"
    password = "your-password"  
    to = "recivers-email"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(" Email sent")
    except Exception as e:
        print("Email failed:", e)

def log_action(cpu, after, reason):
    with open("remediation_log.txt", "a") as f:
        f.write(f"CPU: {cpu:.2f}% -> {after:.2f}% | Reason: {reason}\n")

def main():
    print(" Monitoring started")
    count = 0

    while True:
        cpu = get_cpu()
        print(f"CPU Usage: {cpu:.2f}%")

        
        with open("cpu_status.txt", "w") as f:
            f.write(f"{cpu:.2f}")

        if cpu > CPU_THRESHOLD:
            count += 1
        else:
            count = 0

        if count >= (CHECK_DURATION // 30):
            logs = read_logs()
            reason = analyze_logs_with_llm(logs)
            print(" LLM Analysis:", reason)

            
            with open("last_analysis.txt", "w") as f:
                f.write(reason)

            restart()
            time.sleep(60)
            after = get_cpu()

            log_action(cpu, after, reason)
            notify("CPU Alert", f"Before: {cpu:.2f}%\nAfter: {after:.2f}%\n{reason}")
            count = 0

        time.sleep(30)

if __name__ == "__main__":
    main()
