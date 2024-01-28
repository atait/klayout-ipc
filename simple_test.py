from lyipc import kqp
import phidl.geometry as pg
import random

height = random.randint(5, 30)  # Introduce some randomness to see reload better
box = pg.rectangle((20, height))
kqp(box)
