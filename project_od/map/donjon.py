
class DonjonRoom:
    """A template for a donjonRoom
    """
    def __init__(self, x : int, y : int, shape : list[bool] =[True, True, True, True]) -> None:
        """
        Args:
            x (int): x coord
            y (int): y coord
            shape (list[bool], optional): Describe the shape True is a door and false a wall. It's left, top, right, bottom. Defaults to [True, True, True, True].
        """
        self.shape = shape
        self.next_room = [None for _ in range(4)]
        self.x = x
        self.y = y
        self.loaded : bool = False
    
    def __hash__(self) -> int:
        return hash((self.x,self.y))
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, DonjonRoom):
            return (self.x, self.y) == (__o.x, __o.y)
        return False

    def on_load(self) -> None:
        pass

class RoomGenerator:
    """Generate the Room.
        'next' need to be overridden
    """
    def next(self, x : int, y : int, rules : list[bool], dir : int, *args, **kwargs) -> DonjonRoom:
        """Give an instance of a child of DonjonRoom
            Need to be override

            rules describe the shape of the room, it has a length of 4,
            where:
                0 is left,
                1 is top,
                2 is right,
                3 is bottom
            it can have 3 possibility :
                True there is a door,
                False there is a wall,
                None it's up to the generator to choose

        Args:
            x (int): the room is at x
            y (int): the room is at y
            rules (list[bool]): shape that the room can take
            dir (int): dir from where it come

        Returns:
            LazyRoom: The room instantiate
        """
        return DonjonRoom(x, y)

class Donjon:
    """Generate a donjon at need
    """
    def __init__(self, generator : RoomGenerator, minimum_rooms : int = 0, maximum_rooms : int = 150) -> None:
        self.generator = generator
        self.min_rooms = minimum_rooms
        self.max_rooms = maximum_rooms
        self.rooms : dict[tuple[int, int], DonjonRoom] = {}
        self.to_create : set[tuple[int, int]] = {(0,0)}
        self.nb_loaded : int = 0
        self.get(0,0)
    
    def get(self, x : int, y : int) -> DonjonRoom:
        """Get the room at the coordinate, load it if it's not already

        Args:
            x (int): x coord
            y (int): y coord

        Returns:
            LazyRoom: The room asked
        """
        room = self.rooms.get((x,y), None)
        if room == None or room.loaded == False:
            self.load_room(x,y)
        return room
    
    def load_room(self, x : int, y: int) -> None:
        """Load the room at x, y and create it's neighboors

        Args:
            x (int): x coord
            y (int): y coord
        """
        if (x,y) not in self.rooms: # Not created
            # Neighbors coordinate
            neighborhood = (x-1,y),(x, y-1),(x+1,y),(x,y+1)
            # Neighbor room
            neighbors = [self.rooms.get(k, None) for k in neighborhood]
            # Can have a room in the direction
            rules = [r.shape[(j+2)%4] if r != None else None for j, r in enumerate(neighbors)]
            # Create the room
            room = self.generator.next(x,y, rules=rules, dir=-1)

            # Add the neighbor to the set (for counting purpose)
            for j, ope in enumerate(room.shape):
                if ope and neighborhood[j] not in self.rooms:
                    self.to_create.add(neighborhood[j])
            self.rooms[(x,y)] = room
        else: # Already created
            room = self.rooms[(x,y)]

        x, y = room.x, room.y

        room.loaded = True
        room.on_load()
        self.nb_loaded += 1

        self.to_create.remove((x,y))

        # Create the next room
        for i, (xr,yr) in enumerate(((x-1,y),(x, y-1),(x+1,y),(x,y+1))):
            # If there is a door and the neighbor doesn't exist
            if room.shape[i] and room.next_room[i] == None and (xr,yr) not in self.rooms:

                neighborhood = (xr-1,yr),(xr, yr-1),(xr+1,yr),(xr,yr+1)
                neighbors = []
                rules = []
                authorized_door =  self.max_rooms - self.get_num_estimate_size()
                for j, k in enumerate(neighborhood):
                    r = self.rooms.get(k, None)
                    neighbors.append(r)
                    if r != None:
                        # There is a neighbor, make a wall if he has, or a door, be like him !
                        # Why would you have a personality ?
                        rules.append(r.shape[(j+2)%4])
                    else:
                        rule = False
                        
                        if authorized_door > 0: #Can generate more
                            if self.get_num_estimate_size() < self.min_rooms and self.get_num_border() == 1: #Have to generate more
                                    rule = True
                            else:
                                rule = None
                            authorized_door -= 1
                        rules.append(rule)

                # Create the room
                r = self.generator.next(x=xr, y=yr, dir=i, rules=rules)

                # Add the neighbor to the set (for counting purpose)
                for j, ope in enumerate(r.shape):
                    if ope and neighborhood[j] not in self.rooms:
                        self.to_create.add(neighborhood[j])
                

                self.rooms[(xr,yr)] = r
                
                # Link the room
                for j, sr in enumerate(neighbors):
                    if sr != None:
                        sr.next_room[(j+2)%4] = r
                        r.next_room[j] = sr

    def get_num_loaded(self) -> int:
        """Number of room that has been loaded

        (loaded = True)
        """
        return self.nb_loaded
    
    def get_num_created(self) -> int:
        """Number of room that has been created

        (init)
        """
        return len(self.rooms)

    def get_num_to_create(self) -> int:
        """Number of room that has not been explored

        (not loaded or not created but a door to that place exist)
        """
        return len(self.to_create)
    
    def get_num_unloaded(self) -> int:
        """Number of room that has been created but not loaded

        (loaded = False)
        """
        return self.get_num_created()-self.get_num_loaded()

    def get_num_border(self) -> int:
        """Number of room that has not been created yet but a door exist to that place
        """
        return self.get_num_to_create()-self.get_num_unloaded()

    def get_num_estimate_size(self) -> int:
        """The size that the donjon has if all the new room are closed
        """
        return self.get_num_loaded() + self.get_num_to_create()
    
    def get_size(self) -> int:
        """The number of room
        """
        return self.get_num_created()