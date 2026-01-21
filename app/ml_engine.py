import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

def run_anomaly_detection(metrics):
    df = pd.DataFrame([{
        "cpu": m.cpu,
        "memory": m.memory,
        "disk": m.disk,
        "network": m.network,
        "error_rate": m.error_rate
    } for m in metrics])

    scaler = StandardScaler()
    X = scaler.fit_transform(df)

    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    preds = model.fit_predict(X)
    scores = model.decision_function(X)

    severity = (scores.max() - scores) * 100

    return preds, severity
