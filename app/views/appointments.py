"""Asistente de solicitud de turnos administrativos en tres pasos."""

from __future__ import annotations

import random
from datetime import date

import flet as ft

from app import components as ui
from app import data
from app.theme import P, RADIUS_LG, RADIUS_MD, RADIUS_PILL


TYPE_ICONS = {
    "legalizacion": ft.Icons.SCHOOL_OUTLINED,
    "constancia": ft.Icons.DESCRIPTION_ROUNDED,
    "equivalencia": ft.Icons.TASK_ALT_ROUNDED,
    "certificado": ft.Icons.BADGE_OUTLINED,
}

STEP_LABELS = ["Trámite y sede", "Fecha y hora", "Tus datos"]


def _type_card(item, selected, on_click, col=None) -> ft.Container:
    check = ft.Container(
        width=22,
        height=22,
        bgcolor=P.ACCENT if selected else P.SURFACE,
        border=ft.Border.all(1.5, P.ACCENT if selected else P.LINE_STRONG),
        border_radius=RADIUS_PILL,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.CHECK_ROUNDED, size=13, color=P.WHITE) if selected else None,
    )
    return ui.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ui.icon_tile(
                            TYPE_ICONS.get(item["key"], ft.Icons.DESCRIPTION_ROUNDED),
                            bgcolor=P.ACCENT_SOFT if selected else P.SOFT,
                            color=P.ACCENT,
                            size=38,
                            icon_size=18,
                        ),
                        ft.Container(expand=True),
                        check,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(expand=True),
                ui.text(item["titulo"], 13.5, P.INK, ft.FontWeight.W_600, max_lines=2),
                ft.Row(
                    [
                        ui.text(item["descripcion"], 11.5, P.INK_2, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, expand=True),
                        ui.text(item["duracion"], 10.5, P.ACCENT, ft.FontWeight.W_600),
                    ],
                    spacing=6,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=5,
            expand=True,
        ),
        bgcolor=P.ACCENT_SOFT if selected else P.SURFACE,
        border_color=P.ACCENT if selected else P.LINE,
        border_width=2 if selected else 1,
        padding=16,
        height=144,
        col=col,
        on_click=on_click,
        hover=True,
    )


