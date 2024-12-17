from pythreejs import *
import numpy as np

class ThreeDModeler:
    def __init__(self, root):
        self.scene = Scene(children=[AmbientLight(color='#777777')])
        self.camera = PerspectiveCamera(position=[5, 5, 5], up=[0, 0, 1], children=[DirectionalLight(color='white', position=[3, 5, 1], intensity=0.5)])
        self.renderer = Renderer(camera=self.camera, scene=self.scene, background='black', background_opacity=1,
                                 controls=[OrbitControls(controlling=self.camera)])
        self.root = root
        self.embed_3d_view()

    def embed_3d_view(self):
        from IPython.display import display
        widget = self.renderer
        widget.width = 800
        widget.height = 600
        display(widget)

    def add_cube(self, size=1):
        geometry = BoxGeometry(size, size, size)
        material = MeshLambertMaterial(color='red')
        cube = Mesh(geometry, material)
        self.scene.add(cube)