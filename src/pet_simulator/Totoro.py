import pyxel
from pet_simulator.Basepet import BasePet

class TotoroPet(BasePet):

    def __init__(self):
        super().__init__("Totoro", 13)

        self.hunger_rate = 6
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
            x - 20, y - 20,
            x - 13, y - 43,
            x - 3, y - 20, 13
        )

        pyxel.tri(
            x + 3, y - 20,
            x + 13, y - 43,
            x + 20, y - 20, 13
        )

        # Body
        pyxel.elli(x - 32, y - 25, 64, 65, 13)

        # Belly
        pyxel.elli(x - 21, y + 5, 42, 28, 7)

        # Eyes

        if self.is_alive():
            if self.sleeping:
                    pyxel.line(x - 12, y - 4, x - 5, y - 2, 7)
                    pyxel.line(x + 5, y - 4, x + 12, y - 2, 7)
                    pyxel.text(x + 25, y - 35, "Z Z Z", 7)
            else:
                pyxel.circ(x - 12, y - 5, 3, 7)
                pyxel.circ(x + 12, y - 5, 3, 7)
        else:
            pyxel.line(x - 12, y - 4, x - 5, y - 2, 7)
            pyxel.line(x + 5, y - 4, x + 12, y - 2, 7)



        # Nose
        pyxel.tri(
            x - 3, y + 2,
            x + 3, y + 2,
            x, y + 7, 0
        )

        # Belly markings
        pyxel.line(x - 10, y + 14, x - 5, y + 14, 5)
        pyxel.line(x + 5, y + 14, x + 10, y + 14, 5)

        # Whiskers
        pyxel.line(x - 20, y + 3, x - 30, y, 7)
        pyxel.line(x + 20, y + 3, x + 30, y, 7)

        if self.poop:
            pyxel.circ(x + 40, y + 32, 5, 4)

