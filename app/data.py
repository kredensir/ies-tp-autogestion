"""Datos de demostración del portal.

No hay backend: toda la información vive en memoria para que la aplicación
pueda ejecutarse sin dependencias externas. Las fechas se anclan al
27/10/2026 para que el recorrido de demostración sea siempre coherente.
"""

from __future__ import annotations

from datetime import date

HOY = date(2026, 10, 27)
PERIODO = "Ciclo lectivo 2026"
CARRERA = "Tecnicatura en Inteligencia Artificial y Ciencias de Datos"
CARRERA_CORTA = "Tec. en IA y Ciencias de Datos"

MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]
MESES_CORTOS = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
DIAS_CORTOS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

USER = {
    "nombre": "Robinson Boris Cruz",
    "nombre_corto": "Boris",
    "iniciales": "RBC",
    "legajo": "2026-1482",
    "carrera": CARRERA,
    "email": "boris@instituto.edu.ar",
    "telefono": "388 123-4567",
}

NOTICES = [
    {
        "titulo": "Inscripción a finales",
        "detalle": "El período cierra 48 h antes de cada mesa. Revisá las fechas disponibles.",
        "fecha": "Hoy",
        "tipo": "academico",
    },
    {
        "titulo": "Nuevo seguimiento de trámites",
        "detalle": "Ya podés consultar el estado de tus expedientes en línea, sin pasar por la oficina.",
        "fecha": "Ayer",
        "tipo": "institucional",
    },
    {
        "titulo": "Actualizá tus datos de contacto",
        "detalle": "Verificá tu correo y teléfono antes de solicitar un turno administrativo.",
        "fecha": "22 oct",
        "tipo": "recordatorio",
    },
]

EXAMS = [
    {
        "id": "ex-01",
        "materia": "Programación I",
        "carrera": CARRERA,
        "tipo": "Final",
        "fecha": date(2026, 10, 30),
        "hora": "08:00",
        "aula": "Aula 12",
        "sede": "Sede Central",
        "cierre": date(2026, 10, 28),
        "profesor": "Ing. M. Ríos",
    },
    {
        "id": "ex-02",
        "materia": "Lógica",
        "carrera": CARRERA,
        "tipo": "Final",
        "fecha": date(2026, 11, 3),
        "hora": "18:00",
        "aula": "Aula 4",
        "sede": "Sede Norte",
        "cierre": date(2026, 10, 30),
        "profesor": "Lic. S. Vera",
    },
    {
        "id": "ex-03",
        "materia": "Programación II",
        "carrera": CARRERA,
        "tipo": "Final",
        "fecha": date(2026, 11, 6),
        "hora": "09:00",
        "aula": "Aula Magna",
        "sede": "Sede Central",
        "cierre": date(2026, 11, 4),
        "profesor": "Prf. Calisaya David",
    },
    {
        "id": "ex-04",
        "materia": "Ciencias de Datos",
        "carrera": CARRERA,
        "tipo": "Final",
        "fecha": date(2026, 11, 10),
        "hora": "08:00",
        "aula": "Aula 8",
        "sede": "Sede Central",
        "cierre": date(2026, 11, 6),
        "profesor": "Prf. Calisaya David",
    },
    {
        "id": "ex-05",
        "materia": "Ciberseguridad",
        "carrera": CARRERA,
        "tipo": "Final",
        "fecha": date(2026, 11, 11),
        "hora": "14:00",
        "aula": "Aula 3",
        "sede": "Sede Sur",
        "cierre": date(2026, 10, 20),
        "profesor": "Ing. D. Ferreyra",
    },
    {
        "id": "ex-06",
        "materia": "Prácticas Profesionalizantes I",
        "carrera": CARRERA,
        "tipo": "Coloquio",
        "fecha": date(2026, 11, 13),
        "hora": "14:30",
        "aula": "Aula 6",
        "sede": "Sede Norte",
        "cierre": date(2026, 11, 11),
        "profesor": "Lic. A. Quiroga",
    },
    {
        "id": "ex-07",
        "materia": "Inteligencia Artificial",
        "carrera": CARRERA,
        "tipo": "Final",
        "fecha": date(2026, 11, 18),
        "hora": "09:00",
        "aula": "Aula 9",
        "sede": "Sede Central",
        "cierre": date(2026, 11, 16),
        "profesor": "Mg. L. Bustos",
    },
    {
        "id": "ex-08",
        "materia": "Machine Learning",
        "carrera": CARRERA,
        "tipo": "Final",
        "fecha": date(2026, 11, 24),
        "hora": "17:30",
        "aula": "Aula 2",
        "sede": "Sede Sur",
        "cierre": date(2026, 10, 29),
        "profesor": "Dra. V. Aguirre",
    },
    {
        "id": "ex-09",
        "materia": "Prácticas Profesionalizantes II",
        "carrera": CARRERA,
        "tipo": "Coloquio",
        "fecha": date(2026, 11, 27),
        "hora": "08:30",
        "aula": "Aula Magna",
        "sede": "Sede Central",
        "cierre": date(2026, 11, 25),
        "profesor": "Ing. R. Sosa",
    },
    {
        "id": "ex-10",
        "materia": "Programación III",
        "carrera": CARRERA,
        "tipo": "Final",
        "fecha": date(2026, 12, 2),
        "hora": "10:00",
        "aula": "Aula 5",
        "sede": "Sede Central",
        "cierre": date(2026, 11, 30),
        "profesor": "Lic. N. Herrera",
    },
    {
        "id": "ex-11",
        "materia": "Prácticas Profesionalizantes III",
        "carrera": CARRERA,
        "tipo": "Coloquio",
        "fecha": date(2026, 12, 4),
        "hora": "15:00",
        "aula": "Aula 7",
        "sede": "Sede Norte",
        "cierre": date(2026, 12, 2),
        "profesor": "Mg. T. Molina",
    },
    {
        "id": "ex-12",
        "materia": "Base de Datos",
        "carrera": CARRERA,
        "tipo": "Final",
        "fecha": date(2026, 12, 9),
        "hora": "08:30",
        "aula": "Aula 10",
        "sede": "Sede Central",
        "cierre": date(2026, 12, 4),
        "profesor": "Ing. F. Castro",
    },
]

