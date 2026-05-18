"""CEAScene : une Scene Manim avec le branding CEA intégré.

Utilisation typique :

    from manim import *
    from manim_cea import CEAScene, bullet_list

    class MaPresentation(CEAScene):
        AUTHOR  = "Prénom NOM"
        SEMINAR = "Séminaire CEA"
        DATE    = "Mai 2026"

        def construct(self):
            self.title_slide("Ma présentation")
            self.wait(2)

            self.new_slide("Introduction")
            self.play(FadeIn(bullet_list(["Premier point", "Deuxième point"])))
            self.wait(2)
"""
import os
from manim import (
    Group, Text, Square, ImageMobject,
    FadeIn, FadeOut, WHITE, GREY_C, BOLD, UL, UR, DL, DR, UP, DOWN, LEFT, RIGHT,
)
from .theme import CEA_RED, asset

from manim_slides import Slide

class CEAScene(Slide):
    """Scene de base au format CEA.

    Surchargez les attributs de classe `AUTHOR`, `SEMINAR`, `DATE` dans votre
    sous-classe, puis appelez `self.title_slide(...)` / `self.new_slide(...)`
    dans `construct()`.
    """

    AUTHOR: str = ""
    SEMINAR: str = ""
    DATE: str = ""

    # ------------------------------------------------------------------
    # Cycle de vie
    # ------------------------------------------------------------------
    def setup(self):
        self._page_number = 1
        self._chrome = Group()  # éléments persistants (cube, titre, footer)

    # ------------------------------------------------------------------
    # Briques visuelles (réutilisables si besoin)
    # ------------------------------------------------------------------
    def logo(self, scale: float = 0.45, position=None):
        path = asset("logo_cea.png")
        if os.path.exists(path):
            mob = ImageMobject(path).scale(scale)
        else:
            mob = Square(side_length=1, color=CEA_RED, fill_opacity=1).scale(scale)
        if position is None:
            mob.to_corner(UL, buff=0.5)
        else:
            mob.move_to(position)
        return mob

    def cube(self, kind: str = "frame", scale: float = 0.5):
        """`kind` : 'title' (page de titre) ou 'frame' (slide standard)."""
        path = asset(f"{kind}_cube_black.png")
        if not os.path.exists(path):
            return Group()
        return ImageMobject(path).scale(scale).to_corner(UR, buff=0)

    def footer(self, with_logo: bool = True):
        parts = " – ".join(p for p in (self.AUTHOR, self.SEMINAR, self.DATE) if p)
        if self._page_number is not None:
            parts += f"  {self._page_number}"
        txt = Text(parts, color=GREY_C, font_size=18).to_corner(DR, buff=0.3).shift(UP * 0.1)
        g = Group(txt)
        if with_logo:
            g.add(self.logo(scale=0.15).to_corner(DL, buff=0.3))
        return g

    # ------------------------------------------------------------------
    # API haut niveau
    # ------------------------------------------------------------------
    def title_slide(self, title: str, animate: bool = True):
        """Affiche la slide de titre. Renvoie le Group créé."""
        logo  = self.logo()
        cube  = self.cube(kind="title", scale=0.65)
        base  = 48
        t = Text(title,        font_size=base,       color=WHITE, weight=BOLD)
        a = Text(self.AUTHOR,  font_size=base * 0.65, color=WHITE)
        s = Text(self.SEMINAR, font_size=base * 0.55, color=WHITE)
        d = Text(self.DATE,    font_size=base * 0.5,  color=WHITE)

        texts = Group(t, a, s, d).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        texts.align_to(logo, LEFT).shift(DOWN * 0.5)

        foot = self.footer(with_logo=False)
        self._page_number += 1

        slide = Group(logo, cube, texts, foot)
        if animate:
            self.play(FadeIn(slide))
        else:
            self.add(slide)
        return slide

    def new_slide(self, title_text: str, clear: bool = True, animate: bool = True):
        """Démarre une nouvelle slide standard.

        - Efface l'écran si `clear=True`.
        - Met en place cube (haut droite), titre (haut gauche), footer.
        - Renvoie le Text du titre (pratique pour des animations ultérieures).
        """
        if clear:
            self.clear_slide(animate=animate)

        cube  = self.cube(kind="frame", scale=0.5)
        title = Text(title_text, font_size=32, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.5)
        foot  = self.footer(with_logo=True)
        self._page_number += 1

        self._chrome = Group(cube, title, foot)
        if animate:
            self.play(FadeIn(self._chrome))
        else:
            self.add(self._chrome)
        return title

    def clear_slide(self, animate: bool = True):
        """Efface tout ce qui est actuellement à l'écran."""
        if not self.mobjects:
            return
        if animate:
            self.play(*[FadeOut(m) for m in self.mobjects])
        else:
            self.clear()
