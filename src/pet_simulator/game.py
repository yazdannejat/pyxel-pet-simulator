
import pyxel


WIDTH = 240
HEIGHT = 180


# ==========================================
# BASE CLASS
# ==========================================

class BasePet:

    def __init__(self, name, color):
        self.name = name
        self.color = color

        self.hunger = 20
        self.happiness = 80
        self.energy = 80
        self.cleanliness = 100

        self.sleeping = False
        self.poop = False
        self.score = 0
        self.timer = 0

        # Personality parameters
        self.hunger_rate = 2
        self.energy_rate = 2
        self.happiness_rate = 1
        self.sleep_recovery = 5
        self.play_bonus = 10

    # --------------------------------------
    # Common behaviour
    # --------------------------------------

    def update(self):
        self.timer += 1

        if self.timer % 120 == 0:
            self.hunger = min(
                100, self.hunger + self.hunger_rate
            )

            self.happiness = max(
                0, self.happiness - self.happiness_rate
            )

            self.cleanliness = max(
                0, self.cleanliness - 1
            )

            if self.sleeping:
                self.energy = min(
                    100, self.energy + self.sleep_recovery
                )
            else:
                self.energy = max(
                    0, self.energy - self.energy_rate
                )

        # Feed
        if pyxel.btnp(pyxel.KEY_F):
            self.feed()

        # Play
        if pyxel.btnp(pyxel.KEY_P):
            self.play()

        # Sleep
        if pyxel.btnp(pyxel.KEY_S):
            self.sleeping = not self.sleeping

        # Clean
        if pyxel.btnp(pyxel.KEY_C):
            self.clean()

        # Poop
        if self.timer % 900 == 0:
            self.poop = True
            self.cleanliness = max(
                0, self.cleanliness - 10
            )

        if self.cleanliness < 30:
            self.happiness = max(
                0, self.happiness - 1
            )

    def feed(self):
        self.hunger = max(0, self.hunger - 25)
        self.happiness = min(100, self.happiness + 5)
        self.score += 1

    def play(self):
        if not self.sleeping and self.energy >= 10:
            self.happiness = min(
                100, self.happiness + self.play_bonus
            )
            self.energy = max(0, self.energy - 10)
            self.hunger = min(100, self.hunger + 5)
            self.score += 5

    def clean(self):
        self.cleanliness = 100
        self.poop = False
        self.happiness = min(100, self.happiness + 5)

    # --------------------------------------
    # Drawing common interface
    # --------------------------------------

    def draw(self):
        pyxel.cls(12)

        pyxel.rect(0, 125, WIDTH, 55, 4)
        pyxel.line(0, 125, WIDTH, 125, 7)

        self.draw_pet()

        pyxel.text(85, 5, self.name.upper(), 7)
        pyxel.text(175, 5, f"CARE:{self.score}", 7)

        pyxel.text(55, 45, "F: FEED", 7)
        pyxel.text(55, 55, "P: PLAY", 7)
        pyxel.text(55, 65, "S: SLEEP", 7)
        pyxel.text(55, 75, "C: CLEAN", 7)
        pyxel.text(5, 5, "ESC: BACK", 7)

        if self.sleeping:
            mood = "SLEEPING"
        elif self.hunger > 70:
            mood = "HUNGRY!"
        elif self.happiness < 30:
            mood = "SAD!"
        elif self.energy < 20:
            mood = "TIRED!"
        else:
            mood = "HAPPY!"

        pyxel.text(100, 115, mood, 7)

        self.draw_bar(5, 140, "FOOD", self.hunger, 8)
        self.draw_bar(125, 140, "HAPPY", self.happiness, 11)
        self.draw_bar(5, 153, "ENERGY", self.energy, 10)
        self.draw_bar(125, 153, "CLEAN", self.cleanliness, 9)

    def draw_bar(self, x, y, label, value, color):
        pyxel.text(x, y, label, 7)
        pyxel.rect(x + 45, y, 55, 7, 1)
        pyxel.rect(
            x + 45, y, value * 55 // 100, 7, color
        )
        pyxel.rectb(x + 45, y, 55, 7, 7)

    # Each subclass implements its own appearance
    def draw_pet(self):
        raise NotImplementedError(
            "Each pet must implement draw_pet()"
        )


# ==========================================
# SLEEPY PET
# ==========================================

