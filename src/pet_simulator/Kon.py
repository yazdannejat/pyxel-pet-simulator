
import pyxel
from pet_simulator.Basepet import BasePet

class KonPet(BasePet):

    def __init__(self):
        super().__init__("Kon", 9)

        self.happiness_rate = 4
        self.play_bonus = 25
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
        pyxel.circ(x - 22, y - 20, 12, 4)
        pyxel.circ(x + 22, y - 20, 12, 4)

        # Mane
        pyxel.circ(x, y - 5, 32, 4)
        pyxel.circ(x - 23, y + 8, 12, 4)
        pyxel.circ(x + 23, y + 8, 12, 4)

        # Face
        pyxel.elli(x - 20, y - 20, 40, 42, 9)

        # Eyes

        if self.is_alive():
            if self.sleeping: 
                pyxel.line(x - 9, y - 5, x - 5, y + 2, 0)
                pyxel.line(x + 5, y - 5, x + 9, y + 2, 0)
                pyxel.text(x + 25, y - 30, "ZZ ZZ", 7)
            else:
                pyxel.circ(x - 9, y - 5, 3, 0)
                pyxel.circ(x + 9, y - 5, 3, 0)
        else:
            pyxel.line(x - 9, y - 5, x - 5, y + 2, 0)
            pyxel.line(x + 5, y - 5, x + 9, y + 2, 0)


        # Nose and mouth
        pyxel.circ(x, y + 4, 3, 0)
        pyxel.line(x, y + 7, x, y + 12, 0)
        pyxel.line(x, y + 12, x - 5, y + 14, 0)
        pyxel.line(x, y + 12, x + 5, y + 14, 0)

        if self.poop:
            pyxel.circ(x + 40, y + 32, 5, 4)

