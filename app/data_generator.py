from datetime import datetime
import random
from .models import Metric


def generate_metric():
    return Metric(
        timestamp=str(datetime.now()),
        cpu=random.uniform(10, 95),
        memory=random.uniform(20, 95),
        disk=random.uniform(30, 95),
        network=random.uniform(50, 600),
        error_rate=random.choice([0, 0, 1, 2, 10]),
        anomaly=1,
        score=0.0
    )
