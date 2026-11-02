"""Tokens de diseño del portal.

La paleta es cálida y de bajo contraste: nada de azul ni acentos neón.
La estética sigue las convenciones de iOS (superficies limpias, bordes
suaves, jerarquía tipográfica marcada y acciones principales oscuras).
"""

from __future__ import annotations


class Palette:
    # Superficies
    BG = "#F5F4F0"
    SIDEBAR = "#FBFAF7"
    SURFACE = "#FFFFFF"
    SOFT = "#F1F0EB"
    SOFT_2 = "#E8E6DF"
    LINE = "#E5E3DC"
    LINE_STRONG = "#D6D3CA"

    # Texto
    INK = "#1C1C1E"
    INK_2 = "#6C6C71"
    INK_3 = "#9A9A9F"

    # Acento institucional (verde profundo, sin azul)
    ACCENT = "#2E6B4F"
    ACCENT_DARK = "#245640"
    ACCENT_SOFT = "#E7F0EA"
    ACCENT_LINE = "#C9DED1"

    # Tonos de apoyo
    SAND = "#EDE4D7"
    SAND_DEEP = "#7C5231"
    WARN = "#8A5A00"
    WARN_SOFT = "#FAF0DB"
    DANGER = "#A9362E"
    DANGER_SOFT = "#FBEAE8"
    WHITE = "#FFFFFF"


P = Palette

# (fondo, texto) para badges y avisos
TONES = {
    "accent": (P.ACCENT_SOFT, P.ACCENT),
    "success": (P.ACCENT_SOFT, P.ACCENT),
    "warning": (P.WARN_SOFT, P.WARN),
    "danger": (P.DANGER_SOFT, P.DANGER),
    "neutral": (P.SOFT, P.INK_2),
    "sand": (P.SAND, P.SAND_DEEP),
}

FONT = "Segoe UI"

RADIUS_SM = 10
RADIUS_MD = 14
RADIUS_LG = 18
RADIUS_XL = 24
RADIUS_PILL = 999

SPACE = 8
