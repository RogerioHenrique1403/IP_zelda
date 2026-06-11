class Configuracao:
    def __init__(self):
        self._largura = 1200
        self._altura = 720
        self._fps = 60

    @property
    def largura(self):
        return self._largura

    @property
    def altura(self):
        return self._altura

    @property
    def fps(self):
        return self._fps
        
