"""Vista de fechas de examen con búsqueda y filtros combinables."""

from __future__ import annotations

import flet as ft

from app import components as ui
from app import data
from app.theme import P


def _filtered_exams(state) -> list[dict]:
    filters = state.exam_filters
    query = filters["query"].strip().lower()
    items = []
    for exam in data.EXAMS:
        if filters["materia"] != data.MATERIAS[0] and exam["materia"] != filters["materia"]:
            continue
        if filters["estado"] != "todos":
            status = data.exam_status(exam, state.inscriptions)
            if filters["estado"] == "abiertas" and status not in ("abierta", "cierra_pronto"):
                continue
            if filters["estado"] == "cerradas" and status != "cerrada":
                continue
        if query:
            haystack = " ".join(
                [
                    exam["materia"],
                    exam["carrera"],
                    exam["sede"],
                    exam["profesor"],
                    exam["aula"],
                ]
            ).lower()
            if query not in haystack:
                continue
        items.append(exam)
    return sorted(items, key=lambda e: (e["fecha"], e["hora"]))


def _exam_card(exam, app) -> ft.Container:
    state = app.state
    status = data.exam_status(exam, state.inscriptions)
    label, tone = data.ESTADOS_EXAMEN[status]

    def confirm_inscription(e):
        def close(_):
            app.page.pop_dialog()

        def confirm(_):
            state.inscriptions.add(exam["id"])
            app.page.pop_dialog()
            app.rebuild_view()
            app.toast(f"Inscripción confirmada: {exam['materia']}.", tone="success")

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=P.SURFACE,
            shape=ft.RoundedRectangleBorder(radius=24),
            content_padding=ft.Padding.all(24),
            title=ui.text("Confirmar inscripción", 20, P.INK, ft.FontWeight.W_600),
            content=ft.Container(
                width=420,
                content=ft.Column(
                    [
                        ui.text(
                            "Vas a inscribirte a la siguiente mesa de examen:",
                            13,
                            P.INK_2,
                        ),
                        ft.Container(height=4),
                        ui.card(
                            ft.Column(
                                [
                                    ui.text(exam["materia"], 15, P.INK, ft.FontWeight.W_600),
                                    ui.text(
                                        f"{exam['tipo']} · {exam['profesor']}",
                                        12,
                                        P.INK_2,
                                    ),
                                    ft.Container(height=4),
                                    ui.info_pill(
                                        ft.Icons.SCHEDULE_ROUNDED,
                                        f"{data.fmt_fecha_media(exam['fecha'])} · {exam['hora']} h",
                                    ),
                                    ui.info_pill(
                                        ft.Icons.LOCATION_ON_OUTLINED,
                                        f"{exam['aula']} · {exam['sede']}",
                                    ),
                                ],
                                spacing=5,
                            ),
                            padding=16,
                            bgcolor=P.SOFT,
                            border_width=0,
                            radius=16,
                        ),
                        ui.notice(
                            f"La inscripción cierra el {data.fmt_fecha_numerica(exam['cierre'])}.",
                            tone="warning",
                            icon=ft.Icons.EVENT_BUSY_ROUNDED,
                        ),
                    ],
                    spacing=12,
                    tight=True,
                ),
            ),
            actions=[
                ui.ghost_button("Cancelar", close),
                ui.primary_button(
                    "Confirmar inscripción",
                    confirm,
                    icon=ft.Icons.CHECK_ROUNDED,
                    compact=True,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        app.page.show_dialog(dialog)

    if status == "inscripto":
        action = ui.secondary_button(
            "Inscripto",
            icon=ft.Icons.CHECK_ROUNDED,
            disabled=True,
            compact=True,
            width=124,
        )
    elif status == "cerrada":
        action = ui.secondary_button("Cerrada", disabled=True, compact=True, width=124)
    else:
        action = ui.secondary_button(
            "Inscribirme",
            confirm_inscription,
            icon=ft.Icons.ADD_ROUNDED,
            compact=True,
            width=124,
        )

    meta = ft.Row(
        [
            ui.info_pill(
                ft.Icons.LOCATION_ON_OUTLINED,
                f"{exam['sede']} · {exam['aula']}",
                color=P.INK_2,
            ),
            ui.info_pill(
                ft.Icons.SCHEDULE_ROUNDED,
                f"{exam['hora']} h",
                color=P.INK_2,
            ),
            ui.info_pill(
                ft.Icons.EVENT_BUSY_ROUNDED,
                f"Cierra {data.fmt_fecha_media(exam['cierre'])}",
                color=P.INK_3,
                icon_color=P.INK_3,
            ),
        ],
        spacing=8,
        run_spacing=6,
        wrap=True,
    )

    return ui.card(
        ft.Row(
            [
                ft.Container(
                    width=58,
                    height=64,
                    bgcolor=P.SOFT if status != "inscripto" else P.ACCENT_SOFT,
                    border_radius=15,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        [
                            ui.text(
                                f"{exam['fecha'].day:02d}",
                                20,
                                P.INK if status != "inscripto" else P.ACCENT,
                                ft.FontWeight.W_600,
                            ),
                            ui.text(
                                data.MESES_CORTOS[exam["fecha"].month - 1],
                                9,
                                P.INK_2,
                                ft.FontWeight.W_600,
                            ),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
                ft.Column(
                    [
                        ft.Row(
                            [
                                ui.text(
                                    exam["materia"],
                                    15,
                                    P.INK,
                                    ft.FontWeight.W_600,
                                    expand=True,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ui.badge(label, tone),
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ui.text(
                            f"{exam['tipo']} · {exam['profesor']}",
                            11.5,
                            P.INK_2,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        meta,
                    ],
                    spacing=6,
                    expand=True,
                ),
                ft.Container(content=action, alignment=ft.Alignment.CENTER_RIGHT),
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=18,
    )


def build(app) -> ft.Control:
    state = app.state
    filters = state.exam_filters

    results = ft.Column(spacing=10)
    count_text = ui.text("", 12, P.INK_2, ft.FontWeight.W_500)

    def refresh(update=True):
        exams = _filtered_exams(state)
        count_text.value = (
            f"{len(exams)} fecha{'s' if len(exams) != 1 else ''} encontrada"
            f"{'s' if len(exams) != 1 else ''}"
        )
        if exams:
            results.controls = [_exam_card(exam, app) for exam in exams]
        else:
            results.controls = [
                ui.card(
                    ui.empty_state(
                        "Sin resultados",
                        "Probá con otra búsqueda o quitá los filtros para ver todas las mesas.",
                        action="Limpiar filtros",
                        on_action=lambda e: reset_filters(),
                    ),
                    padding=0,
                )
            ]
        if update:
            results.update()
            count_text.update()

    def reset_filters():
        state.exam_filters.update(
            {
                "query": "",
                "materia": data.MATERIAS[0],
                "estado": "todos",
            }
        )
        app.rebuild_view()

    def on_search(e):
        state.exam_filters["query"] = e.control.value
        refresh()

    def on_materia(value):
        state.exam_filters["materia"] = value
        app.rebuild_view()

    def on_status(value):
        state.exam_filters["estado"] = value
        app.rebuild_view()

    search = ui.field(
        "Buscar",
        value=filters["query"],
        hint="Materia, sede o docente",
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        on_change=on_search,
        col={"xs": 12, "md": 6},
    )

    materia = ui.dropdown_field(
        "Materia",
        data.MATERIAS,
        value=filters["materia"],
        on_select=on_materia,
        col={"xs": 12, "md": 6},
    )

    filters_card = ui.card(
        ft.Column(
            [
                ft.ResponsiveRow([search, materia], spacing=12, run_spacing=12),
                ft.Row(
                    [
                        ui.segmented(
                            [
                                ("todos", "Todas"),
                                ("abiertas", "Abiertas"),
                                ("cerradas", "Cerradas"),
                            ],
                            filters["estado"],
                            on_status,
                        ),
                        ft.Container(expand=True),
                        count_text,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
            ],
            spacing=14,
        ),
        padding=18,
    )

    header = ui.page_header(
        "Fechas de examen",
        f"Mesas de la {data.CARRERA}. Asegurá tu lugar antes del cierre.",
        eyebrow_text="Calendario académico",
        actions=ui.badge("Turno noviembre · diciembre", "accent", icon=ft.Icons.EVENT_AVAILABLE_ROUNDED),
    )

    refresh(update=False)

    return ft.Column(
        [header, filters_card, results],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
