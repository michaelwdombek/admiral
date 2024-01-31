from dataclasses import dataclass, field
from uuid import uuid4
import json


@dataclass
class Boat:
    fleet_id: uuid4
    naval_id: uuid4 = field(default_factory=uuid4)
    task: str = field(default=None)
    status: str = field(default="waiting")

    def render_json(self) -> str:
        return json.dumps({
            "fleet_id": str(self.fleet_id),
            "naval_id": str(self.naval_id),
            "task": self.task,
            "status": self.status
        })