class SleepyPet(BasePet):

    def __init__(self):
        super().__init__("Sleepy", 10)

        self.energy_rate = 4
        self.sleep_recovery = 8

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
        if self.sleeping:
            pyxel.line(x - 12, y - 2, x - 5, y - 2, 0)
            pyxel.line(x + 5, y - 2, x + 12, y - 2, 0)
        else:
            pyxel.pset(x - 9, y - 3, 0)
            pyxel.pset(x + 9, y - 3, 0)

        pyxel.circ(x - 15, y + 6, 3, 8)
        pyxel.circ(x + 15, y + 6, 3, 8)

        if self.sleeping:
            pyxel.text(x + 25, y - 35, "Z Z", 7)

        self.draw_po_poop(x, y)

    def draw_po_poop(self, x, y):
        if self.poop:
            pyxel.circ(x + 40, y + 32, 5, 4)
            pyxel.circ(x + 40, y + 26, 3, 4)


# ==========================================
# TOTORO
# ==========================================

class TotoroPet(BasePet):

    def __init__(self):
        super().__init__("Totoro", 13)

        self.hunger_rate = 6

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
        pyxel.circ(x - 12, y - 5, 3, 7)
        pyxel.circ(x + 12, y - 5, 3, 7)

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


# ==========================================
# KON
# ==========================================

class KonPet(BasePet):

    def __init__(self):
        super().__init__("Kon", 9)

        self.happiness_rate = 4
        self.play_bonus = 25

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
        pyxel.circ(x - 9, y - 5, 3, 0)
        pyxel.circ(x + 9, y - 5, 3, 0)

        # Nose and mouth
        pyxel.circ(x, y + 4, 3, 0)
        pyxel.line(x, y + 7, x, y + 12, 0)
        pyxel.line(x, y + 12, x - 5, y + 14, 0)
        pyxel.line(x, y + 12, x + 5, y + 14, 0)

        if self.poop:
            pyxel.circ(x + 40, y + 32, 5, 4)


# ==========================================
# GAME MANAGER
# ==========================================

class Game:

    def __init__(self):
        self.selected = 0
        self.pet = None

        self.pet_classes = [
            SleepyPet,
            TotoroPet,
            KonPet
        ]

        self.pet_names = [
            "SLEEPY",
            "TOTORO",
            "KON"
        ]

    def choose_pet(self):
        pet_class = self.pet_classes[self.selected]
        self.pet = pet_class()

    def update(self):

        if self.pet is None:

            if pyxel.btnp(pyxel.KEY_LEFT):
                self.selected = (self.selected - 1) % 3

            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.selected = (self.selected + 1) % 3

            if pyxel.btnp(pyxel.KEY_1):
                self.selected = 0
                self.choose_pet()

            if pyxel.btnp(pyxel.KEY_2):
                self.selected = 1
                self.choose_pet()

            if pyxel.btnp(pyxel.KEY_3):
                self.selected = 2
                self.choose_pet()

            if pyxel.btnp(pyxel.KEY_RETURN):
                self.choose_pet()

        else:

            if pyxel.btnp(pyxel.KEY_ESCAPE):
                self.pet = None
            else:
                self.pet.update()

    def draw_menu(self):
        pyxel.cls(1)

        pyxel.text(75, 15, "CHOOSE YOUR PET", 7)

        for i, name in enumerate(self.pet_names):
            x = 12 + i * 76

            color = 5 if i == self.selected else 13

            pyxel.rect(x, 48, 66, 95, 0)
            pyxel.rectb(x, 48, 66, 95, color)

            pyxel.text(x + 12, 65, name, 7)

            if i == 0:
                pyxel.text(x + 5, 90, "SLEEPY", 10)
            elif i == 1:
                pyxel.text(x + 5, 90, "HUNGRY", 13)
            else:
                pyxel.text(x + 5, 90, "PLAYFUL", 9)

            if i == self.selected:
                pyxel.text(x + 18, 120, "SELECT", 11)

        pyxel.text(55, 160, "ARROWS: MOVE   ENTER: START", 7)

    def draw(self):
        if self.pet is None:
            self.draw_menu()
        else:
            self.pet.draw()


# ==========================================
# ENTRY POINT
# ==========================================

def main():
    pyxel.init(WIDTH, HEIGHT, title="Pixel Pet Simulator")

    game = Game()

    pyxel.run(game.update, game.draw)


if __name__ == "__main__":
    main()
