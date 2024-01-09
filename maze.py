from graphics import Cell
import random
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed =None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        if len(self._cells) == 0:
            return 
        entry : Cell = self._cells[0][0]
        dest : Cell = self._cells[self._num_cols-1][self._num_rows-1]
        
        entry.has_top_wall = False
        self._draw_cell(0,0)
        dest.has_bot_wall = False
        self._draw_cell(self._num_cols-1,self._num_rows-1)
    
    def _out_bounds(self,i,j):
        return i < 0 or j < 0 or i >= self._num_cols or j >= self._num_rows
    
    def _break_walls_r(self,i,j):
        if len(self._cells) == 0 : 
            return 
        
        cur_cell : Cell = self._cells[i][j]
        cur_cell._visited = True

        while True :
            to_visit = []
            direct = [(0,1),(1,0),(-1,0),(0,-1)] # down,right,left,up

            #check all directions and see if inbound and notvisited
            for d in range(len(direct)):
                new_i,new_j = i+direct[d][0],j+direct[d][1]
                if not self._out_bounds(new_i,new_j) and not self._cells[new_i][new_j]._visited:
                    to_visit.append((new_i,new_j))
            
            #no where to go
            if len(to_visit) == 0 :
                self._draw_cell(i,j)
                return 
            
            #random next dir 
            idx = random.randrange(len(to_visit))
            next_dir = to_visit[idx]

            #break walls between current and next to visit cell 
            #down
            if next_dir[1] == j+1 :
                self._cells[i][j].has_bot_wall = False
                self._cells[next_dir[0]][next_dir[1]].has_top_wall = False
            
            #right 
            if next_dir[0] == i+1 :
                self._cells[i][j].has_right_wall = False
                self._cells[next_dir[0]][next_dir[1]].has_left_wall = False

            #left 
            if next_dir[0] == i-1:
                self._cells[i][j].has_left_wall = False
                self._cells[next_dir[0]][next_dir[1]].has_right_wall = False

            #up 
            if next_dir[1] == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[next_dir[0]][next_dir[1]].has_bot_wall = False

            self._break_walls_r(next_dir[0],next_dir[1])

    def _reset_visited(self):
        for col in self._cells:
            for cell in col :
                cell._visited = False
    
    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self,i,j):
        self._animate()
        self._cells[i][j]._visited = True

        if i == self._num_cols-1 and j == self._num_rows-1 :
            return True
        
        direct = [(0, 1), (1, 0), (-1, 0), (0, -1)]  # directions: down, right, left, up

        
        for d in range(len(direct)):
            next_i, next_j = i + direct[d][0], j + direct[d][1]
            wall_conditions = [
                not self._cells[i][j].has_bot_wall,
                not self._cells[i][j].has_right_wall,
                not self._cells[i][j].has_left_wall,
                not self._cells[i][j].has_top_wall
            ]

            if not self._out_bounds(next_i, next_j) and not self._cells[next_i][next_j]._visited and wall_conditions[d]:
                self._cells[i][j].draw_move(self._cells[next_i][next_j])
                if self._solve_r(next_i, next_j):
                    return True 
                else :
                    self._cells[i][j].draw_move(self._cells[next_i][next_j],True)
        
        return False 
                    

