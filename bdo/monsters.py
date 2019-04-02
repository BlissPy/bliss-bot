import random.randint

class Monster:
    
    def __init__(self, manager, **data):
        self.manager = manager
        
        self.id = data.get("id")
        self.name = data.get("name")
        self.recommended_levels = data.get("recommended_levels")
        self.spawn_locations = [self.manager.get_location(loc) for loc in data.get("spawn_locations")]
        self.rarity = data.get("rarity")
        
        self.min_exp = data.get("min_exp")
        self.max_exp = data.get("max_exp")

    @property
    def exp(self):
        return random.randint(self.min_exp, self.max_exp)
