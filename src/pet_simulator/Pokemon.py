import pyxel
from pet_simulator.Basepet import BasePet

class PokemonPet(BasePet):

    def __init__(self):
        super().__init__("Pokemon", 10)

        self.energy_rate = 4
        self.sleep_recovery = 8
    def is_alive(self):
        return super().is_alive()
    
    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        bounded_val = max(0, min(100, int(value)))
        super().__setitem__(key, bounded_val)
        
    def draw_pet(self):
        x, y = 120, 83

        pyxel.elli(x - 30, y + 35, 60, 9, 1)

        # Ears
        pyxel.tri(
            x - 22, y - 15,
            x - 15, y - 35,
            x - 5, y - 15, 10
        )

        pyxel.tri(
            x + 5, y - 15,
            x + 15, y - 35,
            x + 22, y - 15, 10
        )

        # Body
        pyxel.elli(x - 25, y - 22, 50, 60, 10)

        # Eyes
        if self.is_alive():
            if self.sleeping:
                pyxel.line(x - 12, y - 2, x - 5, y - 2, 0)
                pyxel.line(x + 5, y - 2, x + 12, y - 2, 0)
                pyxel.text(x + 25, y - 35, "Z Z", 7)
            else:
                pyxel.pset(x - 9, y - 3, 0)
                pyxel.pset(x + 9, y - 3, 0)
        else:
            pyxel.line(x - 12, y - 2, x - 5, y - 2, 0)
            pyxel.line(x + 5, y - 2, x + 12, y - 2, 0)

        pyxel.circ(x - 15, y + 6, 3, 8)
        pyxel.circ(x + 15, y + 6, 3, 8)

        if self.sleeping and self.is_alive():
            pyxel.text(x + 25, y - 35, "Z Z", 7)

        self.draw_po_poop(x, y)

    def draw_po_poop(self, x, y):
        if self.poop:
            pyxel.circ(x + 40, y + 32, 5, 4)
            pyxel.circ(x + 40, y + 26, 3, 4)

