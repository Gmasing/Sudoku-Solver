import numpy as np

failSolve = np.array([[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1] ])

def getDomain(state,x,y):  #Given a cell, determines its available domain
    used = set(state[y]) - {0}                
    used_Column = set(getColumn(state, x))       
    used_Box    = set(getBox(state, x, y))
    z           = used.union(used_Column)
    final = z.union(used_Box)
    return set(range(1, 10)) - final

def getBox(state,x_cord,y_cord): #Returns all the numbers in a box (from top left to bottom right)
    Nums = []   
    box_x = (x_cord // 3) * 3
    box_y = (y_cord // 3) * 3

    for y in range(box_y,box_y+3):
        for x in range(box_x,box_x+3):
            num = state[y][x]
            if num != 0:
                Nums.append(num)
    return Nums

def getColumn(state,n): #Returns the n'th column
    Column = []
    for row in state:
        Column.append(row[n])
    return Column

def getAllEmptyValues(state): #will return [(x,y,numOfValues,[Values])] Used for MRV 
    priorityQueue = []
    for y in range (9):
        for x in range(9):
            domain = state[y][x]
            if len(domain) > 1:
                priorityQueue.append((x,y,len(domain),domain))

    return sorted(priorityQueue, key=lambda tup: tup[2]) #Sorts by numOfValues ascending order

def LCV (state,Values,x,y):
    resultList = []
    row = state[y]
    column = getColumn(state,x)

    for value in Values:
        mirked = 0
        for i in range(9):
            if len(row[i]) > 1:
                if value in state[y][i]: #getPossibleValues(state,i,y):
                    mirked += 1
                
            if len(column[i]) > 1:
                if value in state [i][x]:#getPossibleValues(state,x,i):
                    mirked += 1

        box_x = (x // 3) * 3 #top corner 
        box_y = (y // 3) * 3

        
        for y_box in range(box_y,box_y+3):
            for x_box in range(box_x,box_x+3):
                if  y_box != y and x_box != x:
                    if value in state[y_box][x_box]:
                        mirked += 1

        resultList.append((value,mirked))
    resultList = (sorted(resultList, key=lambda tup: tup[1]))
    return  [x[0] for x in  resultList] 

def isSolution(state):
    valid = True
    for y in range(9):
        for x in range(9):
            if len(state[y][x]) != 1:
                valid = False
                break
    return valid


def propagate(state,y,x,value): #current domain, y,x, value which we're propogating.
    newState = [[s.copy() for s in sublist] for sublist in state]

    if type(value) == set:
        newState[y][x] = value
    else:
        newState[y][x] = {value}

    for i in range(9): #Adapts the row 
        if i != x: #not the state we're modifying 
            length = len(newState[y][i])
            newState[y][i].discard(value)
            newLength = len(newState[y][i])
            if newLength == 0: #invalid sudoku
                return None
            if newLength == 1 and newLength < length: #if we lock in a value we lock it in (propagate further)
                for item in newState[y][i]:
                    newState = propagate(newState,y,i,item)
                    if newState == None:
                        return None

        if i != y: #adapts the column
            length = len(newState[i][x])          
            newState[i][x].discard(value) 
            newLength = len(newState[i][x])
            if newLength == 0:
                return None
            if newLength == 1 and newLength < length:
                for item in newState[i][x]:
                    newState = propagate(newState,i,x,item)
                    if newState == None:
                        return None

    

    box_x = (x // 3) * 3 
    box_y = (y // 3) * 3


    for y_box in range(box_y,box_y+3): #Adapts the box
        for x_box in range(box_x,box_x+3):
            if y_box != y and x_box != x:
                length = len(newState[y_box][x_box])    
                newState[y_box][x_box].discard(value)
                newLength = len(newState[y_box][x_box])
                if newLength == 0:
                    return None
                if newLength == 1 and newLength < length:
                    for item in newState[y_box][x_box]:
                        newState = propagate(newState,y_box,x_box,item)
                        if newState == None:
                            return None

    return newState

def valid(state): 
    valid = True
    for row in state:
        for domain in row:
            if len(domain) == 0:
                valid = False
                break 
    return valid 

def solve(sudoku):

    temp = [[s.copy() for s in sublist] for sublist in sudoku]

    queue = getAllEmptyValues(sudoku)

    for (x,y,numValues,Values) in queue:
        #Then i sort the values in Values by the ones that restrict the least
        if numValues >= 3:
            ValuesSorted = LCV(temp,Values,x,y)
        else:
            ValuesSorted = Values

        for value in ValuesSorted:
            newDomains = propagate(temp,y,x,value)
            if newDomains is None:
                continue
            if not valid(newDomains):
                continue
            if  isSolution(newDomains):
                return newDomains
            else:
                result = solve(newDomains)
                if result is not None:
                    return result
                

            temp[y][x] = sudoku[y][x]
        return None
    return None

def convertBack(sudoku):
    result = []
    for y in range(9):
        result.append([])
        for x in range(9):
            result[y].append(sudoku[y][x].pop())
    return result

def Solvable(state):
    # Check rows
    for y in range(9):
        nums = [n for n in state[y] if n != 0]
        if len(nums) != len(set(nums)):
            return False

    # Check columns
    for x in range(9):
        col = [state[y][x] for y in range(9) if state[y][x] != 0]
        if len(col) != len(set(col)):
            return False

    # Check 3x3 boxes
    for box_y in range(0, 9, 3):
        for box_x in range(0, 9, 3):
            nums = []
            for y in range(box_y, box_y + 3):
                for x in range(box_x, box_x + 3):
                    if state[y][x] != 0:
                        nums.append(state[y][x])
            if len(nums) != len(set(nums)):
                return False

    return True


def sudoku_solver(sudoku):

    converted = convertTable(sudoku)

    queue = []
    for y in range(9):
        for x in range(9):
            cell = converted[y][x]
            if len(cell) == 1:
                for value in cell:
                    queue.append((x,y,value))

    for (x,y,value) in queue:
        converted = propagate(converted,y,x,value)
        if converted == None:
            return failSolve
        

    if isSolution(converted):
        return np.array(convertBack(converted))
    else:
        result = solve(converted)

    if result is not None:
        return np.array(convertBack(result))
    else:
        return failSolve


def convertTable(sudoku):
    sudokuDomains = [[],[],[],[],[],[],[],[],[]]
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] != 0:
                sudokuDomains[y].append(set([sudoku[y][x]]))
            else:
                newDomain = set(getDomain(sudoku,x,y))
                sudokuDomains[y].append(newDomain)
    return sudokuDomains
