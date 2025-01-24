import json
import os


class Player:
    def __init__(self, id):
        self.id = id

        config_path = os.path.join(os.getcwd(), "configuration/config.json")
        with open(config_path, 'r') as file:
            data = json.load(file)
        self.number_barrier = data['number_barrier']

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_barrier(self):
        return self.number_barrier

    def decrement_barrier(self):
        self.number_barrier -= 1

    def have_enough_barrier(self):
        return self.number_barrier != 0

