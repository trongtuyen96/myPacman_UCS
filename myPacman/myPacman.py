from Tkinter import *
import sys
import time

#===========================================
PATH = 'O'
TRIED = 't'
WALL = '%'
DEAD_END = '-'
GOAL = 'G'
FOOD = '.'
PathListUCS =[]
Direction = [[1,0],[-1,0],[0,1],[0,-1]]
#============================================
#======== PRIORITY QUEUE ====================
class PriorityQueue:
    def __init__(self):
        self.queue= []
    
    def length(self):
        return len(self.queue)
    
    def pop(self):
        if self.length() != 0:
            value = self.queue[0]
            del self.queue[0]
        else:
            value = -1
        return value

    def is_empty(self):
        if self.length() == 0:
            return 1
        else:
            return 0

    def push(self, x, y, prio_level):
        i = 0
        len_queue = self.length()
        if len_queue == 0:
            self.queue.append([x, y, prio_level])
        else:
            while i < len_queue and prio_level == 0 :
                    i += 1
                    if i == len_queue:
                        break 
            len_queue = self.length()
            self.queue.append([0, 0, 0]) # initialize first tuple
            while i < len_queue:
                len_queue -= 1 
                self.queue[len_queue]=self.queue[len_queue-1]             
            self.queue[len_queue] = [x, y, prio_level]	        

    
#============================================
ReadMazeList =[]
countGoal = 0
inputlayout = sys.argv[2] + '.lay'
f = open(inputlayout,"r")
countline = 0
#xPacman = 0
#yPacman = 0
#xGoal = 0
#yGoal = 0
for line in f:
    countchar = 0
    rowList = []
    for char in line:
        rowList.append(char)
        if char == 'P':
            xPacman = countchar
            yPacman = countline
        if char == 'G':
            xGoal = countchar
            yGoal = countline
            countGoal += 1
        countchar+=1
    countline+=1
    ReadMazeList.append(rowList)
#==============================================
#========= SET UP FOR CANVAS ==================
Size = 0
TypeforSize = 0
pick = 0
exp1 = 1300 / countchar
exp2 = 700 / countline
if exp1 < exp2:
    pick = exp1
else:
    pick = exp2

if pick >= 40:
    Size = 40
else:
    if pick >= 30:
        Size = 30
    else:
        if pick >= 20:
            Size = 20
        else:
            Size = 10

#==============================================
#============== DRAW CANVAS ===================
master = Tk()
canvas_width = countchar * Size
canvas_height = countline * Size
w = Canvas(master, 
    width=canvas_width,
    height=canvas_height)
w.pack()

#======== ESC ===========
#========NOT WORK =======

if Size == 40:
    img = PhotoImage(file='Pacman40.gif')
if Size == 30:
    img = PhotoImage(file='Pacman30.gif')
if Size == 20:
    img = PhotoImage(file='Pacman20.gif')
if Size == 10:
    img = PhotoImage(file='Pacman10.gif')
Label(master, text=" PACMAN - UCS by Nguyen Trong Tuyen - 1453057", fg = "black", font = "Times").pack()
#==============================================
#================== CLASS =====================
class Maze:
    def __init__(self,mazeFileName):
        self.cost = 0
        self.mazelist = ReadMazeList
        self.RowsInMaze = countline
        self.ColumnsInMaze = countchar
        if countGoal == 1:
            self.goal = w.create_rectangle(xGoal*Size, yGoal*Size, (xGoal+1)*Size, (yGoal+1)*Size, fill = "red")
        w.update()
    
    #==== DRAW MAZE ====
    def DrawMaze(self):
        for y in range(self.RowsInMaze):
            for x in range(self.ColumnsInMaze):
                if self.mazelist[y][x] == WALL:
                    w.create_rectangle(x*Size,y*Size,(x+1)*Size, (y+1)*Size,fill="blue")
                if self.mazelist[y][x] == FOOD:
                    w.create_oval(x*Size + Size / 4,y*Size+ Size / 4,(x+1)*Size- Size / 4, (y+1)*Size- Size / 4,fill="yellow")
        w.update()

    def UpdateState(self,row,col,key=None):
        if key:
            self.mazelist[row][col] = key

    def __getitem__(self,idx):
        return self.mazelist[idx]
    #=============== UCS for stay_left and stay_right ===============
    def UCS(self, mRow,mCol,xPacman, yPacman,rMaze):
        self.cost = 0
        tempMaze = []
        i = 0
        while i < mRow:
            j = 0
            tempMaze.append([])
            while j < mCol:
                tempMaze[i].append(0)
                j += 1
            i += 1
        tempMaze[xPacman][yPacman] = 1
        tempPriority = PriorityQueue()
        tempPriority.push(xPacman,yPacman,1)
        #Queue = []
        #Queue.append([xPacman,yPacman])
        Queue = []
        
        while tempPriority.is_empty() == 0 :
            i = 0 
            Queue = tempPriority.pop()
            if Queue == -1:
                break;
            x = Queue[0]
            y = Queue[1]
            while i <=3 :# 4 direction
                if (x+Direction[i][0] >= 0) and (x+Direction[i][0] < mRow) and (y+Direction[i][1] >= 0) and(y+Direction[i][1] < mCol):
                    if (tempMaze[ x +Direction[i][0]][ y +Direction[i][1]] == 0) :
                        if rMaze[ x +Direction[i][0]][ y +Direction[i][1]] == GOAL: # Goal found
                            tempMaze [ x +Direction[i][0]] [ y +Direction[i][1]] = tempMaze[x][y] + 1
                            changeX = x +Direction[i][0]
                            changeY = y +Direction[i][1] 
                            i = 0
                            while i <= 3: # 4 direction
                                    if (changeX+Direction[i][0] >= 0) and (changeX+Direction[i][0] < mRow) and (changeY+Direction[i][1] >= 0) and(changeY+Direction[i][1] < mCol):
                                        if (tempMaze[changeX+Direction[i][0]][changeY+Direction[i][1]] == tempMaze[changeX][changeY]-1 ) :
                                            # update cost , function f(x) = x, + when turn left or right, remain the same when up or down
                                            oldX = changeX
                                            changeX = changeX + Direction[i][0]
                                            changeY = changeY + Direction[i][1]
                                            if oldX != changeX:
                                                self.cost += changeX
                                            PathListUCS.insert(0,[changeX,changeY])
                                            if tempMaze[changeX][changeY] == 1:
                                                return
                                            i = -1;
                                    i += 1
                        if rMaze[ x +Direction[i][0]][ y +Direction[i][1]] != WALL :
                            #Queue.append( [ x +Direction[i][0], y +Direction[i][1]] )
                            if (sys.argv[4] == 'ucs_stay_right' and i == 3) or  (sys.argv[4] == 'ucs_stay_left' and i == 2):
                                tempPriority.push(x+Direction[i][0],y+Direction[i][1],0)                         
                            else:
                                tempPriority.push(x+Direction[i][0],y+Direction[i][1],1)
                            tempMaze[ x +Direction[i][0]] [ y +Direction[i][1]] = tempMaze[x][y] + 1
                i = i + 1
            del Queue[0]
