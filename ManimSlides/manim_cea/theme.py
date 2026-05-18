"""Palette de couleurs CEA et chemins vers les assets packagés."""
from pathlib import Path

# --- Palette CEA ---
CEA_RED        = "#E50019"
CEA_DARK_BLUE  = "#3E4A83"
CEA_LIGHT_BLUE = "#7E9CBB"
CEA_DARK_GRAY  = "#262626"
CEA_GRAY       = "#787878"
CEA_LIGHT_GRAY = "#BEBEBE"
CEA_YELLOW     = "#FFCD31"
CEA_MACARON    = "#DA837B"
CEA_ARCHIPEL   = "#00939D"
CEA_OPERA      = "#BD987A"
CEA_GLYCINE    = "#A72587"
CEA_GREEN      = "#6AB023"
CEA_ORANGE     = "#FF8C42"

# --- Assets packagés ---
_PKG_DIR    = Path(__file__).parent
ASSETS_DIR  = _PKG_DIR / "graphics"


def asset(name: str) -> str:
    """Retourne le chemin absolu d'un asset packagé (logo, cube, ...)."""
    return str(ASSETS_DIR / name)
