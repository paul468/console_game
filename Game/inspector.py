class inspector:
    def __init__(self, map, stats):
        self.map = map
        self.interface = []
        self.stats = stats
    def generate_interface(self):
        for i in self.map:
            if i == "=":
                self.interface.append("Non-interactable")
            elif i == "0":
                self.interface.append("Interactable")
            elif i == "G":
                final = f"Enemy: Stats:\n[ He is 1 out of {self.stats['enemies']}, he is on level {self.stats['people']*10}]"
                self.interface.append(final)