def _date_card(day: date, selected: bool, on_click) -> ft.Container:
    strong = P.WHITE if selected else P.INK
    muted = "#C7D8CE" if selected else P.INK_3
    return ft.Container(
        content=ft.Column(
            [
                ui.text(data.DIAS_CORTOS[day.weekday()], 11, muted, ft.FontWeight.W_500),
                ui.text(f"{day.day:02d}", 22, strong, ft.FontWeight.W_600),
                ui.text(data.MESES_CORTOS[day.month - 1], 9.5, muted, ft.FontWeight.W_600),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=P.INK if selected else P.SURFACE,
        border=ft.Border.all(1, P.INK if selected else P.LINE),
        border_radius=RADIUS_MD,
        padding=ft.Padding.symmetric(vertical=10, horizontal=6),
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        ink=True,
        ink_color=P.SOFT,
        expand=True,
        tooltip=f"{data.fmt_fecha_larga(day)}",
    )


def _slot_chip(slot: str, available: bool, selected: bool, on_click) -> ft.Container:
    if selected:
        bgcolor = P.INK
        color = P.WHITE
        border = ft.Border.all(1, P.INK)
    elif available:
        bgcolor = P.SURFACE
        color = P.INK
        border = ft.Border.all(1, P.LINE)
    else:
        bgcolor = P.SOFT
        color = P.INK_3
        border = ft.Border.all(1, P.SOFT)

    return ft.Container(
        content=ui.text(slot, 12.5, color, ft.FontWeight.W_600 if selected else ft.FontWeight.W_500),
        bgcolor=bgcolor,
        border=border,
        border_radius=12,
        height=44,
        alignment=ft.Alignment.CENTER,
        on_click=on_click if available else None,
        ink=available,
        ink_color=P.SOFT,
        disabled=not available,
        tooltip=None if available else "Horario no disponible",
        col={"xs": 6, "sm": 3},
    )


def _label(value: str) -> ft.Text:
    return ui.text(value, 11, P.INK_3, ft.FontWeight.W_600, style=ft.TextStyle(letter_spacing=0.4))


def build(app) -> ft.Control:
    state = app.state
    draft = state.appointment

    if draft.get("confirmed_code"):
        return _success(app)

    step = draft["step"]
    tipo = data.appointment_type(draft["tipo"]) if draft["tipo"] else None
    fecha_sel = date.fromisoformat(draft["fecha"]) if draft["fecha"] else None

    def pick_type(key):
        draft["tipo"] = key
        draft["error"] = None
        app.rebuild_view()

    def pick_sede(value):
        draft["sede"] = value
        draft["error"] = None
        app.rebuild_view()

    def save_motivo(e):
        draft["motivo"] = e.control.value

    def pick_date(day: date):
        draft["fecha"] = data.iso(day)
        disponibles = {slot for slot, ok in data.slots_for(data.iso(day)) if ok}
        if draft["hora"] not in disponibles:
            draft["hora"] = None
        draft["error"] = None
        app.rebuild_view()

    def pick_slot(slot: str):
        draft["hora"] = slot
        draft["error"] = None
        app.rebuild_view()

    def fail(message: str):
        draft["error"] = message
        app.rebuild_view()
        app.toast(message, tone="warning")

    def go_next(e=None):
        if step == 1:
            if not draft["tipo"]:
                fail("Elegí el tipo de trámite para continuar.")
                return
            if not draft["sede"]:
                fail("Seleccioná la sede donde querés atenderte.")
                return
        if step == 2:
            if not draft["fecha"]:
                fail("Elegí una fecha para tu turno.")
                return
            if not draft["hora"]:
                fail("Elegí un horario disponible.")
                return
        draft["error"] = None
        draft["step"] = min(3, step + 1)
        app.rebuild_view()

    def go_back(e=None):
        draft["error"] = None
        draft["step"] = max(1, step - 1)
        app.rebuild_view()

    def cancel(e=None):
        state.reset_appointment()
        app.navigate("home")

    # ------------------------------------------------------------------
    # Paso 1: tipo de trámite y sede
    # ------------------------------------------------------------------
    step1 = ft.Column(
        [
            _label("TIPO DE TRÁMITE"),
            ft.ResponsiveRow(
                [
                    _type_card(
                        item,
                        draft["tipo"] == item["key"],
                        lambda e, k=item["key"]: pick_type(k),
                        col={"xs": 12, "sm": 6},
                    )
                    for item in data.APPOINTMENT_TYPES
                ],
                spacing=10,
                run_spacing=10,
            ),
            ft.Container(height=2),
            _label("SEDE"),
            ui.dropdown_field(
                "Sede de atención",
                data.SEDES,
                value=draft["sede"],
                on_select=pick_sede,
                hint="Seleccioná dónde querés atenderte",
            ),
            _label("MOTIVO (OPCIONAL)"),
            ui.field(
                "Motivo de la consulta",
                value=draft["motivo"],
                hint="Contanos brevemente qué necesitás resolver",
                multiline=True,
                min_lines=3,
                max_lines=5,
                on_change=save_motivo,
            ),
            ui.notice(
                "Cada turno tiene una duración estimada. Si llegás tarde, podrías perder la reserva.",
                tone="neutral",
                icon=ft.Icons.INFO_OUTLINE_ROUNDED,
            ),
        ],
        spacing=10,
    )

    # ------------------------------------------------------------------
    # Paso 2: fecha y horario
    # ------------------------------------------------------------------
    if fecha_sel:
        slots_grid = ft.ResponsiveRow(
            [
                _slot_chip(
                    slot,
                    available,
                    draft["hora"] == slot,
                    lambda e, s=slot: pick_slot(s),
                )
                for slot, available in data.slots_for(draft["fecha"])
            ],
            spacing=8,
            run_spacing=8,
        )
    else:
        slots_grid = ui.notice(
            "Seleccioná una fecha para consultar los horarios disponibles.",
            tone="neutral",
            icon=ft.Icons.SCHEDULE_ROUNDED,
        )

    step2 = ft.Column(
        [
            _label("FECHA"),
            ft.Row(
                [
                    _date_card(day, draft["fecha"] == data.iso(day), lambda e, d=day: pick_date(d))
                    for day in data.APPOINTMENT_DATES
                ],
                spacing=8,
            ),
            ft.Container(height=2),
            _label("HORARIO"),
            slots_grid,
            ft.Row(
                [
                    ui.info_pill(ft.Icons.CIRCLE, "Disponible", color=P.INK_2, icon_color=P.SURFACE),
                    ui.info_pill(ft.Icons.CIRCLE, "Seleccionado", color=P.INK_2, icon_color=P.INK),
                    ui.info_pill(ft.Icons.CIRCLE, "No disponible", color=P.INK_3, icon_color=P.SOFT_2),
                ],
                spacing=12,
                wrap=True,
                run_spacing=6,
            ),
            ui.notice(
                f"Sede seleccionada: {draft['sede'].split(' · ')[0] if draft['sede'] else 'sin seleccionar'}.",
                tone="neutral",
                icon=ft.Icons.LOCATION_ON_OUTLINED,
            ),
        ],
        spacing=10,
    )

    # ------------------------------------------------------------------
    # Paso 3: datos de contacto
    # ------------------------------------------------------------------
    def save(field_name):
        def handler(e):
            draft[field_name] = e.control.value

        return handler

    nombre = ui.field(
        "Nombre y apellido",
        value=draft["nombre"],
        hint="Como figura en tu DNI",
        on_change=save("nombre"),
        col={"xs": 12},
    )
    legajo = ui.field(
        "Legajo",
        value=draft["legajo"],
        hint="Ej.: 2026-1482",
        on_change=save("legajo"),
        col={"xs": 12, "sm": 6},
    )
    telefono = ui.field(
        "Teléfono",
        value=draft["telefono"],
        hint="11 5555-0000",
        keyboard_type=ft.KeyboardType.PHONE,
        on_change=save("telefono"),
        col={"xs": 12, "sm": 6},
    )
    email = ui.field(
        "Correo electrónico",
        value=draft["email"],
        hint="nombre@instituto.edu.ar",
        keyboard_type=ft.KeyboardType.EMAIL,
        on_change=save("email"),
        col={"xs": 12},
    )
    recordatorio = ui.switch(
        "Recibir recordatorio por correo 24 h antes",
        value=draft["recordatorio"],
        on_change=lambda e: draft.__setitem__("recordatorio", e.control.value),
    )

    def confirm(e=None):
        ok = True
        nombre.error = None
        legajo.error = None
        telefono.error = None
        email.error = None

        if not (nombre.value or "").strip():
            nombre.error = "Ingresá tu nombre y apellido."
            ok = False
        if len((legajo.value or "").strip()) < 4:
            legajo.error = "Ingresá un legajo válido."
            ok = False
        digits = "".join(ch for ch in (telefono.value or "") if ch.isdigit())
        if len(digits) < 6:
            telefono.error = "Ingresá un teléfono de contacto."
            ok = False
        email_value = (email.value or "").strip()
        if "@" not in email_value or "." not in email_value.split("@")[-1]:
            email.error = "Ingresá un correo válido."
            ok = False

        if not ok:
            app.page.update()
            app.toast("Revisá los datos marcados antes de confirmar.", tone="warning")
            return

        sede_parts = (draft["sede"] or "").split(" · ")
        state.confirmed = {
            "code": f"TUR-2026-{random.randint(300, 999):04d}",
            "tipo": tipo["titulo"] if tipo else "Turno administrativo",
            "fecha": data.fmt_fecha_media(fecha_sel),
            "fecha_larga": data.fmt_fecha_larga(fecha_sel),
            "hora": draft["hora"],
            "sede": sede_parts[0] if sede_parts else "Sede Central",
            "detalle_sede": sede_parts[1] if len(sede_parts) > 1 else "",
        }
        draft["confirmed_code"] = state.confirmed["code"]
        app.rebuild_view()
        app.toast("Turno confirmado. Te enviamos el detalle por correo.", tone="success")

    step3 = ft.Column(
        [
            _label("DATOS DEL SOLICITANTE"),
            ft.ResponsiveRow([nombre], spacing=10, run_spacing=10),
            ft.ResponsiveRow(
                [legajo, telefono],
                spacing=10,
                run_spacing=10,
            ),
            ft.ResponsiveRow([email], spacing=10, run_spacing=10),
            ft.Container(height=2),
            recordatorio,
            ui.notice(
                "Usaremos estos datos únicamente para gestionar tu turno y enviarte recordatorios.",
                tone="neutral",
                icon=ft.Icons.INFO_OUTLINE_ROUNDED,
            ),
        ],
        spacing=10,
    )

    bodies = {1: step1, 2: step2, 3: step3}
    body = bodies[step]

    # ------------------------------------------------------------------
    # Resumen lateral
    # ------------------------------------------------------------------
    fecha_txt = data.fmt_fecha_media(fecha_sel) if fecha_sel else "Sin seleccionar"
    hora_txt = f"{draft['hora']} h" if draft["hora"] else "Sin seleccionar"
    sede_txt = draft["sede"].split(" · ")[0] if draft["sede"] else "Sin seleccionar"

    resumen = ui.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ui.icon_tile(ft.Icons.RECEIPT_LONG_ROUNDED, size=36, icon_size=18),
                        ui.text("Resumen del turno", 14.5, P.INK, ft.FontWeight.W_600, expand=True),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=2),
                ui.divider(),
                ft.Container(height=2),
                ui.summary_row("Trámite", tipo["titulo"] if tipo else "Sin seleccionar"),
                ui.summary_row("Sede", sede_txt),
                ui.summary_row("Fecha", fecha_txt),
                ui.summary_row("Horario", hora_txt),
                ui.summary_row("Solicitante", draft["nombre"] or "Sin completar"),
                ui.divider(),
                ft.Container(height=2),
                ui.notice(
                    "Podés modificar cualquier dato antes de confirmar.",
                    tone="neutral",
                    icon=ft.Icons.EDIT_OUTLINED,
                ),
            ],
            spacing=8,
        ),
        padding=20,
    )

    ayuda = ui.card(
        ft.Column(
            [
                ui.section_header("Antes de venir", "Tené en cuenta"),
                ft.Container(height=2),
                *[
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=16, color=P.ACCENT),
                            ui.text(item, 12, P.INK_2, max_lines=2, expand=True),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    )
                    for item in [
                        "DNI o documentación que acredite tu identidad.",
                        "Comprobante del turno, digital o impreso.",
                        "Llegá 10 minutos antes al sector de atención.",
                    ]
                ],
            ],
            spacing=9,
        ),
        padding=20,
    )

    # ------------------------------------------------------------------
    # Estructura del asistente
    # ------------------------------------------------------------------
    footer = ft.Row(
        [
            ui.ghost_button("Cancelar", cancel, compact=True)
            if step == 1
            else ui.secondary_button(
                "Volver",
                go_back,
                icon=ft.Icons.ARROW_BACK_ROUNDED,
                compact=True,
            ),
            ft.Container(expand=True),
            ui.primary_button(
                "Confirmar turno" if step == 3 else "Continuar",
                confirm if step == 3 else go_next,
                icon=ft.Icons.CHECK_ROUNDED if step == 3 else ft.Icons.ARROW_FORWARD_ROUNDED,
                compact=True,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    wizard_items = [
        ft.Row(
            [
                ui.eyebrow(f"Paso {step} de 3"),
                ft.Container(expand=True),
                ui.text(
                    tipo["titulo"] if tipo and step > 1 else "",
                    11.5,
                    P.INK_3,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        ui.stepper(step, STEP_LABELS),
        ft.Container(height=2),
        ui.divider(),
        ft.Container(height=4),
    ]
    if draft["error"]:
        wizard_items.append(
            ui.notice(
                draft["error"],
                tone="danger",
                icon=ft.Icons.ERROR_OUTLINE_ROUNDED,
            )
        )
    wizard_items.extend([body, ft.Container(height=2), ui.divider(), ft.Container(height=4), footer])

    wizard = ui.card(
        ft.Column(wizard_items, spacing=12),
        padding=24,
    )

    contenido = ft.ResponsiveRow(
        [
            ft.Container(wizard, col={"xs": 12, "lg": 8}),
            ft.Container(
                ft.Column([resumen, ayuda], spacing=14),
                col={"xs": 12, "lg": 4},
            ),
        ],
        spacing=14,
        run_spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    header = ui.page_header(
        "Solicitar turno",
        "Reservá una atención administrativa presencial en tres pasos simples.",
        eyebrow_text="Atención al estudiante",
        actions=ui.badge("Atención presencial", "accent", icon=ft.Icons.APARTMENT_ROUNDED),
    )

    return ft.Column(
        [header, contenido],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def _success(app) -> ft.Control:
    state = app.state
    turno = state.confirmed
    user = data.USER

    def volver(e=None):
        state.reset_appointment()
        app.navigate("home")

    def otro(e=None):
        state.reset_appointment()
        app.rebuild_view()
        app.toast("Podés solicitar un nuevo turno.", tone="neutral")

    check_circle = ft.Container(
        width=76,
        height=76,
        bgcolor=P.ACCENT_SOFT,
        border_radius=RADIUS_PILL,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.CHECK_ROUNDED, size=38, color=P.ACCENT),
    )

    receipt = ft.Container(
        width=520,
        bgcolor=P.SOFT,
        border=ft.Border.all(1, P.LINE),
        border_radius=RADIUS_LG,
        padding=20,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ui.text("Código de turno", 10.5, P.INK_3, ft.FontWeight.W_600),
                                ui.text(turno["code"], 20, P.INK, ft.FontWeight.W_600),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ui.badge("Confirmado", "success", icon=ft.Icons.CHECK_ROUNDED),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=2),
                ui.divider(),
                ft.Container(height=2),
                ui.summary_row("Trámite", turno["tipo"]),
                ui.summary_row("Fecha", turno["fecha_larga"]),
                ui.summary_row("Horario", f"{turno['hora']} h"),
                ui.summary_row("Sede", f"{turno['sede']} · {turno['detalle_sede']}", last=True),
            ],
            spacing=6,
        ),
    )

    tarjeta = ui.card(
        ft.Column(
            [
                check_circle,
                ft.Container(height=6),
                ui.text("Turno confirmado", 27, P.INK, ft.FontWeight.W_600),
                ui.text(
                    "Te esperamos el turno seleccionado. Guardá el código para identificarte en la mesa de atención.",
                    13,
                    P.INK_2,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                ),
                ft.Container(height=8),
                receipt,
                ui.notice(
                    f"También enviamos la confirmación a {user['email']}.",
                    tone="neutral",
                    icon=ft.Icons.MAIL_OUTLINE_ROUNDED,
                ),
                ft.Container(height=4),
                ft.Row(
                    [
                        ui.secondary_button(
                            "Solicitar otro turno",
                            otro,
                            icon=ft.Icons.ADD_ROUNDED,
                            compact=True,
                        ),
                        ui.primary_button(
                            "Volver al inicio",
                            volver,
                            icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                            compact=True,
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=36,
    )

    header = ui.page_header(
        "Solicitar turno",
        "Tu reserva quedó registrada correctamente.",
        eyebrow_text="Atención al estudiante",
    )

    return ft.Column(
        [header, tarjeta],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
