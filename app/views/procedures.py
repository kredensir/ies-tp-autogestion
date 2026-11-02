"""Vista de consulta y seguimiento de trámites administrativos."""

from __future__ import annotations

import flet as ft

from app import components as ui
from app import data
from app.theme import P


PROC_ICONS = {
    "legalizacion": ft.Icons.SCHOOL_OUTLINED,
    "constancia": ft.Icons.DESCRIPTION_ROUNDED,
    "equivalencia": ft.Icons.TASK_ALT_ROUNDED,
}

PROC_TIPO_TURNO = {
    "legalizacion": "legalizacion",
    "constancia": "constancia",
    "equivalencia": "equivalencia",
}


def _tone_color(tone: str) -> str:
    return {"success": P.ACCENT, "warning": P.WARN, "danger": P.DANGER}.get(tone, P.ACCENT)


def _list_item(proc, app) -> ft.Container:
    selected = proc["id"] == app.state.procedure_id
    label, tone = data.ESTADOS_TRAMITE[proc["estado"]]
    color = _tone_color(tone)

    return ui.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ui.icon_tile(
                            PROC_ICONS.get(proc["tipo"], ft.Icons.DESCRIPTION_ROUNDED),
                            bgcolor=P.ACCENT_SOFT if not selected else P.SURFACE,
                            color=P.ACCENT,
                            size=38,
                            icon_size=18,
                        ),
                        ft.Column(
                            [
                                ui.text(
                                    proc["titulo"],
                                    13,
                                    P.INK,
                                    ft.FontWeight.W_600,
                                    max_lines=2,
                                ),
                                ui.text(proc["id"], 11, P.INK_3, ft.FontWeight.W_500),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ui.badge(label, tone),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(height=2),
                ft.Row(
                    [
                        ft.Container(
                            content=ui.progress(
                                proc["progreso"] / 100,
                                color=color,
                                bgcolor=P.LINE if not selected else P.WHITE,
                                height=5,
                            ),
                            expand=True,
                        ),
                        ui.text(f"{proc['progreso']}%", 11, color, ft.FontWeight.W_600),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ui.text(f"Actualizado {proc['actualizado']}", 10.5, P.INK_3),
            ],
            spacing=8,
        ),
        bgcolor=P.ACCENT_SOFT if selected else P.SURFACE,
        border_color=P.ACCENT_LINE if selected else P.LINE,
        border_width=1.5 if selected else 1,
        padding=16,
        on_click=lambda e, pid=proc["id"]: _select(app, pid),
        hover=True,
    )


def _select(app, proc_id: str):
    app.state.procedure_id = proc_id
    app.rebuild_view()


def _meta(label, value, col=None) -> ft.Container:
    return ft.Container(
        col=col,
        content=ft.Column(
            [
                ui.text(label, 10.5, P.INK_3, ft.FontWeight.W_500),
                ui.text(value, 12.5, P.INK, ft.FontWeight.W_500),
            ],
            spacing=2,
        ),
    )


def build(app) -> ft.Control:
    state = app.state
    proc = data.procedure_by_id(state.procedure_id) or data.PROCEDURES[0]
    label, tone = data.ESTADOS_TRAMITE[proc["estado"]]
    tone_color = _tone_color(tone)

    def consultar(e=None):
        query = (search.value or "").strip().upper()
        if not query:
            search.error = "Ingresá un número de trámite."
            search.update()
            app.toast("Ingresá un número para consultar.", tone="warning")
            return
        match = next((p for p in data.PROCEDURES if query in p["id"].upper()), None)
        if match is None:
            search.error = "No encontramos un trámite con ese número."
            search.update()
            app.toast("No encontramos el trámite indicado.", tone="danger")
            return
        state.procedure_id = match["id"]
        app.rebuild_view()
        app.toast(f"Trámite {match['id']} encontrado.", tone="success")

    search = ui.field(
        "Número de trámite",
        hint="Ej.: TR-2026-0148",
        prefix_icon=ft.Icons.CONFIRMATION_NUMBER_ROUNDED,
        on_submit=consultar,
    )

    search_card = ui.card(
        ft.Column(
            [
                ft.Row(
                    [
                        search,
                        ui.primary_button(
                            "Consultar",
                            consultar,
                            icon=ft.Icons.SEARCH_ROUNDED,
                            compact=True,
                            width=118,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ui.text(
                    "También podés seleccionar uno de tus trámites recientes.",
                    11.5,
                    P.INK_3,
                ),
            ],
            spacing=8,
        ),
        padding=18,
    )

    # --- Panel de detalle ---------------------------------------------------
    detalle = ui.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ui.icon_tile(
                            PROC_ICONS.get(proc["tipo"], ft.Icons.DESCRIPTION_ROUNDED),
                            size=46,
                            icon_size=22,
                        ),
                        ft.Column(
                            [
                                ui.text(proc["titulo"], 18, P.INK, ft.FontWeight.W_600, max_lines=2),
                                ft.Row(
                                    [
                                        ui.text(proc["id"], 11.5, P.INK_3, ft.FontWeight.W_500),
                                        ui.text("·", 11.5, P.INK_3),
                                        ui.text(proc["dependencia"], 11.5, P.INK_3),
                                    ],
                                    spacing=5,
                                    wrap=True,
                                ),
                            ],
                            spacing=3,
                            expand=True,
                        ),
                        ui.badge(label, tone),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(height=2),
                ui.divider(),
                ft.Container(height=6),
                ft.Row(
                    [
                        ui.text("Progreso del trámite", 12, P.INK_2, ft.FontWeight.W_500, expand=True),
                        ui.text(f"{proc['progreso']}%", 12.5, tone_color, ft.FontWeight.W_600),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ui.progress(proc["progreso"] / 100, color=tone_color),
                ft.Container(height=4),
                ft.ResponsiveRow(
                    [
                        _meta("Dependencia", proc["dependencia"], col={"xs": 6, "sm": 3}),
                        _meta("Iniciado", proc["iniciado"], col={"xs": 6, "sm": 3}),
                        _meta(
                            "Última actualización",
                            proc["actualizado"],
                            col={"xs": 6, "sm": 3},
                        ),
                        _meta("Estado", label, col={"xs": 6, "sm": 3}),
                    ],
                    spacing=12,
                    run_spacing=12,
                ),
                ft.Container(height=2),
                ui.divider(),
                ft.Container(height=6),
                ui.section_header("Seguimiento", "Historial del expediente"),
                ft.Container(height=8),
                ui.timeline(proc["pasos"]),
                *(
                    [
                        ft.Container(height=4),
                        ui.notice(
                            proc["nota"],
                            tone="danger",
                            icon=ft.Icons.ERROR_OUTLINE_ROUNDED,
                        ),
                    ]
                    if proc.get("nota")
                    else []
                ),
                ft.Container(height=4),
                ft.Row(
                    [
                        ui.secondary_button(
                            "Enviar comprobante",
                            lambda e: app.toast(
                                "Enviamos el comprobante a tu correo institucional.",
                                tone="success",
                            ),
                            icon=ft.Icons.MAIL_OUTLINE_ROUNDED,
                            compact=True,
                        ),
                        ui.primary_button(
                            "Solicitar turno",
                            lambda e: _turno_for(app, proc),
                            icon=ft.Icons.ADD_ROUNDED,
                            compact=True,
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        ),
        padding=24,
    )

    lista = ui.card(
        ft.Column(
            [
                ui.section_header(
                    "Mis trámites",
                    f"{len(data.PROCEDURES)} expedientes recientes",
                ),
                ft.Container(height=4),
                ft.Column(
                    [_list_item(p, app) for p in data.PROCEDURES],
                    spacing=10,
                ),
                ft.Container(height=2),
                ui.notice(
                    "Los expedientes se actualizan cada 24 h.",
                    tone="neutral",
                    icon=ft.Icons.UPDATE_ROUNDED,
                ),
            ],
            spacing=8,
        ),
        padding=16,
    )

    contenido = ft.ResponsiveRow(
        [
            ft.Container(lista, col={"xs": 12, "md": 12, "lg": 5}),
            ft.Container(detalle, col={"xs": 12, "md": 12, "lg": 7}),
        ],
        spacing=14,
        run_spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    header = ui.page_header(
        "Estado de trámites",
        "Seguí cada expediente y conocé el próximo paso sin acercarte a la oficina.",
        eyebrow_text="Autogestión",
        actions=ui.badge("Actualizado hace 2 h", "success", icon=ft.Icons.CHECK_CIRCLE_ROUNDED),
    )

    return ft.Column(
        [header, search_card, contenido],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def _turno_for(app, proc):
    app.state.appointment["tipo"] = PROC_TIPO_TURNO.get(proc["tipo"])
    app.state.appointment["step"] = 1
    app.state.appointment["error"] = None
    app.state.appointment["confirmed_code"] = None
    app.navigate("appointments")
