# CEAPresentation
Dépot illustrant la création de présentation avec beamer et manim-slides de présentation



#Compilation des slides avec manim-slides
##Commandes de bases
manim example.py Partie
manim-slides convert Partie slides.html --open
##Presentation longues
Pour éviter des recompilations excessives, nous conseillons aux utilisateurs de découper leur présentation en parties ou sous parties matérialisées par plusieurs classe. La compilation de plusieurs classes s'effectue logiquement de la façon suivante:

manim example.py PartieUne PartieDeux
manim-slides convert PartieUne PartieDeux slides.html --open

Mais si l'utilisateur n'est amené à ne modifier qu'une seule des parties par exemple la PartieUne alors il peut simplement appeler:
manim example.py PartieUne

Puis afficher la présentation complète (manim-slides utilisera l'ancienne version de PartieDeux) avec la commande précédente:
manim-slides PartieUne PartieDeux
