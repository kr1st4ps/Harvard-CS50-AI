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
        
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


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

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #   Mark cell as a move made
        self.moves_made.add(cell)

        #   Mark cell as safe
        self.mark_safe(cell)
        
        #   Loop through all neighboring cells and prepare new knowledge to be added
        sentence_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                #   Ignore if on the cell on which the move was made or if the cell is known to be safe
                if (i,j) == cell or (i,j) in self.safes:
                    continue

                #   If cell is a known mine, then reduce count and ignore cell
                if (i,j) in self.mines:
                    count -= 1
                    continue

                if i >= 0 and i < self.height and j >= 0 and j < self.width:
                    sentence_cells.add((i,j))
        
        #   Create the new knowledge sentence
        new_knowledge = Sentence(sentence_cells, count)

        #   If all cells in the sentece are safe or mines - mark them accordingly
        if len(new_knowledge.cells) == count:
            for cell in new_knowledge.cells:
                self.mark_mine(cell)
        elif count == 0:
            for cell in new_knowledge.cells:
                self.mark_safe(cell)

        #   Compare each current knowledge sentece to the new one
        for sentence in self.knowledge:
            if new_knowledge.cells in sentence.cells:
                sentence.cells -= new_knowledge.cells
                sentence.count -= new_knowledge.count

                if len(sentence.cells) == count:
                    for cell in sentence.cells:
                        self.mark_mine(cell)
                elif count == 0:
                    for cell in sentence.cells:
                        self.mark_safe(cell)

        #   Add the gained knowledge sentence to knowledge base
        self.knowledge.append(Sentence(sentence_cells, count))

        #   Prints known mines for the user to flag them
        print("Known mines:")
        print(self.mines)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        #   Checks if there are any safe moves and returns it
        for safe_move in self.safes:
            if safe_move not in self.moves_made:
                return safe_move
            
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #   Collects all possible moves that can be made
        possible_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    possible_moves.add((i,j))

        #   If there are no possible moves to make return None
        if len(possible_moves) == 0:
            return None

        #   Collects all moves that are known to possibly be mines
        possible_mines = set()
        for info in self.knowledge:
            for tuple in info.cells:
                possible_mines.add(tuple)

        #   Gets all moves of which we do not have any knowledge
        ideal_moves = list(possible_moves - possible_mines)

        #   If there are moves we know nothing about then make that move, 
        #   otherwise risk by taking one of the moves that are possibly bombs
        if len(ideal_moves) > 0:
            index = random.randrange(0, len(ideal_moves))
            return ideal_moves[index]
        else:
            possible_mines = list(possible_mines)
            index = random.randrange(0, len(possible_mines))
            return possible_mines[index]
