import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        #print(f"inputted cell is {cell} and i and j values are {i} and {j}")
        #print(self.board[i][j])
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        """
        We know a cell is a mine if:
        1. The count is equal to len(cells) -> all the cells in the sentence are mines
        """
        if len(self.cells) == self.count and self.count!=0:
            return self.cells
        return set()
        
        #raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        """
        We know a cell is for sure safe if:
        1. the count of that sentence is 0, then all cells there are 0
        """
        if self.count == 0:
            return self.cells
        return set()
        #raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            #remove emelent from sentence and lower count by 1
            self.cells.remove(cell)
            self.count = self.count - 1
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        # List of sentences to be searched -> a search space
        self.searchspace = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count): #this is a move made, and you are mining knowledge after that move
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many of the neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made           /done
            2) mark the cell as safe                                /maybe done, bookmarked
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell) #should i be using the self keyword here???

        #step 3
        #tuple unpacking first
        (i,initial_col) = cell

        #get set surrounding cells of the inputted cell
        s = set()
        for i in range(i-1,i+2):
            if i>=0 and i<=7:
                j = initial_col
                for j in range(j-1,j+2):
                    if j>=0 and j<= 7:
                        s.add((i,j))
        #after the above loop, we will have a set containing intial cell and all its surrounding cells
        #we loop again and remove intial element as well as any other elements known to be mines or safes
        for element in s.copy():
            # remove the initial element or element is safe
            if element == cell or element in self.safes:
                #print(self.safes)
                #print(element)
                #print(s)
                s.remove(element)

            # if the element is a mine than remove it and reduce count by one
            if element in self.mines:
                s.remove(element)
                count = count -1
        #finally adding the sentence to the knowledge base
        self.knowledge.append(Sentence(s,count))


#There is copy pasting of code here, you might want to review this
        # Infer by comparing to itslef
        #see if all elements are mines
        if Sentence(s,count).known_mines():
            for cell in Sentence(s,count).known_mines():
                if cell not in self.mines:
                    self.mark_mine(cell)
        #check for safes
        elif Sentence(s,count).known_safes():
            for cell in Sentence(s,count).known_safes():
                if cell not in self.safes:
                    self.mark_safe(cell)



        # Infer by comparing to other sentences
        #steps 4 - 6
        # Append this sentence into the search space
        self.searchspace.append(Sentence(s,count))
        
        while True:
            # The exit condition for this loop is that the search space is empty
            if self.searchspace ==[]:
                #print("search space is empty, loop exited")
                break
            #if not, we will update the first sentence in the search space to the knowledge base to run the algo on it, and take it out of the searchspace
            else:
                self.knowledge.append(self.searchspace[0])
                self.searchspace.pop(0)
            
            # Run loop to compare last sentence in knowledge to all the others, see is subsets exist
            for sentence in self.knowledge:

                #if you get to the sentence you are examning right now,  do not do anything, this is condition to exit loop, no more sentences in search space, pick a new move
                if sentence== self.knowledge[-1]:
                    #print(f"{sentence} recenly added sentence, no action to be taken")
                    #print(f"currently the search space is {self.searchspace}")
                    break

                #checking for subsets, also check that you are not comparing an empty set because that always subsets
                if self.knowledge[-1].cells.issubset(sentence.cells) and self.knowledge[-1].cells != set():
                    #print(f"{self.knowledge[-1]} is subset of {sentence}")
                    newsentence = Sentence(set([i for i in sentence.cells if i not in self.knowledge[-1].cells]), sentence.count - self.knowledge[-1].count)
                    #check for mines, if they exist mark all cells as mines
                    if newsentence.known_mines():
                        for cell in newsentence.known_mines():
                            if cell not in self.mines:
                                self.mark_mine(cell)
                    #check for safes
                    elif newsentence.known_safes():
                        for cell in newsentence.known_safes():
                            if cell not in self.safes:
                                self.mark_safe(cell)
                    else: #this is a normal sentence, add it to search space
                        self.searchspace.append(newsentence)
                                

                if sentence.cells.issubset(self.knowledge[-1].cells) and sentence.cells !=set():
                    #print(f"{sentence} is subset of {self.knowledge[-1]}")
                    newsentence = Sentence(set([i for i in self.knowledge[-1].cells if i not in sentence.cells]), self.knowledge[-1].count - sentence.count)
                    #check for mines, if they exist mark all cells as mines
                    if newsentence.known_mines():
                        for cell in newsentence.known_mines():
                            if cell not in self.mines:
                                self.mark_mine(cell)
                    #check for safes
                    elif newsentence.known_safes():
                        for cell in newsentence.known_safes():
                            if cell not in self.safes:
                                self.mark_safe(cell)
                    else: #this is a normal sentence, add it to search space
                        self.searchspace.append(newsentence)
        

        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        #print("the safe space is")
        #print(self.safes)
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        #get number of spaces left that are not mines if it is 0 return none
        spacesleft = self.height*self.width - len(self.moves_made) - len(self.mines)
        if spacesleft == 0:
            return None

        #get spaces left that are you don't know to be mines, return one of them
        self.left = []
        for i in range(8):
            for j in range(8):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    return (i,j)
