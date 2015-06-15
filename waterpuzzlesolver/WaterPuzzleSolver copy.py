"""
Water Pouring Puzzle Solver (2 Glasses)
Amy X. | Last Updated: Jun, 2015

Instructions:
Enter your desired quantity, the capacity of the target glass, your target number of steps,
and the litre capacity of each glass when prompted.

"""
import copy

# Global counter for counting steps taken
counter = 0

class Glass(object):
    """
    Represents properties of each glass.
    """            
    def __init__(self, capacity):
            self.capacity = capacity
            self.level = 0
            self.available = capacity
        
    def fill(self): 
        self.level = self.capacity
        self.available = 0
        return "Fill {0}L glass".format(self.capacity)
            
    def empty(self):
        self.level = 0
        self.available = self.capacity
        return "Empty {0}L glass".format(self.capacity)
    
    def larger(self, glass):
        if self.capacity > glass.capacity:
            return True
        elif self.capacity < glass.capacity:
            return False

class Game(object):
    """
    Stores state of each game.
    """                       
    def __init__(self):
        self.__quantity = None
        self.__target = None
        self.__goal = None
        self.__glasses = []
        self.__moves = 0
        self.__solutionList = []
        self.__differences = []
    
    def setQuantity(self, quantity):
        self.__quantity = quantity
        
    def setTarget(self, target):
        self.__target = target
    
    def getQuantity(self):
        return self.__quantity
    
    def getTarget(self):
        return self.__target
    
    def setGlasses(self, glasslist):
        self.__glasses = glasslist
    
    def replaceGlass(self, old, new):
        for glass in self.__glasses:
            if glass.capacity == old.capacity:
                self.__glasses.remove(glass)
                self.__glasses.append(new)
    
    def getGlass(self, desiredcap):
        for glass in self.__glasses:
            if glass.capacity == desiredcap:
                return glass
            else:
                pass
    
    def getGlasses(self):
        return self.__glasses
    
    def setGoal(self, goal):
        self.__goal = goal
    
    def getGoal(self):
        return self.__goal
    
    def addSolutionStep(self, step):
        self.__solutionList.append(step)
        global counter
        counter += 1
        
    def addSolutions(self, solutionList):
        self.__solutionList += solutionList
        
    def getSolution(self):
        for sol in self.__solutionList:
            print sol
            
    def getSolutionList(self):
        return self.__solutionList
    
    def clearSolutions(self):
        self.__solutionList = []
                
    def pour(self, glass_a, glass_b):
        """
        Pours glass_a contents into glass_b
        """        
        # Get the difference between glass_b's available space and glass_a's level
        remain_b = glass_b.available - glass_a.level
        
        if remain_b < 0: # Glass a's level is greater than glass_b's available space
            glass_a.level = glass_a.level - glass_b.available
            glass_a.available = glass_a.capacity - glass_a.level
            glass_b.level = glass_b.capacity
            glass_b.available = 0
            
        elif remain_b == 0: # Glass a's level is equal to glass_b's available space
            glass_a.level = 0
            glass_a.available = glass_a.capacity
            glass_b.level = glass_b.capacity
            glass_b.available = 0
            
        elif remain_b > 0: # Glass a's level is smaller than glass_b's available space
            glass_b.level = glass_b.level + glass_a.level 
            glass_b.available = glass_b.capacity - glass_b.level
            glass_a.level = 0
            glass_a.available = glass_a.capacity
        
        self.addSolutionStep("Pour {0}L glass in {1}L glass".
                             format(glass_a.capacity, glass_b.capacity))
        global counter
        counter += 1
        
    def fillToQuantity(self, glass, targetglass):
        """
        Fills the target glass to the winning quantity level 
        when only one other glass needs to be used.
        """          
        while targetglass.level != self.__quantity:
            self.addSolutionStep(glass.fill())
            self.pour(glass, targetglass)    
            
    def evenSolExistsWith(self, glass):
        """
        Checks to see if the desired quantity is divisible by the capacity of the glass.
        """                 
        if self.__quantity % glass.capacity == 0 and self.__target.available > glass.capacity:
            print("There is an even solution!")
            return True
        
    def solExistsAtLevelWith(self, glass):
        """
        If a combination of pouring yields desired result at current level,
        return True. Return False otherwise.
        """                 
        self.__differences = []
        
        if glass.available > self.__target.available:
            larger = glass
            smaller = self.__target            
        elif glass.available <= self.__target.available:
            larger = self.__target
            smaller = glass                     
        
        if larger.level == 0:
            # this first so glass doesn't get emptied if 0 and 1 are the same
            self.__differences.append(larger.capacity - smaller.available) 
            self.__differences.append(larger.capacity - smaller.capacity) 
        elif larger.level >= 0:
            self.__differences.append(larger.level - smaller.available)
            self.__differences.append(larger.level - smaller.capacity)
        
        if self.__quantity in self.__differences: 
            return True
        else:
            return False
        
    def solveWith(self, glass):
        """
        Solve the puzzle at current level.
        """                 
        # Compare if glass or target glass has the larger available capacity
        if glass.available > self.__target.available:
            larger = glass
            smaller = self.__target
        elif glass.available <= self.__target.available:
            larger = self.__target
            smaller = glass
            
        i = self.__differences.index(self.__quantity)
        
        # If the glass with the larger available capacity doesn't have any water
        if larger.level == 0: 
            if i == 0: # larger.capacity - smaller.available
                self.addSolutionStep(larger.fill())
                self.pour(larger, smaller)
            elif i == 1: # larger.capacity - smaller.capacity
                larger.fill()
                self.addSolutionStep(smaller.empty())
                self.pour(larger, smaller)
                
        # If the glass with the larger available capacity does have some water
        elif larger.level >= 0:
            if i == 0: # larger.level - smaller.available
                self.pour(larger, smaller)         
            elif i == 1: # larger.level - smaller.capacity
                self.addSolutionStep(smaller.empty())
                self.pour(larger, smaller)                   
        
        # If the glass with the larger available capacity isn't the target glass,
        # empty target glass and pour correct amount into target glass
        if larger != self.__target:
            self.addSolutionStep(self.__target.empty())
            self.pour(larger, self.__target)    
    
    def end(self):
        """
        Game end. Display replay prompt.
        """                   
        self.getSolution()

        print("\n** Done! **\n")
        
        replay = raw_input("Replay? (y/n)\n\n")
        if replay == "y":
            main()
        elif replay == "n":
            print("Good bye!")
        
