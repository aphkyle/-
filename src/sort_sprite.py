from pathlib import Path


class SortName:
    def __init__(self, name):
        name = Path(name).name
        self.filename, x, y, width, height, *_ = name.split("-")
        x, y, width, height = map(int, (x, y, width, height))
        self.x, self.y, self.width, self.height = x, y, width, height
        if self.filename == "Treasure+.png":
            self.id = x // 16 + y
        else:
            self.id = x // 16 + y // 2
        self.conv_dict = {
            "Treasure+.png": {
                # i dont want gold to be too op
                # so i adjusted the price and made some stuff more valuable
                10: {"name": "A LARGE PILE OF GOLD", "price": 3000, "grab_time": 10},
                11: {"name": "A PILE OF GOLD", "price": 2000, "grab_time": 6.67},
                34: {"name": "3 SMALL PIECES OF COPPER", "price": 300, "grab_time": 1},
                38: {
                    "name": "10 SMALL PIECES OF COPPER",
                    "price": 1000,
                    "grab_time": 1.25,
                },
                42: {"name": "A LARGE PILE OF COPPER", "price":2500, "grab_time":10},
                51: {"name": "4 GOLD BARS", "price": 1800, "grab_time": 5},
                52: {"name": "1 SILVER BAR", "price": 400, "grab_time": 0.7},
                55: {"name": "4 SILVER BARS", "price": 1600, "grab_time": 2.8},
                84: {"name": "GOLDEN NECKLACE", "price": 800, "grab_time": 0.5},
                101: {"name": "ANCIENT PHARAOH MASK", "price": 3000, "grab_time": 15},
                116: {
                    "name": "ANCIENT MAMMOTH\nSKULPTURE",
                    "price": 3000,
                    "grab_time": 15,
                },
                117: {
                    "name": "ANCIENT HORUS SKULPTURE",
                    "price": 3000,
                    "grab_time": 15,
                },
                122: {
                    # sorry, i really cant know what this one is
                    "name": "ANCIENT ??? SKULPTURE",
                    "price": 3000,
                    "grab_time": 15,
                },
                134: {"name": "MONEY BAG", "price": 2500, "grab_time": 3},
                145: {"name": "WOODEN TREASURE BOX", "price":2500, "grab_time": 10},
                161: {"name": "GOLDEN TREASURE BOX", "price":2700, "grab_time": 10},
                177: {"name": "SILVER TREASURE BOX", "price":2600, "grab_time": 10},
                198: {"name": "WINE", "price": 1000, "grab_time": 0.5},
                255: {"name": "ANCIENT GOLDEN POOP", "price": -1000, "grab_time": 0.1},
            },
            "indoor.png": {
                143: {"name": "EXIT", "price":0, "grab_time":2},
                178: {"name": "DOOR", "lockpick_time": (5, 5)},
                179: {"name": "BETTER DOOR", "lockpick_time": (9, 11)},
                180: {"name": "DOOR", "lockpick_time": (7, 9)},
                187: {
                    "name": "BOOKSHELF",
                    "price": 500,
                    "grab_time": 5,
                },
                188: {"name": "CABINET", "price": 300, "grab_time": 5},
                189: {"name": "STOOL", "price": 50, "grab_time": 0.1},
                191: {"name": "TABLE", "price": 50, "grab_time": 1},
                194: {"name": "TOILET", "price": 500, "grab_time": 10},
                196: {"name": "GRASS POT", "price": 300, "grab_time": 1},
                197: {"name": "PINK ROSE POT", "price": 300, "grab_time": 1},
                198: {"name": "RED ROSE POT", "price": 300, "grab_time": 1},
            },
        }

    def get_sprite_info(self):
        return self.conv_dict[self.filename][self.id]