MATERIAS = ["Todas las materias"] + sorted({e["materia"] for e in EXAMS})

ESTADOS_EXAMEN = {
    "abierta": ("Inscripción abierta", "success"),
    "cierra_pronto": ("Cierra pronto", "warning"),
    "cerrada": ("Inscripción cerrada", "neutral"),
    "inscripto": ("Inscripto", "success"),
}

PROCEDURES = [
    {
        "id": "TR-2026-0148",
        "tipo": "legalizacion",
        "titulo": "Legalización de título secundario",
        "estado": "en_proceso",
        "progreso": 65,
        "actualizado": "22/10/2026 · 14:32",
        "iniciado": "12/10/2026",
        "dependencia": "Secretaría Académica",
        "pasos": [
            {
                "titulo": "Solicitud recibida",
                "fecha": "12/10/2026 · 10:14",
                "estado": "completado",
                "detalle": "Registramos la solicitud y el comprobante de pago.",
            },
            {
                "titulo": "Documentación validada",
                "fecha": "16/10/2026 · 09:40",
                "estado": "completado",
                "detalle": "DNI y partida de nacimiento verificados.",
            },
            {
                "titulo": "Revisión de Secretaría Académica",
                "fecha": "En curso",
                "estado": "en_proceso",
                "detalle": "Estamos verificando la autenticidad del título.",
            },
            {
                "titulo": "Firma y emisión",
                "fecha": "Estimado 05/11/2026",
                "estado": "pendiente",
                "detalle": "Podrás retirar el documento en Sede Central.",
            },
        ],
        "nota": None,
    },
    {
        "id": "TR-2026-0131",
        "tipo": "constancia",
        "titulo": "Constancia de alumno regular",
        "estado": "aprobado",
        "progreso": 100,
        "actualizado": "20/10/2026 · 11:05",
        "iniciado": "18/10/2026",
        "dependencia": "Departamento de Alumnado",
        "pasos": [
            {
                "titulo": "Solicitud recibida",
                "fecha": "18/10/2026 · 08:52",
                "estado": "completado",
                "detalle": "La solicitud ingresó al circuito de Alumnado.",
            },
            {
                "titulo": "Verificación académica",
                "fecha": "19/10/2026 · 15:10",
                "estado": "completado",
                "detalle": "Confirmamos tu condición de alumno regular.",
            },
            {
                "titulo": "Documento emitido",
                "fecha": "20/10/2026 · 11:05",
                "estado": "completado",
                "detalle": "La constancia está disponible para descargar.",
            },
        ],
        "nota": None,
    },
    {
        "id": "TR-2026-0120",
        "tipo": "equivalencia",
        "titulo": "Equivalencia de materias",
        "estado": "observado",
        "progreso": 40,
        "actualizado": "21/10/2026 · 16:20",
        "iniciado": "09/10/2026",
        "dependencia": "Comisión de Equivalencias",
        "pasos": [
            {
                "titulo": "Solicitud recibida",
                "fecha": "09/10/2026 · 11:28",
                "estado": "completado",
                "detalle": "Recibimos el formulario y los programas adjuntos.",
            },
            {
                "titulo": "Revisión de documentación",
                "fecha": "15/10/2026 · 10:00",
                "estado": "completado",
                "detalle": "La comisión revisó los antecedentes presentados.",
            },
            {
                "titulo": "Subsanar observación",
                "fecha": "Acción requerida",
                "estado": "en_proceso",
                "detalle": "Falta el programa analítico de Estadística II.",
            },
            {
                "titulo": "Resolución final",
                "fecha": "Pendiente",
                "estado": "pendiente",
                "detalle": "Se emitirá una vez completa la documentación.",
            },
        ],
        "nota": (
            "La Comisión observó la documentación. Adjuntá el programa analítico "
            "de «Estadística II» para continuar con el trámite."
        ),
    },
]

