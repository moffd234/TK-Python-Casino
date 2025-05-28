class Category:
    def __init__(self, name: str, id_num: int, easy_num: int, med_num: int, hard_num: int):
        self.name: str = name
        self.id: int = id_num
        self.easy_num: int = easy_num
        self.med_num: int = med_num
        self.hard_num: int = hard_num

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "easy_num": self.easy_num,
            "med_num": self.med_num,
            "hard_num": self.hard_num
        }