def playGame(quantity, target, glasses, game):
    """
    Game algorithm.
    """                       
    quantity = quantity
    glasses = glasses
    targetglass = target
    game = game
    global counter

    """
    ================
    Algorithm Starts
    ================
    """
    # If target glass has the correct value, return solutions
    if targetglass.level == quantity:
        return game.getSolutionList()        
    
    else:
        for glass in glasses:
            if glass == targetglass:
                continue
            
            # If a glass can be filled and poured into target glass to achieve desired level,
            # keep doing it until desired level is achieved
            if game.evenSolExistsWith(glass):
                game.fillToQuantity(glass, targetglass)
                return game.getSolutionList()
            
            # Checks to see if a combination of glass actions at the current level yields result         
            elif game.solExistsAtLevelWith(glass):
                game.solveWith(glass)
                return game.getSolutionList()
            
            # If there are no results at the current level, and the game is within goal steps,
            # pour water from glass_a to glass_b and glass_b to glass_a, and recurse on both possibilities
            elif counter <= (game.getGoal()):
                mockglass = copy.deepcopy(glass)
                mockgame = copy.deepcopy(game)
                mocktarget = copy.deepcopy(targetglass)
                
                if mocktarget.level == 0:
                    game.addSolutionStep(mocktarget.fill())
    
                if mockglass.level == mockglass.capacity:
                    game.addSolutionStep(mockglass.empty())
                    
                game.pour(mocktarget, mockglass)                
                
   
                mockgame.setTarget(mocktarget)
                mockgame.replaceGlass(mockgame.getGlass(glass.capacity), mockglass)
                mockgame.replaceGlass(mockgame.getGlass(targetglass.capacity), mocktarget)
                
                try:
                    gcounter = counter
                    sol = playGame(mockgame.getQuantity(), mockgame.getTarget(), mockgame.getGlasses(), mockgame)
                    # If recursion finds the correct results, add to existing solution list and return
                    if sol != None:
                        game.addSolutions(sol)
                        return game.getSolutionList()
                    
                    # If recursion doesn't find the correct results, recurse on other possibility                 
                    elif sol == None:
                        game.clearSolutions()
                        counter = gcounter

                        mockglass = copy.deepcopy(glass)
                        mockgame = copy.deepcopy(game)    
                        mocktarget = copy.deepcopy(targetglass)
    
                        if mockglass.level == 0:
                            game.addSolutionStep(mockglass.fill())
                        
                        if mocktarget.level == mocktarget.capacity:
                            game.addSolutionStep(mocktarget.empty())                    
    
                        game.pour(mockglass, mocktarget)
            
                        mockgame.setTarget(mocktarget)
                        mockgame.replaceGlass(mockgame.getGlass(glass.capacity), mockglass)
                        mockgame.replaceGlass(mockgame.getGlass(targetglass.capacity), mocktarget)  
                        
                        gcounter = counter
                        sol2 = playGame(mockgame.getQuantity(), mockgame.getTarget(), mockgame.getGlasses(), mockgame)
                        if sol2 != None:
                            game.addSolutions(sol2)
                            return game.getSolutionList()
                        elif sol2 == None:
                            counter = gcounter
                            return None
                            
                except Exception as e:
                    print("1: {0}".format(e))
                    pass            
                
            # If steps exceed target steps of game, return no solution
            elif counter > game.getGoal():
                game.clearSolutions()
                return None
                                         
def main():
    global counter
    counter = 0
    
    print("\nWelcome to the game solver!")
    game = Game()
    
    quantity = int(raw_input("Please enter the quantity: \n"))
    game.setQuantity(quantity)
    
    targetval = int(raw_input("Please enter the capacity of the target glass: \n"))
    target = Glass(targetval)
    game.setTarget(target)
    
    goalsteps = int(raw_input("Please enter the target for the level: \n"))
    game.setGoal(goalsteps)
    
    uinput = True
    glasses = []
    glasslist = []
    
    print("Please enter the litre capacity of each glass followed by enter:")
    
    
    while uinput:
        try:
            glass = int(raw_input())
        
        except ValueError as e:
            if target.capacity not in glasses:
                print("Did you forget to enter your target glass?\nPlease include your target glass.")
                pass
            else:
                break
            
        glasses.append(glass)
    
    glasses = set(glasses)
    
    # Convert given capacities to glass objects           
    for j in glasses:
        if j != target.capacity:
            glasslist.append(Glass(j))
        elif j == target.capacity:
            glasslist.append(target)
        
    game.setGlasses(glasslist)
        
    # Find solution to puzzle
    print("========\nSolution\n========\n")
    playGame(game.getQuantity(), game.getTarget(), game.getGlasses(), game)
    
    # End game
    game.end()

if __name__ == "__main__":
    main()