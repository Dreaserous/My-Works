""" RailYard """

class RailYard():
    def __init__(self, file_name):
        self.file_name = file_name

        with open(r"{}".format(file_name)) as file:
            tracks = file.readlines()
            yard = []
            
            for i in tracks:
                if i[len(i)-1] == '\n':
                    i = i[0 : len(i)-1]
                    yard.append(i)
                else:
                    yard.append(i)

            print("\nYard Initialized\n")

        self.yard = yard

    def __len__(self):
        return len(self.yard)

    def width(self):
        width_list_top = []
        for i in self.yard:
            width_list_bottom = []
            if len(self.yard[0]) != len(i):
                for i in self.yard:
                    width_list_bottom.append(len(i))
                return width_list_bottom

            width_list_top.append(len(i))
        return width_list_top

    def num_loco(self):
        locos = 0
        for i in self.yard:
            if i[len(i)-2] == 'T':
                locos += 1

        return locos

    def destinations(self, track):
        self.dest_list = ['-', 'T']

        for j in track:
            if j not in self.dest_list:
                self.dest_list.append(j)
        return len(self.dest_list) - 2

    def num_of_cars(self, track):
        un_list = []

        self.destinations(track)

        for i in self.dest_list:
            if i not in '-T':
                un_list.append(track.count(i))

        return sum(un_list)

    def display(self):
        dest_count = []
        track_no = 1
        for i in self.yard:
            print(track_no, ":", i)
            track_no += 1
            dest_count.append(self.destinations(i))

        print("\nLocomotive Count:", self.num_loco())
        print("Destination Count:", max(dest_count), "\n")

    def rule_check(self, num_mov, start, end):
        return ((self.num_of_cars(self.yard[start-1]) >= num_mov) and 
            (self.num_of_cars(self.yard[end-1]) + num_mov <= self.width()[end-1] - 2) and 
            ('T' not in self.yard[end-1]) and 
            ('T' in self.yard[start-1]))

    def move(self, num_mov, start, end):
        if self.rule_check(num_mov, start, end):
            temp_len = len(self.yard[start-1])
            objects = self.yard[start-1][temp_len-2: temp_len-num_mov-3: -1]

            start_list = list(self.yard[start-1])
            end_list = list(self.yard[end-1])
            object_list = list(objects)
            object_list.reverse()

            for i in range(len(object_list)):
                end_list.insert(len(end_list)-1, object_list[i])
                end_list.pop(0)

                start_list.pop(len(start_list)-2)
                start_list.insert(0, '-')

            end_str = ''
            for i in end_list:
                end_str += i

            start_str = ''
            for i in start_list:
                start_str += i

            self.yard[end-1] = end_str
            self.yard[start-1] = start_str
            self.display()

        else:
            print("ERROR: Player request denied due to GameRuleRestrictions\n")

    def departure(self):
        departed = False
        iteration = 0
        numcar = 1
        for i in self.yard:
            if self.destinations(i) == 1 and 'T' in i:
                numcar = self.num_of_cars(self.yard[iteration])
                self.yard[iteration] = "-" * self.width()[iteration]
                departed = True
                self.display()
                break

            iteration += 1

        return departed, iteration, numcar

    def win_cond(self):
        win_var = 0
        for i in self.yard:
            win_var += self.destinations(i)

        if win_var == 0:
            return True

        return False



if __name__ == "__main__":
    filename = input("Enter file name: ")
    layout = RailYard(filename)
    layout.display()

    if layout.width().count(layout.width()[0]) == len(layout.width()):
        print("Length of Yard Tracks are:", int(layout.width()[0]))
    else:
        print("The Yard Tracks are of varying lengths:", layout.width())

    game_on = True

    while game_on:
        if layout.num_loco() == 0:
            print("All locomotives have departed!\nGame Over...")
            game_on = False
            continue

        elif layout.win_cond():
            print("\nRailyard Conquered!\nClosing Program...")

            game_on = False

        command = input("\nWhat is your command?\n").split()

        if command[0] == 'move':
            try:
                mov_obj, strack, etrack = int(command[1]), int(command[2]), int(command[3])
            except:
                print("ERROR: Invalid Movement Values")
                continue

            layout.move(mov_obj, strack, etrack)
            departed, iteration, numcar = layout.departure()
            if departed:
                print("**ALERT** Locomotive departed in lane {} with {} cars **ALERT**".format(iteration+1, numcar))

        elif command[0] == 'quit':
            print("Quitting...")
            game_on = False
            continue

        else:
            print("ERROR: Invalid Command")
