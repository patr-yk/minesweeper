import types

class MinesweeperSolver:
    def __init__(self, board):
        #initializing requires Board object
        self.__board = board
        self.__height = self.__board.dim_size
        self.__width = self.__board.dim_size
        self.__bombs = self.__board.num_bombs
        self.__mines_found = 0
        self.probabilities = []
        for x in range(self.__height):
            self.probabilities.append([])
            for y in range(self.__width):
                self.probabilities[x].append('?')

    def get_state(self):
        #Method returning current state of board (1 for covered boxes, 0 for uncovered)
        data = self.__board.get_visible_board()
        return data

    def step(self):
        #Method returns list of x and y coordinates to dig.
        #Coordinates are chosen according to counted probabilities.
        #Method returns of the most top left box with the least probability of mine appearance.
        self.predict_probability()

        min_value_position = [0,-1]
        min_value = 1.0
        for x in range(self.__height):
            for y in range(self.__width):
                if self.probabilities[x][y]!='?' and self.probabilities[x][y] < min_value:
                    if self.probabilities[x][y]==0:
                        self.probabilities[x][y]='?'
                        return [x,y]
                    min_value_position[0] = x
                    min_value_position[1] = y
                    min_value = self.probabilities[x][y]
        if min_value!=1.0:
            print("Guessing...")
            self.probabilities[min_value_position[0]][min_value_position[1]]='?'
            return [min_value_position[0],min_value_position[1]]
        self.probabilities[5][5]='?'
        return [5,5]


    def predict_probability(self):

        changes=1
        data = self.get_state()
        while changes != 0:
            changes = 0
            for x in range(self.__height):
                for y in range(self.__width):
                    probability = self.predict_neighbors_probability(x,y)
                    if probability:
                        if probability==2:
                            probability=0
                        neighbors_template = [[x-1, y-1], [x-1, y], [x-1, y+1], [x, y-1], [x, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]]
                        for z in neighbors_template:
                            if z[0]>=0 and z[1]>=0 and z[0]<=self.__height-1 and z[1]<=self.__width-1 and data[z[0]][z[1]]==' ':
                                last_probability = self.probabilities[z[0]][z[1]]
                                if  last_probability=='?' or (float(last_probability)!=0 and float(last_probability)!=1 and float(last_probability)>probability) or (float(probability)==1):
                                    if probability==1:
                                        self.__mines_found=self.__mines_found+1
                                    self.probabilities[z[0]][z[1]] = probability
                                    changes = changes+1

    def predict_neighbors_probability(self, x, y):
        #Method takes coordinates of box as two parameters(x,y).
        #Method returns probability of mine appearance in neighbor boxes according to number of neighboring mines and total number of neighboring boxes.
        #If coordinates are not valid, or there are not covered neighboring boxes, it will return False
        data = self.get_state()
        current_box = [x,y]

        if data[current_box[0]][current_box[1]]!=" " and data[current_box[0]][current_box[1]]!=0 :
            #insert ' ' probability into uncovered box coordinates


            #get lists of all neighboring boxes
            neighbors = []
            neighbors_template = [[x-1, y-1], [x-1, y], [x-1, y+1], [x, y-1], [x, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]]
            for z in neighbors_template:
                if z[0]>=0 and z[1]>=0 and z[0]<=self.__height-1 and z[1]<=self.__width-1:
                    neighbors.append([z[0], z[1], data[z[0]][z[1]]])

            #get amount of neighboring bombs (if current box is uncovered)
            neighbor_mines = int(data[current_box[0]][current_box[1]])

            #get list of coordinates of covered neighbors
            covered_neighbors = []
            for z in neighbors:
                if self.probabilities[z[0]][z[1]]==1:
                    neighbor_mines = neighbor_mines-1
                if z[2] == " " and self.probabilities[z[0]][z[1]]!=1:
                    covered_neighbors.append(z)

            #If there are uncovered neighbors, Method will count probability.
            if len(covered_neighbors) != 0:
                probability = int(neighbor_mines)/int(len(covered_neighbors))
                if probability==0:
                    probability=2
                return probability
            return False
        return False
