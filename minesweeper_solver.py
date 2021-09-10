"""
I am sorry for missing 'j' characters. My 'j' key is on keyboard is not working properly.
"""
import types

class MinesweeperSolver:
    def __init__(self, board):
        #initializing requires Board object
        self.__board = board
        self.__height = self.__board.dim_height
        self.__width = self.__board.dim_width
        self.__bombs = self.__board.num_bombs
        self.__mines_found = 0
        self.probabilities = []
        for x in range(self.__height):
            self.probabilities.append([])
            for y in range(self.__width):
                self.probabilities[x].append('?')

    def get_state(self):
        #Returns of state of game at the moment (1 for covered boxes, 0 for uncovered)
        data = self.__board.get_visible_board()
        return data

    def step(self):
        #Method returns list of x and y coordinates to dig.
        self.predict_probability()
        min_value_position = [0,-1]
        min_value = 1.0
        for x in range(self.__height):
            #print(x)
            for y in range(self.__width):
                #print(y)
                if self.probabilities[x][y]!='?' and self.probabilities[x][y] < min_value:
                    if self.probabilities[x][y]==0:
                        self.probabilities[x][y]='?'
                        return [x,y]
                    min_value_position[0] = x
                    min_value_position[1] = y
                    min_value = self.probabilities[x][y]
                    #print("změna")
            #print("=================\n==================")
        #print(min_value)
        if min_value!=1.0:
            print("hádám")
            self.probabilities[min_value_position[0]][min_value_position[1]]='?'
            return [min_value_position[0],min_value_position[1]]
        self.probabilities[5][5]='?'
        return [5,5]


    def predict_probability(self):
        changes=1
        data = self.get_state()
        while changes != 0:
            #print("changing...")
            changes = 0
            for x in range(self.__height):
                for y in range(self.__width):
                    probability = self.predict_neighbor_probability(x,y)
                    #print(probability)
                    if probability:
                        if probability==2:
                            probability=0
                        #print("prošlo")
                        neighbors_template = [[x-1, y-1], [x-1, y], [x-1, y+1], [x, y-1], [x, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]]
                        for z in neighbors_template:
                            if z[0]>=0 and z[1]>=0 and z[0]<=self.__height-1 and z[1]<=self.__width-1 and data[z[0]][z[1]]==' ':
                                last_probability = self.probabilities[z[0]][z[1]]
                                if  last_probability=='?' or (float(last_probability)!=0 and float(last_probability)!=1 and float(last_probability)>probability) or (float(probability)==1):
                                    if probability==1:
                                        self.__mines_found=self.__mines_found+1
                                    self.probabilities[z[0]][z[1]] = probability
                                    changes = changes+1
                                    #print("změněno")

    def predict_neighbor_probability(self, x, y):
        data = self.get_state()
        #Method returns list of lists with probabilities (in percents) for eachbox.
        current_box = [x,y]
        #print("current_box"+str(current_box))

        if data[current_box[0]][current_box[1]]!=" " and data[current_box[0]][current_box[1]]!=0 :
            #insert ' ' probability into uncovered box coordinates


            #get lists of all neighboring boxes
            neighbors = []
            neighbors_template = [[x-1, y-1], [x-1, y], [x-1, y+1], [x, y-1], [x, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]]
            for z in neighbors_template:
                if z[0]>=0 and z[1]>=0 and z[0]<=self.__height-1 and z[1]<=self.__width-1:
                    neighbors.append([z[0], z[1], data[z[0]][z[1]]])
            #print(neighbors)

            #get amount of neighboring bombs (if current box is uncovered)
            neighbor_mines = int(data[current_box[0]][current_box[1]])
            #print(neighbor_mines)

            #get list of coordinates of covered neighbors
            covered_neighbors = []

            for z in neighbors:
                if self.probabilities[z[0]][z[1]]==1:
                    neighbor_mines = neighbor_mines-1
                if z[2] == " " and self.probabilities[z[0]][z[1]]!=1:
                    covered_neighbors.append(z)

            #print(covered_neighbors)

            if len(covered_neighbors) != 0:
                #count probability of mine appearance
                #print(int(neighbor_mines))
                #print(int(len(covered_neighbors)))
                #print(int(neighbor_mines)/int(len(covered_neighbors)))
                #print("---------")
                probability = int(neighbor_mines)/int(len(covered_neighbors))
                #print(probability)
                #insert resulted probability into boxes with higher probability
                """for z in covered_neighbors:
                    if self.probabilities[z[0]][z[1]]!=1 or 0:
                        if self.probabilities[z[0]][z[1]]=="?":
                            self.probabilities[z[0]][z[1]] = probability
                        elif probability < int(self.probabilities[z[0]][z[1]]) or probability==1:
                            self.probabilities[z[0]][z[1]] = probability"""
                if probability==0:
                    probability=2
                return probability
            return False
        return False
