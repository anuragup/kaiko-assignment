import os, random, time
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

FAIL_RATE = float(os.getenv("FAIL_RATE", "0.02"))         # 2% default failure rate
READY_DELAY = int(os.getenv("READINESS_DELAY_SEC", "10")) # not ready for N seconds after start
GREETING = os.getenv("GREETING", "hello")
START_TIME = time.time()

REQS = Counter("http_requests_total", "HTTP requests", ["method","endpoint","code"])
LAT = Histogram("http_request_duration_seconds", "Req duration (s)", ["endpoint","method"])

@app.route("/healthz")
def healthz():
    REQS.labels("GET","/healthz","200").inc()
    return "ok", 200

@app.route("/readyz")
def readyz():
    if time.time() - START_TIME < READY_DELAY:
        REQS.labels("GET","/readyz","503").inc()
        return "not ready", 503
    REQS.labels("GET","/readyz","200").inc()
    return "ready", 200

@app.route("/work")
def work():
    t0 = time.time()
    # simulate variable latency
    time.sleep(random.uniform(0.05, 0.2))
    if random.random() < FAIL_RATE:
        LAT.labels("/work","GET").observe(time.time() - t0)
        REQS.labels("GET","/work","500").inc()
        return jsonify({"ok": False}), 500
    LAT.labels("/work","GET").observe(time.time() - t0)
    REQS.labels("GET","/work","200").inc()
    return jsonify({"ok": True, "greeting": GREETING}), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
