class Input:
    def __init__(self) -> None:
        self.rooms = {}
        self.adjacencies = []

    def reset(self):
        self.rooms = {}
        self.adjacencies = []

    def add_rooms_from(self, room_list):
        pre = len(self.rooms)
        for i, each_room in enumerate(room_list):
            self.rooms[pre+i] = each_room

    def add_rules_from(self, adjcancy_list):
        for each_list in adjcancy_list:
            int_list = []

            for each_ele in each_list:
                int_list.append(int(each_ele))

            self.adjacencies.append(int_list)


        
        

