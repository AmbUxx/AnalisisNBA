"""
Módulo UI para componentes reutilizables
"""

from .components import render_comparison_table, render_simple_header, render_metric_card, render_bento_grid
from .styles import apply_custom_styles

__all__ = [
    'render_comparison_table',
    'render_simple_header',
    'render_metric_card',
    'render_bento_grid',
    'apply_custom_styles'
]

