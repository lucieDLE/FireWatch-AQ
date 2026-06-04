import path_setup  # noqa: F401
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

import dash_bootstrap_components as dbc
from dash import Dash
from layout import build_layout
import callbacks  # registers all @app.callback decorators
# ── App init ──────────────────────────────────────────────────────────────────

app = Dash(
    __name__,
    assets_folder=str(ROOT_DIR / "app/assets"),
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
)
server = app.server
app.layout = build_layout()

if __name__ == "__main__":
    app.run(debug=True, port=8050)
