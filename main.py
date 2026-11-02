"""Portal de autogestión de turnos y consultas institucionales.

Ejecutar con:
    python main.py
"""

from __future__ import annotations

import flet as ft

from app import components as ui
from app import data
from app.state import AppState
from app.theme import FONT, P, RADIUS_LG, RADIUS_PILL
from app.views import appointments, exams, home, procedures


ROUTES = {
    "home": ("Inicio", ft.Icons.HOME_ROUNDED, home.build),
    "exams": ("Fechas de examen", ft.Icons.CALENDAR_MONTH_ROUNDED, exams.build),
    "procedures": ("Estado de trámites", ft.Icons.DESCRIPTION_ROUNDED, procedures.build),
    "appointments": ("Solicitar turno", ft.Icons.ADD_CIRCLE_OUTLINE_ROUNDED, appointments.build),
}

ROUTE_ORDER = ["home", "exams", "procedures", "appointments"]


class PortalApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state = AppState()
        self.nav_refs = {}
        self.topbar_title = None
        self._snack = None

        self.content_host = ft.Container(
            expand=True,
            padding=ft.Padding.only(left=36, right=36, top=26, bottom=36),
            alignment=ft.Alignment.TOP_LEFT,
        )
        self.sidebar = self._build_sidebar()
        self.topbar = self._build_topbar()
        self.mobile_nav = self._build_mobile_nav()

        self.content_host.content = ROUTES[self.state.route][2](self)

        main_row = ft.Row(
            [
                self.sidebar,
                ft.Column(
                    [self.topbar, self.content_host],
                    spacing=0,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

        self.shell = ft.Column(
            [main_row, self.mobile_nav],
            spacing=0,
            expand=True,
        )

        page.add(self.shell)
        page.update()
        self._on_resize()

    # ------------------------------------------------------------------
    # Navegación y avisos
    # ------------------------------------------------------------------
    def navigate(self, route: str):
        if route not in ROUTES:
            return
        self.state.route = route
        self.content_host.content = ROUTES[route][2](self)
        self._refresh_nav()
        if self.topbar_title is not None:
            self.topbar_title.value = ROUTES[route][0]
        self.page.update()

    def rebuild_view(self):
        self.content_host.content = ROUTES[self.state.route][2](self)
        self.content_host.update()

    def _refresh_nav(self):
        for route, (container, icon, label) in self.nav_refs.items():
            active = route == self.state.route
            container.bgcolor = P.ACCENT_SOFT if active else None
            icon.color = P.ACCENT if active else P.INK_2
            label.color = P.INK if active else P.INK_2
            label.weight = ft.FontWeight.W_600 if active else ft.FontWeight.W_500
            try:
                container.update()
            except Exception:
                pass
        try:
            self.mobile_nav.selected_index = ROUTE_ORDER.index(self.state.route)
            self.mobile_nav.update()
        except Exception:
            pass

    def toast(self, message: str, tone: str = "neutral"):
        colors = {
            "neutral": P.INK,
            "success": P.ACCENT,
            "warning": P.WARN,
            "danger": P.DANGER,
        }
        icons = {
            "neutral": ft.Icons.INFO_OUTLINE_ROUNDED,
            "success": ft.Icons.CHECK_CIRCLE_ROUNDED,
            "warning": ft.Icons.ERROR_OUTLINE_ROUNDED,
            "danger": ft.Icons.ERROR_OUTLINE_ROUNDED,
        }
        snack = ft.SnackBar(
            content=ft.Row(
                [
                    ft.Icon(icons.get(tone, icons["neutral"]), size=18, color=P.WHITE),
                    ui.text(message, 13, P.WHITE, ft.FontWeight.W_500, expand=True),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=colors.get(tone, P.INK),
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.Margin.only(left=24, right=24, bottom=24),
            shape=ft.RoundedRectangleBorder(radius=14),
            duration=3200,
            elevation=0,
        )
        if self._snack is not None and getattr(self._snack, "open", False):
            self.page.pop_dialog()
        self._snack = snack
        self.page.show_dialog(snack)

    def open_notices(self):
        def close(e=None):
            self.page.pop_dialog()

        rows = []
        for index, notice in enumerate(data.NOTICES):
            rows.append(
                ft.Row(
                    [
                        ui.icon_tile(
                            ft.Icons.CAMPAIGN_ROUNDED
                            if notice["tipo"] == "institucional"
                            else ft.Icons.EVENT_NOTE_ROUNDED,
                            size=36,
                            icon_size=18,
                            bgcolor=P.SOFT,
                            color=P.INK_2,
                        ),
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ui.text(
                                            notice["titulo"],
                                            12.5,
                                            P.INK,
                                            ft.FontWeight.W_600,
                                            expand=True,
                                        ),
                                        ui.text(notice["fecha"], 10.5, P.INK_3),
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ui.text(notice["detalle"], 11.5, P.INK_2, max_lines=2),
                            ],
                            spacing=3,
                            expand=True,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )
            if index < len(data.NOTICES) - 1:
                rows.append(ui.divider())

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=P.SURFACE,
            shape=ft.RoundedRectangleBorder(radius=24),
            content_padding=ft.Padding.all(24),
            title=ui.text("Avisos institucionales", 20, P.INK, ft.FontWeight.W_600),
            content=ft.Container(
                width=450,
                content=ft.Column(rows, spacing=12, tight=True),
            ),
            actions=[ui.primary_button("Entendido", close, compact=True)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.show_dialog(dialog)

    def open_help(self):
        def close(e=None):
            self.page.pop_dialog()

        def go_turno(e=None):
            self.page.pop_dialog()
            self.navigate("appointments")

        pasos = [
            ("1", "Elegí el trámite", "Seleccioná el tipo de gestión y la sede más cercana."),
            ("2", "Reservá día y horario", "Los turnos se habilitan con 5 días de anticipación."),
            ("3", "Presentate con tu DNI", "Llegá 10 minutos antes y traé el comprobante del turno."),
        ]
        items = []
        for numero, titulo, detalle in pasos:
            items.append(
                ft.Row(
                    [
                        ft.Container(
                            width=28,
                            height=28,
                            bgcolor=P.ACCENT_SOFT,
                            border_radius=RADIUS_PILL,
                            alignment=ft.Alignment.CENTER,
                            content=ui.text(numero, 12, P.ACCENT, ft.FontWeight.W_600),
                        ),
                        ft.Column(
                            [
                                ui.text(titulo, 13, P.INK, ft.FontWeight.W_600),
                                ui.text(detalle, 11.5, P.INK_2, max_lines=2),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=P.SURFACE,
            shape=ft.RoundedRectangleBorder(radius=24),
            content_padding=ft.Padding.all(24),
            title=ui.text("Guía de trámites", 20, P.INK, ft.FontWeight.W_600),
            content=ft.Container(
                width=470,
                content=ft.Column(
                    [
                        ui.text(
                            "La mayoría de las gestiones se resuelven en una sola visita.",
                            12.5,
                            P.INK_2,
                        ),
                        ft.Container(height=2),
                        *items,
                        ui.notice(
                            "Los requisitos cambian según el trámite. Consultá el detalle antes de reservar.",
                            tone="warning",
                            icon=ft.Icons.INFO_OUTLINE_ROUNDED,
                        ),
                    ],
                    spacing=14,
                    tight=True,
                ),
            ),
            actions=[
                ui.ghost_button("Cerrar", close),
                ui.primary_button("Solicitar turno", go_turno, compact=True),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.show_dialog(dialog)

    # ------------------------------------------------------------------
    # Armado del shell
    # ------------------------------------------------------------------
    def _build_sidebar(self) -> ft.Container:
        brand = ft.Row(
            [
                ft.Container(
                    width=40,
                    height=40,
                    bgcolor=P.INK,
                    border_radius=13,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, size=21, color=P.WHITE),
                ),
                ft.Column(
                    [
                        ui.text("Portal", 15.5, P.INK, ft.FontWeight.W_600),
                        ui.text("Comunidad educativa", 10.5, P.INK_3),
                    ],
                    spacing=0,
                ),
            ],
            spacing=11,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        nav_items = []
        for route in ROUTE_ORDER:
            label_text, icon_data, _ = ROUTES[route]
            active = route == self.state.route
            icon = ft.Icon(icon_data, size=19, color=P.ACCENT if active else P.INK_2)
            label = ui.text(
                label_text,
                13,
                P.INK if active else P.INK_2,
                ft.FontWeight.W_600 if active else ft.FontWeight.W_500,
            )
            container = ft.Container(
                content=ft.Row([icon, label], spacing=11, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                height=44,
                padding=ft.Padding.symmetric(horizontal=12),
                border_radius=12,
                bgcolor=P.ACCENT_SOFT if active else None,
                ink=True,
                ink_color=P.SOFT,
                on_click=lambda e, r=route: self.navigate(r),
            )
            self.nav_refs[route] = (container, icon, label)
            nav_items.append(container)

        help_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.HELP_OUTLINE_ROUNDED, size=18, color=P.SAND_DEEP),
                            ui.text("¿Necesitás ayuda?", 12.5, P.INK, ft.FontWeight.W_600),
                        ],
                        spacing=7,
                    ),
                    ui.text(
                        "Revisá requisitos y tiempos antes de reservar.",
                        11,
                        P.INK_2,
                        max_lines=2,
                    ),
                    ft.Row(
                        [
                            ui.text("Ver guía", 12, P.SAND_DEEP, ft.FontWeight.W_600),
                            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=14, color=P.SAND_DEEP),
                        ],
                        spacing=3,
                    ),
                ],
                spacing=5,
            ),
            bgcolor=P.SAND,
            border_radius=RADIUS_LG,
            padding=14,
            ink=True,
            ink_color="#10FFFFFF",
            on_click=lambda e: self.open_help(),
        )

        user = ft.Row(
            [
                ui.avatar(data.USER["iniciales"], size=38),
                ft.Column(
                    [
                        ui.text(data.USER["nombre"], 12, P.INK, ft.FontWeight.W_600, max_lines=1),
                        ui.text(f"Legajo {data.USER['legajo']}", 10.5, P.INK_3, max_lines=1),
                    ],
                    spacing=1,
                    expand=True,
                ),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            width=252,
            bgcolor=P.SIDEBAR,
            border=ft.Border.only(right=ft.BorderSide(1, P.LINE)),
            padding=ft.Padding.symmetric(horizontal=16, vertical=22),
            content=ft.Column(
                [
                    brand,
                    ft.Container(height=26),
                    ui.text("MENÚ", 10, P.INK_3, ft.FontWeight.W_600, style=ft.TextStyle(letter_spacing=1.1)),
                    ft.Container(height=8),
                    ft.Column(nav_items, spacing=4),
                    ft.Container(expand=True),
                    help_card,
                    ft.Container(height=16),
                    ui.divider(),
                    ft.Container(height=14),
                    user,
                ],
                spacing=0,
            ),
        )

    def _build_topbar(self) -> ft.Container:
        self.topbar_title = ui.text(ROUTES[self.state.route][0], 13, P.INK, ft.FontWeight.W_600)

        bell = ft.Stack(
            [
                ui.icon_button(
                    ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                    lambda e: self.open_notices(),
                    tooltip="Avisos institucionales",
                ),
                ft.Container(
                    width=7,
                    height=7,
                    bgcolor=P.DANGER,
                    border_radius=RADIUS_PILL,
                    right=8,
                    top=8,
                ),
            ],
            width=40,
            height=40,
        )

        return ft.Container(
            height=84,
            padding=ft.Padding.symmetric(horizontal=36, vertical=16),
            border=ft.Border.only(bottom=ft.BorderSide(1, P.LINE)),
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ui.text("Portal de autogestión", 10.5, P.INK_3, ft.FontWeight.W_600),
                            self.topbar_title,
                        ],
                        spacing=2,
                    ),
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            ui.badge(data.PERIODO, "neutral", icon=ft.Icons.SCHOOL_OUTLINED),
                            bell,
                            ft.Container(width=4),
                            ft.Container(width=1, height=26, bgcolor=P.LINE),
                            ft.Container(width=4),
                            ui.avatar(data.USER["iniciales"], size=36),
                            ft.Column(
                                [
                                    ui.text(data.USER["nombre"], 12, P.INK, ft.FontWeight.W_600),
                                    ui.text(data.CARRERA_CORTA, 10.5, P.INK_3),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def _build_mobile_nav(self) -> ft.NavigationBar:
        destinations = []
        for route in ROUTE_ORDER:
            label_text, icon_data, _ = ROUTES[route]
            destinations.append(
                ft.NavigationBarDestination(
                    icon=icon_data,
                    selected_icon=icon_data,
                    label=label_text,
                )
            )
        return ft.NavigationBar(
            destinations=destinations,
            selected_index=ROUTE_ORDER.index(self.state.route),
            bgcolor=P.SURFACE,
            indicator_color=P.ACCENT_SOFT,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            elevation=0,
            border=ft.Border.only(top=ft.BorderSide(1, P.LINE)),
            on_change=lambda e: self.navigate(ROUTE_ORDER[e.control.selected_index]),
            visible=False,
        )

    def _on_resize(self, e=None):
        width = self.page.width or 1220
        narrow = width < 980
        self.sidebar.visible = not narrow
        self.mobile_nav.visible = narrow
        pad = 20 if narrow else 36
        self.content_host.padding = ft.Padding.only(
            left=pad,
            right=pad,
            top=20 if narrow else 26,
            bottom=24 if narrow else 36,
        )
        self.topbar.padding = ft.Padding.symmetric(horizontal=pad, vertical=16)
        try:
            self.page.update()
        except Exception:
            pass


def main(page: ft.Page):
    page.title = "Portal de autogestión · Comunidad educativa"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = P.BG
    page.padding = 0
    page.spacing = 0
    page.window.width = 1220
    page.window.height = 840
    page.window.min_width = 980
    page.window.min_height = 680
    page.window.resizable = True
    page.theme = ft.Theme(
        color_scheme_seed=P.ACCENT,
        use_material3=True,
        font_family=FONT,
        scaffold_bgcolor=P.BG,
        canvas_color=P.BG,
        divider_color=P.LINE,
        hint_color=P.INK_3,
        splash_color="#142E6B4F",
        hover_color="#0A1C1C1E",
    )
    page.on_resize = lambda e: None

    portal = PortalApp(page)
    page.on_resize = portal._on_resize


if __name__ == "__main__":
    ft.run(main)