ESTADOS_TRAMITE = {
    "en_proceso": ("En proceso", "warning"),
    "aprobado": ("Aprobado", "success"),
    "observado": ("Requiere acción", "danger"),
}

APPOINTMENT_TYPES = [
    {
        "key": "legalizacion",
        "titulo": "Legalización de título",
        "descripcion": "Título secundario o terciario",
        "duracion": "20 min",
    },
    {
        "key": "constancia",
        "titulo": "Constancia de alumno regular",
        "descripcion": "Para trámites, becas o viajes",
        "duracion": "10 min",
    },
    {
        "key": "equivalencia",
        "titulo": "Equivalencia de materias",
        "descripcion": "Revisión de programas analíticos",
        "duracion": "30 min",
    },
    {
        "key": "certificado",
        "titulo": "Certificado de estudios",
        "descripcion": "Analítico parcial o completo",
        "duracion": "15 min",
    },
]

SEDES = [
    "Sede Central · Av. Rivadavia 1850",
    "Sede Norte · Av. Cabildo 2200",
    "Sede Sur · Av. Directorio 980",
]

APPOINTMENT_DATES = [
    date(2026, 10, 29),
    date(2026, 10, 30),
    date(2026, 11, 2),
    date(2026, 11, 3),
    date(2026, 11, 4),
]

TIME_SLOTS = ["09:00", "09:30", "10:00", "11:00", "14:00", "14:30", "15:30", "16:30"]

UNAVAILABLE_SLOTS = {
    "2026-10-29": {"10:00", "14:30"},
    "2026-10-30": {"09:30", "15:30"},
    "2026-11-02": {"09:00", "11:00", "14:00"},
    "2026-11-03": {"16:30"},
    "2026-11-04": {"09:30", "10:00", "14:30", "15:30"},
}

DEFAULT_CONFIRMED = {
    "code": "TUR-2026-0287",
    "tipo": "Constancia de alumno regular",
    "fecha": "Vie 30 oct",
    "fecha_larga": "viernes 30 de octubre",
    "hora": "11:00",
    "sede": "Sede Central",
    "detalle_sede": "Av. Rivadavia 1850",
}


def new_appointment_draft() -> dict:
    """Borrador limpio del asistente de turnos."""
    return {
        "step": 1,
        "tipo": None,
        "sede": None,
        "motivo": "",
        "fecha": None,
        "hora": None,
        "nombre": USER["nombre"],
        "legajo": USER["legajo"],
        "email": USER["email"],
        "telefono": USER["telefono"],
        "recordatorio": True,
        "error": None,
        "confirmed_code": None,
    }


def fmt_fecha_larga(d: date) -> str:
    return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]}"


def fmt_fecha_media(d: date) -> str:
    return f"{DIAS_CORTOS[d.weekday()]} {d.day} {MESES_CORTOS[d.month - 1]}"


def fmt_fecha_numerica(d: date) -> str:
    return f"{d.day:02d}/{d.month:02d}/{d.year}"


def fmt_fecha_chip(d: date) -> str:
    return f"{DIAS_CORTOS[d.weekday()]} {d.day}"


def iso(d: date) -> str:
    return d.isoformat()


def exam_status(exam: dict, inscriptions=()) -> str:
    if exam["id"] in inscriptions:
        return "inscripto"
    if exam["cierre"] < HOY:
        return "cerrada"
    if (exam["cierre"] - HOY).days <= 3:
        return "cierra_pronto"
    return "abierta"


def exam_is_open(exam: dict, inscriptions=()) -> bool:
    return exam_status(exam, inscriptions) in ("abierta", "cierra_pronto")


def open_exams(inscriptions=()) -> list[dict]:
    return [e for e in EXAMS if exam_is_open(e, inscriptions)]


def procedure_by_id(proc_id: str):
    return next((p for p in PROCEDURES if p["id"] == proc_id), None)


def appointment_type(key: str):
    return next((t for t in APPOINTMENT_TYPES if t["key"] == key), None)


def slots_for(day_iso: str) -> list[tuple[str, bool]]:
    busy = UNAVAILABLE_SLOTS.get(day_iso, set())
    return [(slot, slot not in busy) for slot in TIME_SLOTS]
