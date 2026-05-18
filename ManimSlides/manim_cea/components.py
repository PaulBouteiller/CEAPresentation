"""Composants visuels au style CEA : listes à puces, colonnes, etc."""
from manim import (VMobject,
    Group, VGroup, Text, Dot, Square, Mobject,
    WHITE, BOLD, DOWN, RIGHT, LEFT, UP,
)
from .theme import CEA_RED, CEA_GRAY

def _auto_group(*mobs):
    if all(isinstance(m, VMobject) for m in mobs):
        return VGroup(*mobs)
    return Group(*mobs)

# ----------------------------------------------------------------------
# Listes
# ----------------------------------------------------------------------
def bullet_list(items, color=WHITE, font_size=32, buff_between=0.4,
                indent=0, bullet_style="square"):
    """Liste à puces (carrés rouges) ; les tuples `(item, [sous-items])` créent
    automatiquement un niveau d'indentation."""
    lst = _auto_group()
    for item in items:
        has_sub = isinstance(item, tuple)
        content = item[0] if has_sub else item

        if bullet_style == "square":
            c = CEA_RED if indent == 0 else CEA_GRAY
            bullet = Square(
                side_length=0.12 if indent == 0 else 0.08,
                color=c, fill_opacity=1, stroke_width=0,
            )
        else:
            bullet = Dot(radius=0.06 if indent == 0 else 0.04, color=color)

        txt = (Text(content, color=color, font_size=font_size)
               if isinstance(content, str) else content)
        row = _auto_group(bullet, txt)
        txt.next_to(bullet, RIGHT, buff=0.2)
        lst.add(row)

        if has_sub:
            lst.add(bullet_list(
                item[1], color, font_size * 0.9, buff_between * 0.8,
                indent + 0.8, bullet_style,
            ))

    lst.arrange(DOWN, aligned_edge=LEFT, buff=buff_between)
    lst.to_edge(LEFT, buff=1.5 + indent)
    return lst


def numbered_list(items, color=WHITE, font_size=32, buff_between=0.4):
    """Liste numérotée : numéros rouges en gras, texte blanc."""
    lst = _auto_group()
    for i, item in enumerate(items, 1):
        n = Text(f"{i}.", color=CEA_RED, font_size=font_size, weight=BOLD)
        t = (Text(item, color=color, font_size=font_size)
             if isinstance(item, str) else item)
        row = _auto_group(n, t)
        t.next_to(n, RIGHT, buff=0.3)
        lst.add(row)
    lst.arrange(DOWN, aligned_edge=LEFT, buff=buff_between)
    lst.to_edge(LEFT, buff=1.5)
    return lst


# ----------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------
def two_columns(left, right, buff=1.0):
    """Aligne deux Mobjects côte à côte."""
    return _auto_group(left, right).arrange(RIGHT, buff=buff)


# ----------------------------------------------------------------------
# Items à carré rouge (utile pour mélanger Text / MathTex / VGroup)
# ----------------------------------------------------------------------
def red_square_item(content, color=None, size=0.12, spacing=0.2):
    """Préfixe `content` d'un petit carré rouge."""
    color = color or CEA_RED
    bullet = Square(side_length=size, color=color, fill_opacity=1, stroke_width=0)
    item = _auto_group(bullet, content)
    content.next_to(bullet, RIGHT, buff=spacing)
    if isinstance(content, (VGroup, Group)) and len(content) > 0:
        bullet.move_to(content[0].get_center())
        bullet.align_to(content[0], LEFT).shift(LEFT * (spacing + size / 2))
    return item


def red_square_list(items, buff_horizontal=1.5, buff_between=0.6):
    """Liste de Mobjects préfixés de carrés rouges."""
    lst = _auto_group(*[red_square_item(it) for it in items])
    lst.arrange(DOWN, aligned_edge=LEFT, buff=buff_between)
    lst.to_edge(LEFT, buff=buff_horizontal)
    return lst
