import numpy as np
import copy
import time
from logic import *

def main():
    field = getField()
    tic = time.perf_counter()

    lightPositions, totLen, direction = shootLight(field)
    print(lightPositions)

    futureSteps = 3
    iterations = 40
    for i in range(iterations):
        toc = time.perf_counter()

        print(f" ===== STEP {i} ===== {toc - tic:0.4f}")
        if i == 1: print(f"Prob gonna take {(toc - tic)*50/60} Minutes")
        elif i == 5: print(f"Prob gonna take {(toc - tic)*10/60} Minutes")

        remainingSteps = (iterations-i)-1
        if futureSteps>remainingSteps:
            print(f"Futuresteps is {futureSteps}, lowering it to {iterations-i-1}")
            futureSteps = iterations-i-1

        n, pos, direction = testLightDirections(lightPositions, field, direction, futureSteps) # Figures out the best of the lightPositions

        field[pos[0]][pos[1]] = direction
        lightPositions, totLen, direction = shootLight(field, False, False)
        print(f"lightPositions are {lightPositions}")


    print("==========================================Final Print==========================================")

    shootLight(field, True, True)



def testing():
    field = getField()

    printField(field, turns)


if __name__ == "__main__":
    main()





# 299 bei 30
