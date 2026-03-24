from world.layers.base_layer import BaseLayer


class SurfaceLayer(BaseLayer):
    def __init__(self) -> None:
        super().__init__(layer_name="surface", display_name="поверхность")