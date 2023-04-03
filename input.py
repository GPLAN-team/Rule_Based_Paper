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
        self.adjacencies.clear()
        for each_list in adjcancy_list:
            adj_list = []

            for each_ele in each_list:
                adj_list.append(each_ele)

            self.adjacencies.append(adj_list)

    def add_non_adjacencies_from(self, non_adjacency_list):
        self.non_adjacencies.clear()
        for each_list in non_adjacency_list:
            nadj_list = []

            for each_ele in each_list:
                nadj_list.append(each_ele)

            self.non_adjacencies.append(nadj_list)
