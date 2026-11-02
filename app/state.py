"""Estado compartido de la aplicación (en memoria)."""

from __future__ import annotations

from dataclasses import dataclass, field

from app import data


@dataclass
class AppState:
    route: str = "home"
    inscriptions: set[str] = field(default_factory=set)
    exam_filters: dict = field(
        default_factory=lambda: {
            "query": "",
            "materia": data.MATERIAS[0],
            "estado": "todos",
        }
    )
    procedure_id: str = data.PROCEDURES[0]["id"]
    appointment: dict = field(default_factory=data.new_appointment_draft)
    confirmed: dict = field(default_factory=lambda: dict(data.DEFAULT_CONFIRMED))

    def reset_appointment(self) -> None:
        self.appointment = data.new_appointment_draft()
