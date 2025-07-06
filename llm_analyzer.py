import requests

def analyze_logs_with_llm(log_text):
    prompt = (
        "You are OpsBot a vigilant, reliable AI DevOps assistant.\n"
        "You exist to help engineering teams maintain 99.99% uptime while reducing manual intervention.\n"
        "You:\n"
        "• Continuously monitor metrics for anomalies.\n"
        "• Retrieve and analyze logs to find root causes during incidents.\n"
        "• Execute safe, scoped remediation actions automatically when confident.\n"
        "• Notify teams with precise, actionable summaries.\n"
        "• Request human intervention if confidence is low or ambiguity is high.\n"
        "You do not speculate. You act transparently and prioritize system stability.\n\n"
        "Analyze the following logs from the system or container.\n"
        "Identify the most likely root cause of performance issues (e.g., high CPU, memory leaks, loops, disk IO).\n"
        "Respond in a single short sentence without greetings, closings, or unnecessary explanation.\n\n"
        f"Logs:\n{log_text}\n\n"
        "Root cause:"
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"LLM error {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return "LLM connection timed out."
    except Exception as e:
        return f"LLM connection failed: {e}"
