import pyxel
import math
WIDTH = 240
HEIGHT = 180
class BasePet:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.state = "alive"

        self.hunger = 20
        self.happiness = 80
        self.energy = 80
        self.cleanliness = 100
        self.speed = 2

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


    def __getitem__(self, key):
        match key:
            case "energy":
                return self.energy
            case "cleanliness":
                return self.cleanliness
            case "hunger":
                return self.hunger
            case "happiness":
                return self.happiness
            case _:
                raise("Unknown category")  

    def __setitem__(self, key, value):
        match key:
            case "energy":
                self.energy = max(0, min(100, value))                
            case "cleanliness":
                self.cleanliness = max(0, min(100, value))
            case "hunger":
                self.hunger = max(0, min(100, value))
            case "happiness":
                self.happiness = max(0, min(100, value))
            case _:
                raise("Unknown category") 
        
        
    def update(self):
        if(self.state == "dead"):
            return
        self.timer += (self.speed)
        if(self.hunger == 100 or self.happiness == 0 or self.energy == 0 or self.cleanliness == 0):
            self.state = "dead"
            self.hunger = 100
            self.happiness = 0 
            self.energy = 0
            self.cleanliness = 0
            self.sleeping = True
            return

          
            
        if self.timer % 120 == 0:
            self.hunger = min(
                100, self.hunger + self.hunger_rate
            )

            self.happiness = max(
                0, self.happiness - self.happiness_rate
            )

            self.cleanliness = max(
                0, self.cleanliness - 2
            )

            if self.sleeping:
                self.energy = min(
                    100, self.energy + self.sleep_recovery
                )
            else:
                self.energy = max(
                    0, self.energy - self.energy_rate
                )
                
        

        # Poop
        if self.timer % int(1800/self.hunger_rate) == 0:
            if(self.poop):
                self.cleanliness = max(
                    0, self.cleanliness - 20
                    )
            else:
                self.poop = True
                self.cleanliness = max(
                    0, self.cleanliness - 10
                )

        if self.cleanliness < 30:
            self.happiness = max(
                0, self.happiness - 10
            )

    def feed(self):
        if not self.sleeping:
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

    def draw_Report(self):
        report = f"HUNGER = {self.hunger} Energy = {self.energy} Cleanliness = {self.cleanliness} Sleeping = {self.sleeping}"
    
    def draw_random_event(self, x, y, amount, category, color = 10):
        points = [
            (15, 0),  (4, 10),  (11, 10),  (0, 25),  (9, 14),  (2, 14), 
        ]
        num_points = len(points)
        for i in range(num_points):
            p1 = points[i]
            p2 = points[(i + 1) % num_points] 
            pyxel.line(x + p1[0], y + p1[1],
                       x + p2[0], y + p2[1],
                       color)
        # OUTLINE
        pyxel.text(x + 20 , y + 7.5,
                   f"{"+" if amount > 0 else "-"}{int(math.fabs(amount))} {category}"
                   , color)

        
    def is_alive(self):
        return self.state == "alive"

    def draw_pixel_arrow(self, x, y, color=7):
        pyxel.line(x, y + 2, x + 8, y + 2, color)
        pyxel.tri(x + 11, y + 2, x + 7, y, x + 7, y + 4, color)
        
    def draw_cross(self, x, y, color=8):
        for offset in range(4):
            pyxel.line(x + offset, y, x + 16 + offset, y + 16, color)
        for offset in range(4):
            pyxel.line(x + offset, y + 16, x + 16 + offset, y, color)

        pyxel.text(x - 10, y + 24, "NOT ALIVE!", 8)
        
    # Drawing common interface
    def draw(self, event = False, cat ="", amount = 0):
        pyxel.cls(12)

        pyxel.rect(0, 125, WIDTH, 55, 4)
        
        pyxel.line(0, 125, WIDTH, 125, 7)
        pyxel.text(205, 80, "NEXT PET", 7)
        self.draw_pixel_arrow(225,70,7)

        self.draw_pet()
        

        pyxel.text(85, 5, self.name.upper(), 7)
        pyxel.text(175, 5, f"CARE:{self.score}", 7)
        pyxel.text(5, 5, "ESC: EXIT", 7)        

        if self.state == "dead":
            mood = "DEAD"
            self.draw_cross(65,65)
            self.draw_pet()
        else:
            if(event):
                self.draw_random_event(30, 30, amount, cat)
                
            pyxel.text(55, 45, "F: FEED", 7)
            pyxel.text(55, 55, "P: PLAY", 7)
            pyxel.text(55, 65, "S: SLEEP", 7)
            pyxel.text(55, 75, "C: CLEAN", 7)
            pyxel.text(2,172, "PRESS (SPACE) TO SAVE",7)


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

        self.draw_bar(5, 140, "FOOD", 100 - self.hunger, 8)
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
        
    def to_dict(self):
        return {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "cleanliness": self.cleanliness,
            "sleeping": self.sleeping,
            "poop": self.poop,
            "score": self.score,
            "timer": self.timer,
        }

    def from_dict(self, data):
        self.hunger = data.get("hunger", self.hunger)
        self.happiness = data.get("happiness", self.happiness)
        self.energy = data.get("energy", self.energy)
        self.cleanliness = data.get("cleanliness", self.cleanliness)
        self.sleeping = data.get("sleeping", self.sleeping)
        self.poop = data.get("poop", self.poop)
        self.score = data.get("score", self.score)
        self.timer = data.get("timer", self.timer)
        
    # Each subclass implements its own appearance
    def draw_pet(self):
        raise NotImplementedError(
            "Each pet must implement draw_pet()"
        )

