"""Componentes reutilizables de la interfaz.

Todos los controles comparten los mismos tokens de color, radios y
espaciados para mantener consistencia visual en las cuatro vistas.
"""

from __future__ import annotations

import flet as ft

from app.theme import P, RADIUS_LG, RADIUS_MD, RADIUS_PILL, RADIUS_SM, RADIUS_XL, TONES


# ---------------------------------------------------------------------------
# Tipografía
# ---------------------------------------------------------------------------
def text(value, size=14, color=P.INK, weight=ft.FontWeight.W_400, **kwargs) -> ft.Text:
    return ft.Text(str(value), size=size, color=color, weight=weight, **kwargs)


def eyebrow(value: str, color: str = P.ACCENT) -> ft.Text:
    return ft.Text(
        value.upper(),
        size=10.5,
        color=color,
        weight=ft.FontWeight.W_600,
        style=ft.TextStyle(letter_spacing=1.2),
    )


# ---------------------------------------------------------------------------
# Superficies
# ---------------------------------------------------------------------------
def card(
    content,
    *,
    padding=22,
    radius=RADIUS_XL,
    bgcolor=P.SURFACE,
    border_color=P.LINE,
    border_width=1,
    on_click=None,
    col=None,
    height=None,
    expand=None,
    tooltip=None,
    hover=False,
) -> ft.Container:
    kwargs = {
        "content": content,
        "padding": padding,
        "bgcolor": bgcolor,
        "border": ft.Border.all(border_width, border_color) if border_width else None,
        "border_radius": radius,
        "alignment": ft.Alignment.TOP_LEFT,
    }
    if col is not None:
        kwargs["col"] = col
    if height is not None:
        kwargs["height"] = height
    if expand is not None:
        kwargs["expand"] = expand
    if tooltip is not None:
        kwargs["tooltip"] = tooltip
    if on_click is not None:
        kwargs["on_click"] = on_click
        kwargs["ink"] = True
        kwargs["ink_color"] = P.SOFT

    container = ft.Container(**kwargs)

    if hover and on_click is not None:
        def _on_hover(e):
            active = str(getattr(e, "data", "")).lower() == "true"
            container.border = ft.Border.all(1, P.LINE_STRONG if active else border_color)
            container.bgcolor = P.SURFACE if active else bgcolor
            container.update()

        container.on_hover = _on_hover

    return container


def divider(color=P.LINE, height=1) -> ft.Container:
    return ft.Container(height=height, bgcolor=color)


def spacer(height: int = 4) -> ft.Container:
    return ft.Container(height=height)


# ---------------------------------------------------------------------------
# Botones
# ---------------------------------------------------------------------------
def _base_style(
    *,
    bgcolor,
    color,
    side=None,
    compact=False,
    radius=RADIUS_MD,
) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        color={ft.ControlState.DEFAULT: color, ft.ControlState.DISABLED: P.INK_3},
        bgcolor={ft.ControlState.DEFAULT: bgcolor, ft.ControlState.DISABLED: P.SOFT},
        elevation=0,
        shadow_color="transparent",
        padding=ft.Padding.symmetric(horizontal=16 if compact else 20, vertical=0),
        shape=ft.RoundedRectangleBorder(radius=radius),
        side=side,
        text_style=ft.TextStyle(
            size=13 if compact else 14,
            weight=ft.FontWeight.W_600,
            color=color,
        ),
        overlay_color="#10000000",
        icon_size=16 if compact else 18,
    )


def primary_button(
    label,
    on_click=None,
    *,
    icon=None,
    disabled=False,
    expand=False,
    width=None,
    compact=False,
    tooltip=None,
) -> ft.Button:
    kwargs = {
        "content": label,
        "on_click": on_click,
        "style": _base_style(bgcolor=P.INK, color=P.WHITE, compact=compact),
        "height": 38 if compact else 44,
        "disabled": disabled,
        "expand": expand,
    }
    if icon is not None:
        kwargs["icon"] = icon
        kwargs["icon_color"] = P.WHITE
    if width is not None:
        kwargs["width"] = width
    if tooltip is not None:
        kwargs["tooltip"] = tooltip
    return ft.Button(**kwargs)


