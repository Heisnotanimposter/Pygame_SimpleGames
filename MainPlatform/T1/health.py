
class Health:
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health

    def damage(self, amount):
        self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0  

    def heal(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health 
