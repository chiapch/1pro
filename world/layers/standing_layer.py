from world.layers.base_layer import BaseLayer


class StandingLayer(BaseLayer):
    def __init__(self) -> None:
        super().__init__(layer_name="standing", display_name="standing")