def secondary_button(
    label,
    on_click=None,
    *,
    icon=None,
    disabled=False,
    expand=False,
    width=None,
    compact=False,
    tooltip=None,
) -> ft.Button:
    kwargs = {
        "content": label,
        "on_click": on_click,
        "style": _base_style(
            bgcolor=P.SURFACE,
            color=P.INK,
            side=ft.BorderSide(1, P.LINE_STRONG),
            compact=compact,
        ),
        "height": 38 if compact else 44,
        "disabled": disabled,
        "expand": expand,
    }
    if icon is not None:
        kwargs["icon"] = icon
        kwargs["icon_color"] = P.INK
    if width is not None:
        kwargs["width"] = width
    if tooltip is not None:
        kwargs["tooltip"] = tooltip
    return ft.Button(**kwargs)


def ghost_button(
    label,
    on_click=None,
    *,
    icon=None,
    color=P.ACCENT,
    compact=False,
    tooltip=None,
) -> ft.TextButton:
    kwargs = {
        "content": label,
        "on_click": on_click,
        "style": ft.ButtonStyle(
            color=color,
            overlay_color="#0F2E6B4F",
            padding=ft.Padding.symmetric(horizontal=10 if compact else 12, vertical=6),
            shape=ft.RoundedRectangleBorder(radius=RADIUS_SM),
            text_style=ft.TextStyle(
                size=12.5 if compact else 13.5,
                weight=ft.FontWeight.W_600,
            ),
        ),
    }
    if icon is not None:
        kwargs["icon"] = icon
        kwargs["icon_color"] = color
    if tooltip is not None:
        kwargs["tooltip"] = tooltip
    return ft.TextButton(**kwargs)


def icon_button(
    icon,
    on_click=None,
    *,
    tooltip=None,
    size=40,
    icon_size=19,
    bgcolor=P.SURFACE,
    color=P.INK_2,
    border=True,
) -> ft.Container:
    return ft.Container(
        width=size,
        height=size,
        bgcolor=bgcolor,
        border=ft.Border.all(1, P.LINE) if border else None,
        border_radius=RADIUS_MD,
        alignment=ft.Alignment.CENTER,
        tooltip=tooltip,
        ink=True,
        ink_color=P.SOFT,
        on_click=on_click,
        content=ft.Icon(icon, size=icon_size, color=color),
    )


# ---------------------------------------------------------------------------
# Indicadores
# ---------------------------------------------------------------------------
def badge(label: str, tone: str = "neutral", icon=None) -> ft.Container:
    bg, fg = TONES.get(tone, TONES["neutral"])
    items = []
    if icon is not None:
        items.append(ft.Icon(icon, size=13, color=fg))
    items.append(text(label, 11.5, fg, ft.FontWeight.W_600))
    return ft.Container(
        content=ft.Row(items, spacing=5, tight=True),
        bgcolor=bg,
        border_radius=RADIUS_PILL,
        padding=ft.Padding.symmetric(horizontal=10, vertical=6),
    )


def status_badge(status: str, labels: dict) -> ft.Container:
    label, tone = labels.get(status, (status, "neutral"))
    return badge(label, tone)


def icon_tile(
    icon,
    *,
    bgcolor=P.ACCENT_SOFT,
    color=P.ACCENT,
    size=40,
    icon_size=20,
    radius=RADIUS_MD,
) -> ft.Container:
    return ft.Container(
        width=size,
        height=size,
        bgcolor=bgcolor,
        border_radius=radius,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(icon, size=icon_size, color=color),
    )


def avatar(initials: str, size=38, bgcolor=P.ACCENT_SOFT, color=P.ACCENT) -> ft.Container:
    return ft.Container(
        width=size,
        height=size,
        bgcolor=bgcolor,
        border_radius=RADIUS_PILL,
        alignment=ft.Alignment.CENTER,
        content=text(initials, size * 0.34, color, ft.FontWeight.W_600),
    )


