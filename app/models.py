from sqlalchemy import Column, Integer, Float, String
from .database import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String)

    cpu = Column(Float)
    memory = Column(Float)
    disk = Column(Float)
    network = Column(Float)
    error_rate = Column(Float)

    anomaly = Column(Integer, default=1)
    score = Column(Float, default=0.0)
