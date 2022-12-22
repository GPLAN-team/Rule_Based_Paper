class Input:
    def __init__(self) -> None:
        self.rooms = {}
        self.adjacencies = []
        self.non_adjacencies = []

    def reset(self):
        self.rooms = {}
        self.adjacencies = []
        self.non_adjacencies = []

    def add_rooms_from(self, room_list):
        self.rooms.clear()
        pre = len(self.rooms)
        for i, each_room in enumerate(room_list):
            self.rooms[pre+i] = each_room

    def add_doors_from(self, adjcancy_list):
        for each_list in adjcancy_list:
            int_list = []

            for each_ele in each_list:
                int_list.append(int(each_ele))

            self.adjacencies.append(int_list)
            
    def add_non_adjacencies_from(self, non_adjacency_list):
        for each_list in non_adjacency_list:
            int_list = []

            for each_ele in each_list:
                int_list.append(int(each_ele))

            self.non_adjacencies.append(int_list)


        
        