def progress(value: float, *, color=P.ACCENT, bgcolor=P.SOFT_2, height=6) -> ft.ProgressBar:
    return ft.ProgressBar(
        value=max(0.0, min(1.0, value)),
        color=color,
        bgcolor=bgcolor,
        bar_height=height,
        border_radius=RADIUS_PILL,
    )


def info_pill(icon, label, *, color=P.INK_2, bgcolor=None, icon_color=None) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icon, size=14, color=icon_color or color),
                text(label, 12, color),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor=bgcolor,
        border_radius=RADIUS_PILL,
        padding=ft.Padding.symmetric(horizontal=9, vertical=5),
    )


def notice(
    message,
    *,
    tone="warning",
    icon=ft.Icons.INFO_OUTLINE_ROUNDED,
    action=None,
    on_action=None,
) -> ft.Container:
    bg, fg = TONES.get(tone, TONES["neutral"])
    items = [ft.Icon(icon, size=18, color=fg), text(message, 12.5, fg, ft.FontWeight.W_500, expand=True)]
    if action:
        items.append(ghost_button(action, on_action, color=fg, compact=True))
    return ft.Container(
        content=ft.Row(items, spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=bg,
        border_radius=RADIUS_MD,
        padding=ft.Padding.symmetric(horizontal=14, vertical=12),
    )


def empty_state(
    title,
    description,
    *,
    icon=ft.Icons.SEARCH_OFF_ROUNDED,
    action=None,
    on_action=None,
) -> ft.Container:
    items = [
        ft.Container(
            width=52,
            height=52,
            bgcolor=P.SOFT,
            border_radius=RADIUS_PILL,
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(icon, size=24, color=P.INK_3),
        ),
        text(title, 15, P.INK, ft.FontWeight.W_600),
        text(description, 12.5, P.INK_2, text_align=ft.TextAlign.CENTER, max_lines=3),
    ]
    if action:
        items.append(ghost_button(action, on_action, icon=ft.Icons.ARROW_BACK_ROUNDED))
    return ft.Container(
        content=ft.Column(
            items,
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.symmetric(horizontal=24, vertical=44),
    )


# ---------------------------------------------------------------------------
# Formularios
# ---------------------------------------------------------------------------
def _field_border() -> dict:
    return {
        ft.ControlState.DEFAULT: ft.OutlineInputBorder(
            border_radius=RADIUS_MD,
            side=ft.BorderSide(1, P.LINE),
            gap_padding=1,
        ),
        ft.ControlState.FOCUSED: ft.OutlineInputBorder(
            border_radius=RADIUS_MD,
            side=ft.BorderSide(1.5, P.ACCENT),
            gap_padding=1,
        ),
        ft.ControlState.ERROR: ft.OutlineInputBorder(
            border_radius=RADIUS_MD,
            side=ft.BorderSide(1.5, P.DANGER),
            gap_padding=1,
        ),
    }


def field(
    label,
    *,
    value="",
    hint=None,
    on_change=None,
    on_submit=None,
    error=None,
    multiline=False,
    keyboard_type=None,
    read_only=False,
    expand=True,
    col=None,
    prefix_icon=None,
    min_lines=None,
    max_lines=None,
    autofocus=False,
    text_size=14,
) -> ft.TextField:
    kwargs = {
        "label": label,
        "value": value or "",
        "hint_text": hint,
        "filled": True,
        "fill_color": P.SOFT,
        "border": _field_border(),
        "content_padding": ft.Padding.only(left=14, right=14, top=16, bottom=12)
        if not multiline
        else ft.Padding.symmetric(horizontal=14, vertical=14),
        "text_size": text_size,
        "color": P.INK,
        "cursor_color": P.ACCENT,
        "label_style": ft.TextStyle(size=12, color=P.INK_2, weight=ft.FontWeight.W_500),
        "hint_style": ft.TextStyle(size=13.5, color=P.INK_3),
        "error_style": ft.TextStyle(size=11, color=P.DANGER),
        "read_only": read_only,
        "autofocus": autofocus,
        "multiline": multiline,
        "expand": expand,
    }
    if on_change is not None:
        kwargs["on_change"] = on_change
    if on_submit is not None:
        kwargs["on_submit"] = on_submit
    if error is not None:
        kwargs["error"] = error
    if keyboard_type is not None:
        kwargs["keyboard_type"] = keyboard_type
    if prefix_icon is not None:
        kwargs["prefix_icon"] = prefix_icon
    if multiline:
        kwargs["min_lines"] = min_lines or 3
        kwargs["max_lines"] = max_lines or 5
    if col is not None:
        kwargs["col"] = col
    return ft.TextField(**kwargs)


def dropdown_field(
    label,
    options,
    *,
    value=None,
    on_select=None,
    hint=None,
    expand=True,
    col=None,
) -> ft.Dropdown:
    dd = ft.Dropdown(
        label=label,
        hint_text=hint,
        options=[ft.dropdown.Option(o) for o in options],
        value=value,
        filled=True,
        fill_color=P.SOFT,
        border=_field_border(),
        content_padding=ft.Padding.only(left=14, right=14, top=16, bottom=12),
        text_size=14,
        color=P.INK,
        label_style=ft.TextStyle(size=12, color=P.INK_2, weight=ft.FontWeight.W_500),
        hint_style=ft.TextStyle(size=13.5, color=P.INK_3),
        menu_height=320,
        expand=expand,
        col=col,
    )
    if on_select is not None:
        dd.on_select = lambda e: on_select(dd.value)
    return dd


def segmented(options, selected, on_select) -> ft.Container:
    """Control segmentado propio, con aspecto de iOS y sin azul."""
    row = ft.Row(spacing=4, tight=True)
    for value, label in options:
        active = value == selected
        row.controls.append(
            ft.Container(
                content=text(
                    label,
                    12.5,
                    P.WHITE if active else P.INK_2,
                    ft.FontWeight.W_600 if active else ft.FontWeight.W_500,
                ),
                bgcolor=P.INK if active else None,
                border_radius=9,
                padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                ink=True,
                ink_color=P.SOFT,
                on_click=lambda e, v=value: on_select(v),
            )
        )
    return ft.Container(
        content=row,
        bgcolor=P.SOFT,
        border_radius=12,
        padding=4,
    )


def switch(label, *, value=True, on_change=None) -> ft.Switch:
    return ft.Switch(
        label=label,
        value=value,
        active_color=P.ACCENT,
        active_track_color=P.ACCENT_SOFT,
        inactive_track_color=P.SOFT_2,
        inactive_thumb_color=P.SURFACE,
        label_text_style=ft.TextStyle(size=13, color=P.INK_2),
        on_change=on_change,
    )


# ---------------------------------------------------------------------------
# Encabezados y bloques de contenido
# ---------------------------------------------------------------------------
def page_header(
    title,
    subtitle=None,
    *,
    actions=None,
    eyebrow_text=None,
) -> ft.Row:
    items = []
    if eyebrow_text:
        items.append(eyebrow(eyebrow_text))
    items.append(text(title, 28, P.INK, ft.FontWeight.W_600))
    if subtitle:
        items.append(text(subtitle, 13.5, P.INK_2, max_lines=2))
    return ft.Row(
        [
            ft.Column(items, spacing=5, expand=True),
            actions if actions is not None else ft.Container(width=0),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
    )


def section_header(title, subtitle=None, *, action=None, on_action=None) -> ft.Row:
    left = [text(title, 16.5, P.INK, ft.FontWeight.W_600)]
    if subtitle:
        left.append(text(subtitle, 12.5, P.INK_2))
    right = ft.Container(width=0)
    if action:
        right = ghost_button(action, on_action, icon=ft.Icons.ARROW_FORWARD_ROUNDED)
    return ft.Row(
        [ft.Column(left, spacing=3, expand=True), right],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def summary_row(label, value, *, value_color=P.INK, last=False) -> ft.Container:
    content = ft.Column(
        [
            ft.Row(
                [
                    text(label, 12, P.INK_2, expand=True),
                    text(value, 12.5, value_color, ft.FontWeight.W_600, text_align=ft.TextAlign.RIGHT),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
            ),
            ft.Container(height=11) if not last else ft.Container(height=0),
        ],
        spacing=0,
    )
    return content


def quick_tile(icon, title, subtitle, *, on_click=None, col=None) -> ft.Container:
    tile = ft.Container(
        content=ft.Column(
            [
                icon_tile(icon, size=36, icon_size=18, radius=RADIUS_SM),
                spacer(2),
                text(title, 13.5, P.INK, ft.FontWeight.W_600),
                text(subtitle, 11.5, P.INK_2, max_lines=2),
            ],
            spacing=4,
        ),
        bgcolor=P.SOFT,
        border_radius=RADIUS_LG,
        padding=14,
        on_click=on_click,
        ink=True,
        ink_color=P.SOFT_2,
        col=col,
        height=126,
    )
    return tile


# ---------------------------------------------------------------------------
# Asistente de turnos
# ---------------------------------------------------------------------------
def stepper(current: int, labels) -> ft.Container:
    items = []
    for index, label in enumerate(labels, start=1):
        done = index < current
        active = index == current
        circle_bg = P.INK if (active or done) else P.SOFT
        circle_fg = P.WHITE if (active or done) else P.INK_3
        items.append(
            ft.Row(
                [
                    ft.Container(
                        width=26,
                        height=26,
                        bgcolor=circle_bg,
                        border_radius=RADIUS_PILL,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(ft.Icons.CHECK_ROUNDED, size=14, color=circle_fg)
                        if done
                        else text(str(index), 11.5, circle_fg, ft.FontWeight.W_600),
                    ),
                    text(
                        label,
                        12,
                        P.INK if (active or done) else P.INK_3,
                        ft.FontWeight.W_600 if active else ft.FontWeight.W_500,
                    ),
                ],
                spacing=8,
                tight=True,
            )
        )
        if index < len(labels):
            items.append(
                ft.Container(
                    height=1,
                    bgcolor=P.LINE,
                    expand=True,
                    margin=ft.Margin.symmetric(horizontal=6),
                )
            )
    return ft.Container(content=ft.Row(items, vertical_alignment=ft.CrossAxisAlignment.CENTER), width=None)


def timeline(steps) -> ft.Column:
    rows = []
    for index, step in enumerate(steps):
        state = step.get("estado", "pendiente")
        done = state == "completado"
        current = state == "en_proceso"
        last = index == len(steps) - 1

        if done:
            dot = ft.Container(
                width=24,
                height=24,
                bgcolor=P.ACCENT,
                border_radius=RADIUS_PILL,
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(ft.Icons.CHECK_ROUNDED, size=14, color=P.WHITE),
            )
            connector_color = P.ACCENT_LINE
            title_color = P.INK
            date_color = P.ACCENT
        elif current:
            dot = ft.Container(
                width=24,
                height=24,
                bgcolor=P.WARN_SOFT,
                border=ft.Border.all(2, P.WARN),
                border_radius=RADIUS_PILL,
                alignment=ft.Alignment.CENTER,
                content=ft.Container(width=8, height=8, bgcolor=P.WARN, border_radius=RADIUS_PILL),
            )
            connector_color = P.LINE
            title_color = P.INK
            date_color = P.WARN
        else:
            dot = ft.Container(
                width=24,
                height=24,
                border=ft.Border.all(2, P.LINE_STRONG),
                border_radius=RADIUS_PILL,
            )
            connector_color = P.LINE
            title_color = P.INK_2
            date_color = P.INK_3

        rows.append(
            ft.Row(
                [
                    ft.Column(
                        [
                            dot,
                            ft.Container(
                                width=2,
                                height=54,
                                bgcolor=connector_color,
                                border_radius=RADIUS_PILL,
                            )
                            if not last
                            else ft.Container(),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        width=24,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                text(step["titulo"], 13.5, title_color, ft.FontWeight.W_600),
                                text(step["fecha"], 11.5, date_color, ft.FontWeight.W_500),
                                spacer(2),
                                text(step["detalle"], 12, P.INK_2, max_lines=2),
                            ],
                            spacing=2,
                        ),
                        padding=ft.Padding.only(left=12, bottom=0 if last else 18),
                        expand=True,
                    ),
                ],
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        )
    return ft.Column(rows, spacing=0)
