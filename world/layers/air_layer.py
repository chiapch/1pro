from world.layers.base_layer import BaseLayer


class AirLayer(BaseLayer):
    def __init__(self) -> None:
        super().__init__(layer_name="air", display_name="воздух")