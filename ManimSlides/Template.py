#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple d'utilisation du template CEA pour Manim Slides
"""

from manim import *
from manim_slides import Slide
from cea_theme_utils import (CEATheme, create_bullet_list, 
                             create_numbered_list, create_two_columns)


class ExemplePresentation(Slide):
    def __init__(self):
        super().__init__()
        self.camera.background_color = BLACK
        author="P. Bouteiller"
        seminar="Séminaire mécanique"
        date="01/11/25"
        self.theme = CEATheme(self, author, seminar, date)
        
    def construct(self):
        # ===== SLIDE 1: PAGE DE TITRE =====
        title_slide = self.theme.create_title_slide(title="Élasticité anisotrope\nen transformations finies")
        
        self.play(*[FadeIn(obj) for obj in title_slide])
        self.wait()
        self.next_slide()
        
        # ===== SLIDE 2: PLAN =====
        self.clear()
        
        # Éléments de base de la slide
        slide_elements, title = self.theme.create_standard_slide(title_text="Plan")
        
        self.add(slide_elements)
        self.play(Write(title))
        
        # Liste numérotée pour le plan
        plan_items = ["Introduction à la mécanique des milieux continus",
                      "Le problème élastique",
                      "Élasticité anisotrope en transformations finies"]
        
        plan_list = create_numbered_list(plan_items, font_size=32)
        plan_list.shift(UP * 0.5)
        
        for item in plan_list:
            self.play(FadeIn(item))
            self.next_slide()
        
        # ===== SLIDE 3: LISTES À PUCES =====
        self.clear()
        slide_elements, title = self.theme.create_standard_slide(title_text="Hypothèses fondamentales")
        
        self.add(slide_elements, title)
        
        # Liste à puces principale
        main_items = ["Hypothèse des petites déformations",
                      "Matériau homogène et isotrope",
                      "Comportement élastique linéaire"]
        
        bullet_list = create_bullet_list(main_items)
        
        for bullet in bullet_list:
            self.play(FadeIn(bullet))
            self.wait(0.5)
        
        self.next_slide()
        
        # ===== SLIDE 4: DEUX COLONNES =====
        self.clear()
        slide_elements, title = self.theme.create_standard_slide(title_text="Comparaison des approches")
        
        self.add(slide_elements, title)
        
        # Colonne gauche
        left_title = Text("Approche Lagrangienne", font_size=28, color=CEATheme.CEA_LIGHT_BLUE, weight=BOLD)
        left_items = ["Description matérielle", "Configuration de référence", "Convient aux solides"]
        left_list = create_bullet_list(left_items, font_size=26)
        left_content = Group(left_title, left_list).arrange(DOWN, buff=0.5)
        
        # Colonne droite
        right_title = Text("Approche Eulérienne", font_size=28, color=CEATheme.CEA_YELLOW, weight=BOLD)
        right_items = ["Description spatiale", "Configuration actuelle", "Convient aux fluides"]
        right_list = create_bullet_list(right_items, font_size=26)
        right_content = Group(right_title, right_list).arrange(DOWN, buff=0.5)
        
        # Créer la mise en page à deux colonnes
        columns = create_two_columns(left_content, right_content, buff=1.5)
        columns.shift(UP * 0.3)
        
        self.play(FadeIn(columns))
        self.next_slide()
        
        # ===== SLIDE 5: BLOC D'ALERTE =====
        self.clear()
        slide_elements, title = self.theme.create_standard_slide(title_text="Points importants")
        
        self.add(slide_elements, title)
        
        # Créer un bloc d'alerte (équivalent beamer alertblock)
        alert_title = Text("Attention", font_size=32, color=WHITE, weight=BOLD)
        alert_title.set_color(CEATheme.CEA_RED)
        
        alert_text = Text(
            "Les transformations finies nécessitent\nune formulation non-linéaire complète",
            font_size=28,
            color=WHITE,
            line_spacing=1.2
        )
        
        alert_box = Group(alert_title, alert_text).arrange(DOWN, buff=0.3)
        
        # Ajouter un fond
        background = SurroundingRectangle(alert_box, color=CEATheme.CEA_RED,
                                          fill_opacity=0.2, buff=0.4, corner_radius=0.1)
        
        alert_block = Group(background, alert_box)
        alert_block.shift(UP * 0.5)
        
        # Option simple : tout en FadeIn
        self.play(FadeIn(alert_block))
        self.next_slide()


if __name__ == "__main__":
    # Pour exécuter: manim -pql exemple_presentation.py ExemplePresentation
    pass