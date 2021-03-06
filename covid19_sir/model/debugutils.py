from model.base import logger
from model.human import Human, Adult, K12Student, Toddler, Infant, Elder
from model.location import Location, District, Restaurant


class DebugUtils:
    def __init__(self, model):
        self.humans = []
        self.adults = []
        self.k12students = []
        self.toddlers = []
        self.infants = []
        self.elders = []
        self.locations = []
        self.districts = []
        self.restaurants = []
        self.model = model
        self.human_status = {}
        self.count_school = 0
        self.count_home = 0
        self.count_restaurant = 0
        self.count_work = 0
        self._populate()

    def print_world(self):
        for district in self.districts:
            print("{} District:".format(district.name))
            for i, building in enumerate(district.locations):
                num_humans_in_rooms = [len(room.humans) for room in building.locations]
                print("{0}{1}".format(type(building).__name__, i))
                print(num_humans_in_rooms)
            for i, building in enumerate(district.locations):
                for j, room in enumerate(building.locations):
                    humans_in_rooms = [human.unique_id for human in room.humans]
                    print("{0}{1}-room{2}".format(type(building).__name__, i, j))
                    print(humans_in_rooms)
                humans_in_building = [human.unique_id for human in building.humans]
                print("{0}{1}".format(type(building).__name__, i))
                print(humans_in_building)

    def update_human_status(self):
        for human in self.humans:
            if human not in self.human_status:
                self.human_status[human] = {}
            self.human_status[human][self.model.global_count.day_count] = human.info()

    def update_infection_status(self):
        self.count_school = 0
        self.count_home = 0
        self.count_restaurant = 0
        self.count_work = 0
        for human in self.model.global_count.infection_info:
            location = self.model.global_count.infection_info[human]
            if 'School' in location.strid:
                self.count_school += 1
            elif 'Home' in location.strid:
                self.count_home += 1
            elif 'Restaurant' in location.strid:
                self.count_restaurant += 1
            elif 'Work' in location.strid:
                self.count_work += 1
            else:
                logger.warning(f"Unexpected infection location: {location}")

    def print_infection_status(self):
        self.update_infection_status()
        print(f"School: {self.count_school}")
        print(f"Home: {self.count_home}")
        print(f"Restaurant: {self.count_restaurant}")
        print(f"Work: {self.count_work}")
        print(f"Total: {self.count_school + self.count_home + self.count_restaurant + self.count_work}")

    def _populate(self):
        for agent in self.model.agents:
            if isinstance(agent, Human):
                self.humans.append(agent)
            if isinstance(agent, Adult):
                self.adults.append(agent)
            if isinstance(agent, K12Student):
                self.k12students.append(agent)
            if isinstance(agent, Toddler):
                self.toddlers.append(agent)
            if isinstance(agent, Infant):
                self.infants.append(agent)
            if isinstance(agent, Elder):
                self.elders.append(agent)
            if isinstance(agent, Location):
                self.locations.append(agent)
            if isinstance(agent, District):
                self.districts.append(agent)
            if isinstance(agent, Restaurant):
                self.restaurants.append(agent)
