"""
LLM Multi-Agent System Evaluation Dashboard
Visualises per-project, per-variant evaluation scores from Claude, Codex, and Gemini.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import streamlit as st

# ---------------------------------------------------------------------------
# Global matplotlib style (scientific / publication-ready)
# ---------------------------------------------------------------------------
mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "legend.framealpha": 0.9,
    "legend.edgecolor": "#aaaaaa",
    "figure.dpi": 150,
    "grid.linestyle": "--",
    "grid.linewidth": 0.6,
    "grid.alpha": 0.5,
})

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
PROJECTS: List[str] = [str(i) for i in range(1, 11)]
MODELS: List[str] = ["Claude", "Codex", "Gemini"]
VARIANTS: List[str] = ["gaia", "non_gaia", "prepared_gaia"]
VARIANT_LABELS: Dict[str, str] = {
    "gaia": "GAIA",
    "non_gaia": "Non-GAIA",
    "prepared_gaia": "Prepared GAIA",
}
SCORE_KEYS: List[str] = [
    "requirements_fit",
    "logical_consistency",
    "component_coverage",
    "interface_logic",
    "implementation_alignment",
    "overall",
]
SCORE_LABELS: Dict[str, str] = {
    "requirements_fit": "Req. Fit",
    "logical_consistency": "Logic",
    "component_coverage": "Coverage",
    "interface_logic": "Interface",
    "implementation_alignment": "Impl. Align.",
    "overall": "Overall",
}
MODEL_COLORS: Dict[str, str] = {
    "Claude": "#1f77b4",   # muted blue
    "Codex":  "#ff7f0e",   # safety orange
    "Gemini": "#2ca02c",   # cooked asparagus green
}
MODEL_HATCHES: Dict[str, str] = {
    "Claude": "",
    "Codex":  "//",
    "Gemini": "..",
}

# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def _load_json(path: Path) -> Optional[Dict]:
    if not path.is_file():
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None


def load_project_title(project: str) -> str:
    raw = _load_json(BASE_DIR / project / "requirements.json")
    if raw and isinstance(raw, list) and raw[0].get("title"):
        return raw[0]["title"]
    return ""


def load_project_scores(project: str) -> Dict[str, Dict[str, Optional[Dict]]]:
    """
    Returns nested dict: model -> variant -> scores dict (or None).
    scores dict has keys from SCORE_KEYS.
    """
    reports_dir = BASE_DIR / project / "Reports"
    data: Dict[str, Dict[str, Optional[Dict]]] = {}
    for model in MODELS:
        data[model] = {}
        for variant in VARIANTS:
            path = reports_dir / model / f"report_{variant}.json"
            report = _load_json(path)
            data[model][variant] = report.get("scores") if report else None
    return data


# ---------------------------------------------------------------------------
# Figure factory
# ---------------------------------------------------------------------------

BAR_WIDTH = 0.22
X = np.arange(len(SCORE_KEYS))


def _draw_variant_axes(
    ax: plt.Axes,
    variant: str,
    model_scores: Dict[str, Optional[Dict]],
    show_ylabel: bool,
) -> List:
    """Populate a single axes (one variant) with grouped bars. Returns legend handles."""
    handles = []
    n = len(MODELS)
    offsets = np.linspace(-(n - 1) / 2, (n - 1) / 2, n) * BAR_WIDTH

    for model, offset in zip(MODELS, offsets):
        scores = model_scores[model]
        if scores is None:
            continue
        values = [scores.get(key, np.nan) for key in SCORE_KEYS]
        bar = ax.bar(
            X + offset,
            values,
            BAR_WIDTH,
            label=model,
            color=MODEL_COLORS[model],
            hatch=MODEL_HATCHES[model],
            alpha=0.82,
            edgecolor="white",
            linewidth=0.4,
        )
        handles.append(bar)

    ax.set_title(VARIANT_LABELS[variant])
    ax.set_xticks(X)
    ax.set_xticklabels(
        [SCORE_LABELS[k] for k in SCORE_KEYS],
        rotation=28,
        ha="right",
    )
    ax.set_ylim(0, 10.5)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y")

    if show_ylabel:
        ax.set_ylabel("Score  (0 – 10)", labelpad=6)

    # Mark "no data" for variants with zero bars
    active = [m for m in MODELS if model_scores[m] is not None]
    if not active:
        ax.text(
            0.5, 0.5, "No data available",
            ha="center", va="center",
            transform=ax.transAxes,
            color="#888888",
            fontsize=9,
            style="italic",
        )

    return handles


def build_project_figure(project: str, data: Dict, title: str = "") -> plt.Figure:
    fig, axes = plt.subplots(
        1, 3,
        figsize=(15, 4.2),
        sharey=True,
        gridspec_kw={"wspace": 0.08},
    )

    all_handles: List = []
    all_labels: List[str] = []

    for ax, variant in zip(axes, VARIANTS):
        model_scores = {m: data[m][variant] for m in MODELS}
        handles = _draw_variant_axes(
            ax=ax,
            variant=variant,
            model_scores=model_scores,
            show_ylabel=(variant == VARIANTS[0]),
        )
        for h in handles:
            label = h.get_label()
            if label not in all_labels:
                all_handles.append(h)
                all_labels.append(label)

    name = f" — {title}" if title else ""
    fig.suptitle(
        f"Project {project}{name}",
        fontsize=11,
        fontweight="bold",
        y=1.03,
    )
    fig.legend(
        all_handles,
        all_labels,
        title="LLM Model",
        title_fontsize=8,
        loc="lower center",
        ncol=3,
        bbox_to_anchor=(0.5, -0.2),
        frameon=True,
    )
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Streamlit application
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(
        page_title="LLM MAS Evaluation Dashboard",
        page_icon="📊",
        layout="wide",
    )

    st.title("LLM Multi-Agent System Evaluation Dashboard")
    st.markdown(
        """
        Pairwise comparison of evaluation scores assigned by **Claude**, **Codex**, and **Gemini**
        across 10 projects and three implementation variants
        (*GAIA*, *Non-GAIA*, *Prepared GAIA*).

        **Score dimensions** (0 – 10 scale):
        *Requirements Fit* · *Logical Consistency* · *Component Coverage* ·
        *Interface Logic* · *Implementation Alignment* · *Overall*
        """,
        unsafe_allow_html=False,
    )
    st.divider()

    # Sidebar — filter
    with st.sidebar:
        st.header("Filters")
        selected_projects = st.multiselect(
            "Projects to display",
            options=PROJECTS,
            default=PROJECTS,
            format_func=lambda p: f"Project {p}",
        )
        show_missing = st.checkbox(
            "Show projects with no reports at all",
            value=False,
        )

    if not selected_projects:
        st.info("Select at least one project in the sidebar.")
        return

    for project in selected_projects:
        project_title = load_project_title(project)
        data = load_project_scores(project)

        has_any = any(
            data[m][v] is not None
            for m in MODELS
            for v in VARIANTS
        )

        if not has_any and not show_missing:
            continue

        with st.expander(f"Project {project}", expanded=True):
            if not has_any:
                st.warning("No report files found for this project yet.")
                continue

            # Show which (model, variant) combinations are available
            available = [
                f"{m} / {VARIANT_LABELS[v]}"
                for m in MODELS
                for v in VARIANTS
                if data[m][v] is not None
            ]
            st.caption(f"Available reports: {', '.join(available)}")

            fig = build_project_figure(project, data, project_title)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    st.divider()
    st.caption(
        "Scores are read from `<project>/Reports/<Model>/report_<variant>.json`. "
        "Missing files are silently skipped."
    )


if __name__ == "__main__":
    main()