#===============================================
myMaze = Maze(inputlayout)
myMaze.DrawMaze()
#================================================
#================= FOR UCS ======================
if sys.argv[4] == 'ucs_stay_left' or sys.argv[4] == 'ucs_stay_right' :
    myMaze.UCS(countline,countchar,yPacman, xPacman,ReadMazeList)
    pacman = w.create_image(xPacman*Size, yPacman*Size, anchor=NW,image = img)
    file = open("1453057.txt", "w")
    num = len(PathListUCS)
    w.coords(pacman,xPacman*Size,yPacman*Size)
    if num==0:
        file.write("NO WAY AVAILABLE OR NO GOAL")
        file.close()
    else:
        file.write("%s\n" % (num))
        file.write("%s\n" % (myMaze.cost))
        if countGoal > 1:
            toadox = PathListUCS[num-1][1] 
            toadoy = PathListUCS[num-1][0]
            flag = 0
            if myMaze.mazelist[toadoy-1][toadox] == 'G':
                xGoal = toadox
                yGoal = toadoy-1
                flag = 1
            if (myMaze.mazelist[toadoy+1][toadox] == 'G') and flag ==0:
                xGoal = toadox
                yGoal = toadoy+1
                flag = 1
            if (myMaze.mazelist[toadoy][toadox-1] == 'G') and flag ==0:
                xGoal = toadox-1
                yGoal = toadoy
                flag = 1
            if (myMaze.mazelist[toadoy][toadox+1] == 'G') and flag ==0:
                xGoal = toadox+1
                yGoal = toadoy
                flag = 1
            w.create_rectangle(xGoal*Size, yGoal*Size, (xGoal+1)*Size, (yGoal+1)*Size, fill = "red")
        for i in (range(num)):
            toadox = PathListUCS[i][1] 
            toadoy = PathListUCS[i][0]
            w.coords(pacman,toadox*Size, toadoy*Size)
            w.update()
            time.sleep(0.2)
            w.create_rectangle(toadox*Size,toadoy*Size,(toadox+1)*Size,(toadoy+1)*Size, fill = "green")
            w.update()
            if i < num - 1:
                toadoxs = PathListUCS[i+1][1]
                toadoys = PathListUCS[i+1][0]
                if toadox == toadoxs and toadoy== toadoys - 1:
                    file.write("D ")
                if toadox ==  toadoxs and toadoy== toadoys + 1:
                    file.write("U ")
                if toadox == toadoxs - 1 and toadoy== toadoys:
                    file.write("R ")
                if toadox == toadoxs + 1 and toadoy== toadoys:
                    file.write("L ")
        toadox = PathListUCS[num-1][1] 
        toadoy = PathListUCS[num-1][0]
        if toadox == xGoal and toadoy== yGoal - 1:
            file.write("D ")
        if toadox == xGoal and toadoy== yGoal + 1:
            file.write("U ")
        if toadox == xGoal - 1 and toadoy== yGoal:
            file.write("R ")
        if toadox == xGoal + 1 and toadoy== yGoal:
            file.write("L ")
        file.close()
        w.coords(pacman,xGoal*Size,yGoal*Size)
        w.create_image(xGoal*Size,yGoal*Size,anchor=NW,image = img)
w.update()
mainloop()