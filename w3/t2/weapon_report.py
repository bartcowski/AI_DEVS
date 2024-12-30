from typing import List
import uuid
from qdrant_client import models

class WeaponReportChunk:
    vector: List[float]
    original_text: str
    report_date: str
    weapon_name: str

    def __init__(self, vector, original_text, report_date, weapon_name):
        self.vector = vector
        self.original_text = original_text
        self.report_date = report_date
        self.weapon_name = weapon_name

    def to_qdrant_point(self) -> models.PointStruct:
        return models.PointStruct(
            id=str(uuid.uuid4()),
            payload={
                "original_text": self.original_text,
                "report_date": self.report_date,
                "weapon_name": self.weapon_name
            },
            vector=self.vector)
