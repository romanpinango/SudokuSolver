class Sudoku:

    def __init__(self, size):
        self.size = size
        self.grid = [0] * size
        for i in range(size):
            self.grid[i] = [0] * size
        self.candidates = [0] * size
        for i in range(size):
            self.candidates[i] = [0] * size
        for i in range(size):
            for j in range(size):
                self.candidates[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.hasChanged = False
        self.boxOdds = [0] * self.size
        for i in range(size):
            self.boxOdds[i] = [0] * size
        for i in range(size):
            for j in range(size):
                self.boxOdds[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.rowOdds = [0] * self.size
        for i in range(size):
            self.rowOdds[i] = [0] * size
        for i in range(size):
            for j in range(size):
                self.rowOdds[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.columnOdds = [0] * self.size
        for i in range(size):
            self.columnOdds[i] = [0] * size
        for i in range(size):
            for j in range(size):
                self.columnOdds[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def print(self):
        print("Sudoku Grid")
        for i in range(self.size):
            if i % 3 == 0:
                print(" ")
            for j in range(self.size):
                if j % 3 == 0:
                    print(" " + str(self.grid[i][j]), end='')
                elif j == self.size - 1:
                    print(self.grid[i][j])
                else:
                    print(self.grid[i][j], end='')

    def printCandidates(self):
        print("Candidates")
        for i in range(self.size):
            if i % 3 == 0:
                print(" ")
            for j in range(self.size):
                if j % 3 == 0:
                    print(" " + str(len(self.candidates[i][j])), end='')
                elif j == self.size - 1:
                    print(len(self.candidates[i][j]))
                else:
                    print(len(self.candidates[i][j]), end='')

    def printBoxOdds(self):
        for i in range(self.size):
            print("Box " + str(i+1) + " - ", end='')
            for j in range(self.size):
                print(" " + str(j+1) + ":" + str(len(self.boxOdds[i][j])), end='')
            print("")

    def printFullBoxOdds(self):
        for i in range(self.size):
            print("Box " + str(i+1) + " - ", end='')
            for j in range(self.size):
                print(" " + str(j+1) + ":" + str(self.boxOdds[i][j]), end='')
            print("")

    def printRowOdds(self):
        for i in range(self.size):
            print("Row " + str(i+1) + " - ", end='')
            for j in range(self.size):
                # if len(self.rowOdds[i][j]) == 2:
                print(" " + str(j+1) + ":" + str(self.rowOdds[i][j]), end='')
            print("")

    def printColumnOdds(self):
        for i in range(self.size):
            print("Column " + str(i+1) + " - ", end='')
            for j in range(self.size):
                # if len(self.columnOdds[i][j]) == 2:
                print(" " + str(j+1) + ":" + str(self.columnOdds[i][j]), end='')
            print("")

    def load(self, values):
        j = 0
        k = 0
        for i in range(len(values)):
            if values[i] == ",":
                j = j + 1
                k = 0
            else:
                self.grid[j][k] = int(values[i])
                k = k + 1

    def solve(self):
        self.hasChanged = True
        while self.hasChanged:
            self.hasChanged = False

            # Check candidates by row, column and box
            for i in range(self.size):
                for j in range(self.size):
                    if self.grid[i][j] != 0:
                        self.candidates[i][j].clear()
                        # self.candidates[i][j].append(self.grid[i][j])
                    else:
                        self.checkRow(i, self.candidates[i][j])
                        self.checkColumn(j, self.candidates[i][j])
                        self.checkBox(i, j, self.candidates[i][j])
                    if self.grid[i][j] == 0 and len(self.candidates[i][j]) == 1:
                        self.grid[i][j] = self.candidates[i][j][0]

            # Check the odds of every number in each box
            for i in range(self.size):
                for j in range(self.size):
                    self.updateBoxOdds(i, j)
                    if len(self.boxOdds[i][j]) == 1:
                        self.setBoxUnique(i, j + 1, self.boxOdds[i][j])

            # Check the odds of every number in each row
            for i in range(self.size):
                for j in range(self.size):
                    self.rowOdds[i][j] = self.updateRowOdds(i, j + 1)
                    if len(self.rowOdds[i][j]) == 1:
                        self.setRowUnique(i, j + 1, self.rowOdds[i][j])

            # Check the odds of every number in each column
            for i in range(self.size):
                for j in range(self.size):
                    self.columnOdds[i][j] = self.updateColumnOdds(i, j + 1)
                    if len(self.columnOdds[i][j]) == 1:
                        self.setColumnUnique(i, j + 1, self.rowOdds[i][j])

            # Check nDependencies in Boxes
            potentials = []
            for i in range(self.size):
                potentials.clear()
                for j in range(self.size):
                    if len(self.boxOdds[i][j]) == 2:
                        potentials.append(j)
                if len(potentials) >= 2:
                    for j in potentials:
                        for k in potentials:
                            if j < k:
                                if self.boxOdds[i][j] == self.boxOdds[i][k]:
                                    # print("Remove BoxId " + str(i) + " numbers " + str(j) + " " + str(k))
                                    # print("Foco " + str(j + 1) + " y " + str(k + 1))
                                    for p in range(self.size):
                                        for q in self.boxOdds[i][j]:
                                            if (p + 1) != (j + 1) and (p + 1) != (k + 1) and self.boxOdds[i][p].count(q) > 0:
                                                # print("Ahora Borro " + str(q) + " de " + str(p + 1))
                                                self.boxOdds[i][p].remove(q)
                                                if len(self.boxOdds[i][p]) == 1:
                                                    # print("Pongo unico " + str(i) + " de " + str(p + 1))
                                                    self.setBoxUnique(i, p + 1, self.boxOdds[i][p])

            # Check nDependencies in Rows
            potentials = []
            for i in range(self.size):
                potentials.clear()
                for j in range(self.size):
                    if len(self.rowOdds[i][j]) == 2:
                        potentials.append(j)
                if len(potentials) >= 2:
                    for j in potentials:
                        for k in potentials:
                            if j < k:
                                if self.rowOdds[i][j] == self.rowOdds[i][k]:
                                    # print("Remove BoxId " + str(i) + " numbers " + str(j) + " " + str(k))
                                    # print("Foco " + str(j + 1) + " y " + str(k + 1))
                                    for p in range(self.size):
                                        for q in self.rowOdds[i][j]:
                                            if (p + 1) != (j + 1) and (p + 1) != (k + 1) and self.rowOdds[i][p].count(q) > 0:
                                                # print("Ahora Borro " + str(q) + " de " + str(p + 1))
                                                self.rowOdds[i][p].remove(q)
                                                if len(self.rowOdds[i][p]) == 1:
                                                    print("Pongo unico " + str(i) + " de " + str(p + 1))
                                                    self.setRowUnique(i, p + 1, self.rowOdds[i][p])

            # Check nDependencies in Columns
            potentials = []
            for i in range(self.size):
                potentials.clear()
                for j in range(self.size):
                    if len(self.columnOdds[i][j]) == 2:
                        potentials.append(j)
                if len(potentials) >= 2:
                    for j in potentials:
                        for k in potentials:
                            if j < k:
                                if self.columnOdds[i][j] == self.columnOdds[i][k]:
                                    # print("Remove BoxId " + str(i) + " numbers " + str(j) + " " + str(k))
                                    # print("Foco " + str(j + 1) + " y " + str(k + 1))
                                    for p in range(self.size):
                                        for q in self.columnOdds[i][j]:
                                            if (p + 1) != (j + 1) and (p + 1) != (k + 1) and self.columnOdds[i][p].count(q) > 0:
                                                # print("Ahora Borro " + str(q) + " de " + str(p + 1))
                                                self.columnOdds[i][p].remove(q)
                                                if len(self.columnOdds[i][p]) == 1:
                                                    print("Pongo unico " + str(i) + " de " + str(p + 1))
                                                    self.setColumnUnique(i, p + 1, self.columnOdds[i][p])

            # CheckAssumptions
            for i in range(self.size):
                for j in range(self.size):
                    orientation = self.isAssumption(i, j)
                    if orientation > 0:
                        print("Is assumption! BoxId " + str(i + 1) + " Number " + str(j + 1) + " Orientation " + str(orientation))
                        if self.processAssumption(i, j, orientation):
                            if len(self.boxOdds[i][j]) == 1:
                                self.setBoxUnique(i, j + 1, self.boxOdds[i][j])

            self.print()
            # self.printCandidates()
            # self.printFullBoxOdds()
            # self.printRowOdds()
            self.printColumnOdds()
            input("Press any key to resumen...")

    def processAssumption(self, boxId, number, orientation):
        internalChange = False
        for i in range(self.size):
            if orientation == 1 and int(i / 3) == int(boxId / 3) and i != boxId:
                print("Actualizo el BoxId " + str(i + 1) + " row " + str(self.getRowAssumption(self.boxOdds[boxId][number])))
                internalChange = self.updateBoxWithAssumptions(i, number, orientation, self.getRowAssumption(self.boxOdds[boxId][number]))
            elif orientation == 2 and int(i % 3) == int(boxId % 3) and i != boxId:
                print("Actualizo el BoxId " + str(i + 1) + " column " + str(self.getColumnAssumption(self.boxOdds[boxId][number])))
                internalChange = self.updateBoxWithAssumptions(i, number, orientation, self.getColumnAssumption(self.boxOdds[boxId][number]))
        return internalChange

    def updateBoxWithAssumptions(self, boxId, number, orientation, position):
        internalChange = False
        for i in self.boxOdds[boxId][number]:
            if orientation == 1:
                if (int(i / 3) == position):
                    self.boxOdds[boxId][number].remove(i)
                    internalChange = True
            elif orientation == 2:
                if (int(i % 3) == position):
                    self.boxOdds[boxId][number].remove(i)
                    internalChange = True
        return internalChange

    def getRowAssumption(self, odds):
        return int(odds[0] / 3)

    def getColumnAssumption(self, odds):
        return int(odds[0] % 3)

    def isAssumption(self, boxId, number):
        orientation = 0 # 1=horizontal, 2=vertical
        arrayMods = []
        arrayDivs = []
        if len(self.boxOdds[boxId][number]) > 1 and len(self.boxOdds[boxId][number]) <= 3:
            for i in self.boxOdds[boxId][number]:
                arrayDivs.append(int((i - 1) / 3))
                arrayMods.append(int((i - 1) % 3))
            isHorizontal = True
            isVertical = True
            x = arrayDivs[0]
            for i in arrayDivs:
                if x != i:
                    isHorizontal = False
                    break
            if not isHorizontal:
                y = arrayMods[0]
                for i in arrayMods:
                    if y != i:
                        isVertical = False
                        break
            else:
                isVertical = False
            if isHorizontal:
                orientation = 1
                # print("IsHorizontal BoxId " + str(boxId + 1) + " Number " + str(number + 1) + " odds " + str(self.boxOdds[boxId][number]))
            if isVertical:
                orientation = 2
                # print("IsVertical   BoxId " + str(boxId + 1) + " Number " + str(number + 1) + " odds " + str(self.boxOdds[boxId][number]))
        return orientation

    def setColumnUnique(self, columnId, number, value):
        n = 1
        for i in range(self.size):
            if self.candidates[i][columnId].count(number) > 0 and value.count(n) > 0:
                self.candidates[i][columnId].clear()
                # self.candidates[rowId][j].append(number)
                self.grid[i][columnId] = number
                self.hasChanged = True
                break
            n = n + 1

    def updateColumnOdds(self, columnId, number):
        odds = []
        for i in range(self.size):
            if self.candidates[i][columnId].count(number) > 0:
                odds.append(i + 1)
            if self.grid[i][columnId] == number:
                odds.clear()
                break
        return odds

    def setRowUnique(self, rowId, number, value):
        n = 1
        for j in range(self.size):
            if self.candidates[rowId][j].count(number) > 0 and value.count(n) > 0:
                self.candidates[rowId][j].clear()
                # self.candidates[rowId][j].append(number)
                self.grid[rowId][j] = number
                self.hasChanged = True
                break
            n = n + 1

    def updateRowOdds(self, rowId, number):
        odds = []
        for j in range(self.size):
            if self.candidates[rowId][j].count(number) > 0:
                odds.append(j + 1)
            if self.grid[rowId][j] == number:
                odds.clear()
                break
        return odds

    '''
    def setBoxUnique(self, boxId, number):
        boxX = int(boxId / 3) * 3
        boxY = int(boxId % 3) * 3
        for i in range(boxX, boxX + 3):
            for j in range(boxY, boxY + 3):
                if self.candidates[i][j].count(number) > 0:
                    self.candidates[i][j].clear()
                    self.grid[i][j] = number
                    self.hasChanged = True
                    break
    '''

    def setBoxUnique(self, boxId, number, value):
        print("Recibo " + str(boxId) + " - " + str(number) + " - " + str(value))
        n = 1
        boxX = int(boxId / 3) * 3
        boxY = int(boxId % 3) * 3
        for i in range(boxX, boxX + 3):
            for j in range(boxY, boxY + 3):
                if self.candidates[i][j].count(number) > 0 and value.count(n) > 0:
                    self.candidates[i][j].clear()
                    self.grid[i][j] = number
                    self.hasChanged = True
                    break
                n = n + 1

    def updateBoxOdds(self, boxId, number):
        boxX = int(boxId / 3) * 3
        boxY = int(boxId % 3) * 3
        position = 1
        for i in range(boxX, boxX + 3):
            for j in range(boxY, boxY + 3):
                if self.candidates[i][j].count(number + 1) == 0:
                    if self.boxOdds[boxId][number].count(position) > 0:
                        self.boxOdds[boxId][number].remove(position)
                if self.grid[i][j] == number + 1:
                    self.boxOdds[boxId][number].clear()
                    break
                position = position + 1

    def checkRow(self, row, candidates):
        for j in range(self.size):
            if self.grid[row][j] != 0:
                if candidates.count(self.grid[row][j]) > 0:
                    self.hasChanged = True
                    candidates.remove(self.grid[row][j])

    def checkColumn(self, column, candidates):
        for i in range(self.size):
            if self.grid[i][column] != 0:
                if candidates.count(self.grid[i][column]) > 0:
                    self.hasChanged = True
                    candidates.remove(self.grid[i][column])

    def checkBox(self, row, column, candidates):
        boxX = int(row / 3) * 3
        boxY = int(column / 3) * 3
        for i in range(boxX, boxX + 3):
            for j in range(boxY, boxY + 3):
                if self.grid[i][j] != 0:
                    if candidates.count(self.grid[i][j]) > 0:
                        self.hasChanged = True
                        candidates.remove(self.grid[i][j])

s1 = Sudoku(9)
# s1.load("530070000,600195000,098000060,800060003,400803001,700020006,060000280,000419005,000080079")
# s1.load("009300007,602000080,040005020,800200000,004000500,000009001,060900040,070000602,400003100")
# s1.load("605000040,003200000,040601009,000000064,160804072,480000000,700908020,000002400,020000607")
s1.load("001000300,008903000,500020060,000038014,060000070,310590000,090040006,000706100,006000700")
s1.solve()
print(s1.candidates[0][0])