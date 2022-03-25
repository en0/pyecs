from pyecs.typing import ISystem, IScene
from ..components import Movement, Transform


class MoveSystem(ISystem):

    def setup(self) -> None:
        ...

    def teardown(self) -> None:
        ...

    def update(self, scene: IScene, frame_delay: float) -> None:
        for entity in scene.get_entities(Movement):
            mov: Movement = entity[Movement]
            xfr: Transform = entity[Transform]
            s = mov.speed * frame_delay
            try:
                x = xfr.position + mov.vector * s
            except:
                import pdb; pdb.set_trace()

            if mov.bounce == True:
                ...
            else:
                ...
            xfr.position = x
