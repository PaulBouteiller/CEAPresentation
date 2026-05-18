"""manim_cea — surcouche Manim au style CEA.

Exemple minimal :

    from manim import *
    from manim_cea import CEAScene, bullet_list

    class Demo(CEAScene):
        AUTHOR  = "Prénom NOM"
        SEMINAR = "Séminaire CEA"
        DATE    = "Mai 2026"

        def construct(self):
            self.title_slide("Ma présentation")
            self.wait(2)
            self.new_slide("Introduction")
            self.play(FadeIn(bullet_list(["Point 1", "Point 2"])))
            self.wait(2)
"""
from .scene import CEAScene
from .components import (
    bullet_list,
    numbered_list,
    two_columns,
    red_square_item,
    red_square_list,
)
from .video import VideoMobject
from .theme import (
    asset,
    CEA_RED, CEA_DARK_BLUE, CEA_LIGHT_BLUE, CEA_DARK_GRAY, CEA_GRAY,
    CEA_LIGHT_GRAY, CEA_YELLOW, CEA_MACARON, CEA_ARCHIPEL, CEA_OPERA,
    CEA_GLYCINE, CEA_GREEN, CEA_ORANGE,
)

__version__ = "0.1.0"

__all__ = [
    # Scene
    "CEAScene",
    # Composants
    "bullet_list", "numbered_list", "two_columns",
    "red_square_item", "red_square_list",
    # Vidéo
    "VideoMobject",
    # Couleurs
    "CEA_RED", "CEA_DARK_BLUE", "CEA_LIGHT_BLUE", "CEA_DARK_GRAY", "CEA_GRAY",
    "CEA_LIGHT_GRAY", "CEA_YELLOW", "CEA_MACARON", "CEA_ARCHIPEL", "CEA_OPERA",
    "CEA_GLYCINE", "CEA_GREEN", "CEA_ORANGE",
]
