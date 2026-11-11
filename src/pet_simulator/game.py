
import pyxel
import json,os, random
from pet_simulator.Kon import KonPet
from pet_simulator.Totoro import TotoroPet
from pet_simulator.Pokemon import PokemonPet

WIDTH = 240
HEIGHT = 180






# GAME Console
# ==========================================

class Game:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.selected = 0
        self.pet = None
        self.delay_frames = 5
        self.state = "LOGO"
        self.logo = "BY HAMED YAZDAN NEJAT"
        self.timer = self.char_index = 0
        self.event = False
        self.eventPublish = False
        pyxel.quit_key = pyxel.KEY_NONE
        
        self.stats = {
            "energy": [],
            "cleanliness": [],
            "hunger": [],
            "happiness": []
        }
        self.categories = list(self.stats.keys())
        self.eventCategory = ""
        self.eventAmount = 0

        self.pet_classes = [
            PokemonPet,
            TotoroPet,
            KonPet
        ]

        self.pet_names = [
            "Pokemon",
            "TOTORO",
            "KON"
        ]
        self.pets = [pet_class() for pet_class in self.pet_classes]
        
    def save_pets(self, filename="pets_save.json"):
            save_data = {
                "selected": self.selected,
                "pets": [pet.to_dict() for pet in self.pets],
            }
            with open(filename, "w") as f:
                json.dump(save_data, f, indent=4)
            print("Game saved successfully!")
            
    def load_pets(self, filename="pets_save.json"):
        if not os.path.exists(filename):
            print("No save file found.")
            return False

        with open(filename, "r") as f:
            save_data = json.load(f)

        self.selected = save_data.get("selected", 0)
        saved_pets_data = save_data.get("pets", [])

        for i, pet_data in enumerate(saved_pets_data):
            if i < len(self.pets):
                self.pets[i].from_dict(pet_data)
                self.pets[i].timer = 0

        #if self.pet is not None:
        self.pet = self.pets[self.selected]
        #self.pet.timer = 0

        print("Game loaded successfully!")
        return True 
            
    def choose_pet(self):        
        self.pet = self.pets[self.selected]
    
    def next_pet(self):

        self.selected = (self.selected + 1) % 3
        self.pet = self.pets[self.selected]


    def trigger_random_event(self):
        chosen_category = random.choice(self.categories)        
        change_val = random.randint(-5, 4)
        event_amount = change_val + 1 if change_val >= 0 else change_val    
        self.stats[chosen_category].append(event_amount)    
        for cat, values in self.stats.items():
            formatted_val = ", ".join(str(x) for x in values)
            print(f"{cat.capitalize()}: {formatted_val}"  f"   mean = {str(round(sum(values)/len(values),2)) if len(values) > 0 else ""}")
            print("--------------------------------------")
        return chosen_category, event_amount

    def update(self):
        if self.state == "lLOGO":
            self.timer += 1

            if self.timer % 5 == 0 and self.char_index < len(self.logo):
                self.char_index += 1

            total_logo_frames = (len(self.logo) * 5) + 60
            if self.timer >= total_logo_frames:
                self.state = "MENU"
        self.state = "MENU"
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
                
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.load_pets()

        else:

            if pyxel.btnp(pyxel.KEY_ESCAPE):
                self.pet = None


            else:
                if (not self.event) and self.pet.timer % (180 * self.pet.speed) == 0 and self.pet.timer >= (180 * self.pet.speed):
                    self.event = True
                    self.eventPublish = True
                    self.eventCategory, self.eventAmount = self.trigger_random_event()

                    #print(self.pet.timer)
                if(self.eventPublish):
                    if(self.pet.timer % (180 * self.pet.speed) == (30 * self.pet.speed)):
                        self.eventPublish = False  
                
                # Next Pet
                if pyxel.btnr(pyxel.KEY_RIGHT):
                    self.next_pet()
                # Prev Pet
                if pyxel.btnr(pyxel.KEY_SPACE):
                    self.save_pets()
                
                if self.pet.is_alive():
                    # Feed
                    if pyxel.btnp(pyxel.KEY_F):
                        self.pet.feed()
            
                    # Play
                    if pyxel.btnp(pyxel.KEY_P):
                        self.pet.play()
            
                    # Sleep
                    if pyxel.btnp(pyxel.KEY_S):
                        self.pet.sleeping = not self.pet.sleeping
            
                    # Clean
                    if pyxel.btnp(pyxel.KEY_C):
                        self.pet.clean()
                    
                for any_pet in self.pets:
                    any_pet.update()
                    if(self.event and any_pet.is_alive()):
                        current_catAmount = any_pet[self.eventCategory]
                        any_pet[self.eventCategory] = self.eventAmount + current_catAmount
                        self.event = False
                #self.pet.update()
    async def  draw_logo(self):
        pyxel.cls(1)
        pyxel.text(75, 20, "PET SIMULATOR", 7)
        
        chars_to_show = min(len(self.logo), pyxel.frame_count // self.delay_frames)
        visible_text = self.logo[:chars_to_show]
        pyxel.text(70, 65, visible_text, 7)
        
        
        
    def draw_menu(self):
        #self.draw_logo()
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

        pyxel.text(35, 160, "ARROWS: MOVE   ENTER: START    SPACE: LOAD", 7)

    def draw(self):
        if self.state == "LOGO":
            pyxel.text(80, 55, "PET SIMULATOR", 10)
            pyxel.text(65, 75, self.logo[: self.char_index], 7)
            if self.timer >= len(self.logo) * 5 + 20:
                pyxel.text(95, 85, "EPITA", 7)
        else:
            if self.pet is None:
                self.draw_menu()
            else:
                self.pet.draw(self.eventPublish, self.eventCategory, self.eventAmount)



# ENTRY POINT
# ==========================================

def main():
    pyxel.init(WIDTH, HEIGHT, title="Pixel Pet Simulator")

    game = Game()

    pyxel.run(game.update, game.draw)


if __name__ == "__main__":
    main()
