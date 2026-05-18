# CEAPresentation
Dépôt illustrant la création de présentations avec Beamer et Manim-Slides.
Manim-Slides est un outil permettant de transformer des animations Manim en
présentations interactives, navigables slide par slide.

# Compilation des slides avec Manim-Slides
Supposons que le fichier utilisateur s'appelle `example.py`.

## Commandes de base
Les commandes de base pour compiler une slide et l'afficher dans le navigateur :
```bash
manim example.py Partie
manim-slides convert Partie slides.html --open
```

## Présentations longues
Pour éviter des recompilations excessives, nous conseillons aux utilisateurs de
découper leur présentation en parties ou sous-parties matérialisées par plusieurs
classes. La compilation de plusieurs classes s'effectue de la façon suivante :
```bash
manim example.py PartieUne PartieDeux
manim-slides convert PartieUne PartieDeux slides.html --open
```

Mais si l'utilisateur n'est amené à modifier qu'une seule partie, par exemple
`PartieUne`, il peut simplement recompiler celle-ci :
```bash
manim example.py PartieUne
```

Puis afficher la présentation complète (manim-slides utilisera l'ancienne version
de `PartieDeux`) avec la commande suivante :
```bash
manim-slides PartieUne PartieDeux
```

## Options utiles

### Compilation rapide
Pour accélérer la compilation, l'utilisateur peut rajouter l'option `-ql`
(basse qualité) à la ligne de commande :
```bash
manim example.py PartieUne -ql
```

### Compilation en boucle
Si les scènes ont été numérotées `Slide1`, `Slide2`, etc., il est possible de
toutes les compiler en une seule commande grâce à une boucle shell :
```bash
for i in {1..5}; do manim -ql example.py Slide$i; done
```

Puis de les convertir et afficher en une seule commande :
```bash
manim-slides convert $(for i in {1..5}; do echo Slide$i; done) slides.html --open
```

### Export en PowerPoint
Pour exporter la présentation au format `.pptx` plutôt qu'en HTML,
il suffit de changer l'extension dans la commande de conversion :
```bash
manim-slides convert PartieUne PartieDeux slides.pptx
```
Ou avec une boucle si les scènes sont numérotées :
```bash
manim-slides convert $(for i in {1..5}; do echo Slide$i; done) slides.pptx
```
