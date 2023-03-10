import numpy as np
import copy
import time

def getField():
    field = []
    with open('input.txt') as f:
        f = f.read().split("\n")
        for l in f:
            field.append(l)

    for i, row in enumerate(field):
        field[i] = list(row)
    field = tuple(field)
    print("==========================================")
    return field

def grid(row, col, field):
    if col < 0 or row < 0 or row > len(field) - 1 or col > len(field[0]) - 1:
        return "#"
    else:
        return field[row][col]

def printField(field):
    print("")
    for row in range(len(field)):
        for col in range(len(field[0])):
            symbol = field[row][col]
            if symbol == "*": print("\033[1;93m" + symbol + "\033[0m", end="")
            elif symbol == "#": print("\033[1;107m" + symbol + "\033[0m", end="")
            elif symbol in ["<", ">", "^", "v"]: print("\033[1;91m" + symbol + "\033[0m", end="")
            else: print(field[row][col], end='')
        print("")

######################################

def findBreakpoint(field, pos, directions, direction, breakPoints, createLights=False):
    #print(f"[findBreakpoint] for pos {pos}, direction {direction}")
    totLen = 0
    lightPositions = []
    for i in range(len(field[0])):
        lastPos = pos.copy()
        pos = pos + directions[direction]
        symbol = grid(pos[0], pos[1], field)
        #print(f"{pos} in {breakPoints}")
        is_in_list = np.any(np.all(pos == breakPoints, axis=1)) # May be slow?
        if is_in_list:
            #print("found pos in breakPoints, return 0")
            return lastPos, pos, field, 0, "I", []
        elif not symbol in ['*']:
            totLen += 1
            lightPositions.append(tuple(pos))

        if symbol in ["<", ">", "^", "v", "#", "B", "S"]:
            #print(f"  [findBreakpoint] Searching {direction}, ended at {pos}, totLen {totLen}, blocked by {symbol}")

            return lastPos, pos, field, totLen, symbol, lightPositions
        if createLights:
            field[pos[0]][pos[1]] = "*"


def shootLight(f, visualize=True, createStars=False):
    field = copy.deepcopy(f)  # Maybe no need?
    directions = {
        "^": np.array([-1, 0]),
        "v": np.array([1, 0]),
        "<": np.array([0, -1]),
        ">": np.array([0, 1])
    }
    total = 0
    direction = 'v'
    startPosition = np.array([1, 1])
    pos = startPosition

    breakPoints = []
    breakPoints.append(startPosition)
    for i in range(50): # Max Light Bounces
        lastPos, pos, field, totLen, symbol, lightPositions = findBreakpoint(field, pos, directions, direction,
                                                                             breakPoints, createStars)
        breakPoints.append(pos)
        total += totLen # totLen last line
        if symbol in ["#", "B", "S", "I"]:
            if visualize:
                printField(field)
            if createStars:
                print(f"[shootLight] Total Length is {total}")
            return lightPositions[:-1], total, direction
        elif symbol in directions.keys():
            direction = symbol


def testSignleDirection(tField, row, col, pos, futureSteps, direction):
    tField[row][col] = direction
    #print(f"{direction} at {pos}")
    tempLightPositions, totLen, lastDirection = shootLight(tField, False, False)
    if futureSteps > 0:
        futureSteps -= 1
        totLen, futurePos, futureDirection = testLightDirections(tempLightPositions, tField, lastDirection,
                                                futureSteps)  # Figures out the best of the lightPositions
    return (totLen, pos, direction)

def testLightDirections(lightPositions, field, direction, futureSteps = 1):
    ### shootLight(field, True, True)
    bestDirections = []
    #print(f"[loopAllLightpositions] starting with {lightPositions} in {direction}")
    for pos in lightPositions:
        #print(f"[loopAllLightpositions] im at pos {pos}, going general direction {direction}")
        row = pos[0]
        col = pos[1]
        tField = copy.deepcopy(field)
        if '^' != direction and 'v' != direction:
            bestDirections.append(testSignleDirection(tField, row, col, pos, futureSteps, "^"))
            bestDirections.append(testSignleDirection(tField, row, col, pos, futureSteps, 'v'))

        if '<' != direction and '>' != direction:

            bestDirections.append(testSignleDirection(tField, row, col, pos, futureSteps, "<"))
            bestDirections.append(testSignleDirection(tField, row, col, pos, futureSteps, '>'))


    if len(bestDirections) > 0:
        bestDirections = sorted(bestDirections)
        #print(f"[LoopallLightPositions] Returning {bestDirections[-1]}")
        return bestDirections[-1]
    return 0, (None), 'None'

