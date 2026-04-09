"""
GameGen AI - Shared tip renderer

Call render_tips(tips_list) anywhere in a UI module to display
the contextual tips panel returned by ui/tips.py.
"""

import streamlit as st


def render_tips(tips: list[dict]) -> None:
    """
    Render a list of tip dicts produced by the tips engine.

    Each dict must have keys:
        icon   : emoji string
        level  : "critical" | "warning" | "info" | "tip"
        text   : the tip message
    """
    if not tips:
        return

    st.markdown(
        '<div class="tips-header">💡 LIVE TIPS</div>',
        unsafe_allow_html=True,
    )
    for tip in tips:
        level = tip.get("level", "tip")
        icon  = tip.get("icon", "💡")
        text  = tip.get("text", "")
        st.markdown(
            f'<div class="tip-card tip-{level}">'
            f'<strong>{icon}</strong> {text}'
            f'</div>',
            unsafe_allow_html=True,
        )
