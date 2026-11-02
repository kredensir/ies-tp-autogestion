"""Vista de inicio: resumen personal y accesos rápidos."""

from __future__ import annotations

import flet as ft

from app import components as ui
from app import data
from app.theme import P, RADIUS_PILL, RADIUS_XL


def _stat_card(icon, label, value, meta, *, bgcolor, color, on_click=None, col=None):
    return ui.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ui.icon_tile(icon, bgcolor=bgcolor, color=color, size=38, icon_size=19),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.ARROW_OUTWARD_ROUNDED, size=15, color=P.INK_3)
                        if on_click
                        else ft.Container(),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(expand=True),
                ui.text(label, 11.5, P.INK_2, ft.FontWeight.W_500),
                ui.text(value, 17, P.INK, ft.FontWeight.W_600, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                ui.text(meta, 11.5, P.INK_3, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
            ],
            spacing=3,
            expand=True,
        ),
        padding=18,
        col=col,
        height=164,
        on_click=on_click,
        hover=True,
    )


def _mini_exam_row(exam, on_click):
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    width=48,
                    height=54,
                    bgcolor=P.SOFT,
                    border_radius=12,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        [
                            ui.text(exam["fecha"].day, 17, P.INK, ft.FontWeight.W_600),
                            ui.text(data.MESES_CORTOS[exam["fecha"].month - 1], 9, P.INK_2, ft.FontWeight.W_600),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
                ft.Column(
                    [
                        ui.text(exam["materia"], 13.5, P.INK, ft.FontWeight.W_600, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ui.text(
                            f"{data.fmt_fecha_media(exam['fecha'])} · {exam['hora']} h · {exam['sede']}",
                            11.5,
                            P.INK_2,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, size=18, color=P.INK_3),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(vertical=9, horizontal=4),
        border_radius=12,
        ink=True,
        ink_color=P.SOFT,
        on_click=on_click,
    )


def build(app) -> ft.Control:
    state = app.state
    user = data.USER
    abiertos = data.open_exams(state.inscriptions)
    proximo = abiertos[0] if abiertos else data.EXAMS[-1]
    pendientes = [p for p in data.PROCEDURES if p["estado"] in ("en_proceso", "observado")]
    turno = state.confirmed
    dias = max(0, (proximo["fecha"] - data.HOY).days)

    hoy_texto = f"{data.DIAS[data.HOY.weekday()]} {data.HOY.day} de {data.MESES[data.HOY.month - 1]}"

    header = ui.page_header(
        f"Hola, {user['nombre_corto']}",
        "Este es el resumen de tu actividad académica de hoy.",
        actions=ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, size=15, color=P.INK_2),
                    ui.text(hoy_texto, 12, P.INK_2, ft.FontWeight.W_500),
                ],
                spacing=7,
                tight=True,
            ),
            bgcolor=P.SURFACE,
            border=ft.Border.all(1, P.LINE),
            border_radius=RADIUS_PILL,
            padding=ft.Padding.symmetric(horizontal=14, vertical=9),
        ),
    )

    # --- Tarjeta principal: próximo examen ---------------------------------
    hero_left = ft.Column(
        [
            ft.Row(
                [
                    ft.Container(width=6, height=6, bgcolor=P.ACCENT, border_radius=RADIUS_PILL),
                    ui.eyebrow("Próximo examen"),
                ],
                spacing=7,
                tight=True,
            ),
            ui.text(proximo["materia"], 29, P.INK, ft.FontWeight.W_600, max_lines=2),
            ft.Row(
                [
                    ui.info_pill(
                        ft.Icons.SCHEDULE_ROUNDED,
                        f"{data.fmt_fecha_media(proximo['fecha'])} · {proximo['hora']} h",
                        color=P.INK_2,
                    ),
                    ui.info_pill(
                        ft.Icons.LOCATION_ON_OUTLINED,
                        f"{proximo['aula']} · {proximo['sede']}",
                        color=P.INK_2,
                    ),
                ],
                spacing=8,
                wrap=True,
                run_spacing=8,
            ),
            ui.text(
                f"{proximo['tipo']} · {proximo['profesor']}",
                12,
                P.INK_2,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
            ft.Container(height=2),
            ft.Row(
                [
                    ui.primary_button(
                        "Ver fechas de examen",
                        lambda e: app.navigate("exams"),
                        icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                    ),
                    ui.ghost_button(
                        "Agregar al calendario",
                        lambda e: app.toast("Agregamos el examen a tu calendario."),
                        icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
                    ),
                ],
                spacing=6,
            ),
        ],
        spacing=12,
        expand=True,
    )

    date_card = ft.Container(
        width=138,
        bgcolor="#F9F8F4",
        border=ft.Border.all(1, "#E2DED4"),
        border_radius=RADIUS_XL,
        padding=ft.Padding.symmetric(horizontal=14, vertical=16),
        content=ft.Column(
            [
                ui.text(data.MESES_CORTOS[proximo["fecha"].month - 1], 10.5, P.INK_2, ft.FontWeight.W_600),
                ui.text(f"{proximo['fecha'].day:02d}", 38, P.INK, ft.FontWeight.W_600),
                ui.text(data.DIAS[proximo["fecha"].weekday()], 11, P.INK_2),
                ft.Container(height=8),
                ft.Container(height=1, bgcolor="#E2DED4"),
                ft.Container(height=8),
                ui.text("Faltan", 10.5, P.INK_3),
                ui.text(f"{dias} días", 12.5, P.ACCENT, ft.FontWeight.W_600),
            ],
            spacing=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    hero = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=["#EDE5D8", "#E7EFE8"],
        ),
        border=ft.Border.all(1, "#E1DDD2"),
        border_radius=28,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        padding=ft.Padding.symmetric(horizontal=28, vertical=26),
        content=ft.Row(
            [hero_left, date_card],
            spacing=24,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # --- Indicadores -------------------------------------------------------
    stats = ft.ResponsiveRow(
        [
            _stat_card(
                ft.Icons.EVENT_AVAILABLE_ROUNDED,
                "Próximo turno",
                f"{turno['fecha']} · {turno['hora']}",
                turno["tipo"],
                bgcolor=P.ACCENT_SOFT,
                color=P.ACCENT,
                col={"xs": 12, "sm": 4},
            ),
            _stat_card(
                ft.Icons.PENDING_ACTIONS_ROUNDED,
                "Trámites activos",
                f"{len(pendientes)} en curso",
                "Legalización de título",
                bgcolor=P.WARN_SOFT,
                color=P.WARN,
                on_click=lambda e: app.navigate("procedures"),
                col={"xs": 12, "sm": 4},
            ),
            _stat_card(
                ft.Icons.CALENDAR_MONTH_ROUNDED,
                "Inscripciones abiertas",
                f"{len(abiertos)} mesas",
                "Finales de noviembre y diciembre",
                bgcolor=P.SAND,
                color=P.SAND_DEEP,
                on_click=lambda e: app.navigate("exams"),
                col={"xs": 12, "sm": 4},
            ),
        ],
        spacing=14,
        run_spacing=14,
    )

    # --- Próximas fechas --------------------------------------------------
    fechas_rows = []
    for index, exam in enumerate(abiertos[:3]):
        fechas_rows.append(_mini_exam_row(exam, lambda e: app.navigate("exams")))
        if index < min(len(abiertos), 3) - 1:
            fechas_rows.append(ui.divider())

    proximas = ui.card(
        ft.Column(
            [
                ui.section_header(
                    "Próximas fechas",
                    "Mesas con inscripción habilitada",
                    action="Ver todas",
                    on_action=lambda e: app.navigate("exams"),
                ),
                ft.Container(height=6),
                ui.divider(),
                ft.Column(fechas_rows, spacing=0),
            ],
            spacing=0,
        ),
        padding=20,
        col={"xs": 12, "md": 7},
    )

    # --- Accesos rápidos --------------------------------------------------
    accesos = ui.card(
        ft.Column(
            [
                ui.section_header("Accesos rápidos", "Todo lo que necesitás, en un lugar"),
                ft.Container(height=4),
                ft.ResponsiveRow(
                    [
                        ui.quick_tile(
                            ft.Icons.ADD_CIRCLE_OUTLINE_ROUNDED,
                            "Solicitar turno",
                            "Elegí día y horario",
                            on_click=lambda e: app.navigate("appointments"),
                            col={"xs": 6},
                        ),
                        ui.quick_tile(
                            ft.Icons.DESCRIPTION_ROUNDED,
                            "Consultar trámite",
                            "Seguí tu expediente",
                            on_click=lambda e: app.navigate("procedures"),
                            col={"xs": 6},
                        ),
                        ui.quick_tile(
                            ft.Icons.CALENDAR_MONTH_ROUNDED,
                            "Fechas de examen",
                            "Inscribite a una mesa",
                            on_click=lambda e: app.navigate("exams"),
                            col={"xs": 6},
                        ),
                        ui.quick_tile(
                            ft.Icons.HELP_OUTLINE_ROUNDED,
                            "Guía de trámites",
                            "Requisitos y pasos",
                            on_click=lambda e: app.open_help(),
                            col={"xs": 6},
                        ),
                    ],
                    spacing=10,
                    run_spacing=10,
                ),
            ],
            spacing=0,
        ),
        padding=20,
        col={"xs": 12, "md": 5},
    )

    contenido = ft.ResponsiveRow(
        [proximas, accesos],
        spacing=14,
        run_spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    aviso = ui.notice(
        "Inscripción a finales: el período cierra 48 h antes de cada mesa.",
        tone="warning",
        action="Ver fechas",
        on_action=lambda e: app.navigate("exams"),
    )

    return ft.Column(
        [header, hero, stats, contenido, aviso],
        spacing=22,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
