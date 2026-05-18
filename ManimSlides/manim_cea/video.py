"""VideoMobject : afficher une vidéo comme un ImageMobject animé."""
from dataclasses import dataclass
import numpy as np
import cv2
from PIL import Image
from manim import ImageMobject, change_to_rgba_array


@dataclass
class _VideoStatus:
    time: float = 0
    videoObject: object = None
    loop_count: int = 0

    def __deepcopy__(self, memo):
        return self


class VideoMobject(ImageMobject):
    """Lit une vidéo (via OpenCV) et la rend image par image dans la Scene.

    Paramètres
    ----------
    filename : str
        Chemin vers le fichier vidéo.
    imageops : callable, optionnel
        Fonction PIL -> PIL appliquée à chaque frame.
    speed : float
        Multiplicateur de vitesse de lecture.
    loop : bool | int
        `True` pour boucler indéfiniment, un entier pour un nombre fini de
        boucles, `False` pour ne pas boucler.
    """

    def __init__(self, filename=None, imageops=None, speed=1.0, loop=False, **kwargs):
        self.filename = filename
        self.imageops = imageops
        self.speed = speed
        self.loop = (
            float("inf") if loop is True
            else (int(loop) if isinstance(loop, (int, float)) else 0)
        )

        self.status = _VideoStatus()
        self.status.videoObject = cv2.VideoCapture(filename)
        self.status.videoObject.set(cv2.CAP_PROP_POS_FRAMES, 1)
        ret, frame = self.status.videoObject.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            if imageops is not None:
                img = imageops(img)
        else:
            img = Image.fromarray(np.uint8([
                [63,   0,   0,   0],
                [0,  127,   0,   0],
                [0,    0, 191,   0],
                [0,    0,   0, 255],
            ]))

        super().__init__(img, **kwargs)
        if ret:
            self.add_updater(self._updater)

    def _updater(self, mobj, dt):
        if dt == 0:
            return
        s = self.status
        s.time += 1000 * dt * mobj.speed
        s.videoObject.set(cv2.CAP_PROP_POS_MSEC, s.time)
        ret, frame = s.videoObject.read()

        if not ret and s.loop_count < self.loop:
            s.loop_count += 1
            s.time = 0
            s.videoObject.set(cv2.CAP_PROP_POS_MSEC, s.time)
            ret, frame = s.videoObject.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            if mobj.imageops is not None:
                img = mobj.imageops(img)
            mobj.pixel_array = change_to_rgba_array(
                np.asarray(img), mobj.pixel_array_dtype,
            )
