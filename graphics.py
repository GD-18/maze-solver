from tkinter import Tk,BOTH,Canvas

class Window :
    def __init__(self,width,height):
        self.__width = width
        self.__height = height
        self.__root = Tk()
        self.__root.title('Maze Solver')
        self.__canvas = Canvas(self.__root,bg = "white",height=self.__height,width=self.__width)
        self.__canvas.pack(fill=BOTH,expand=1)
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW",self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self,line,fill_color="black"):
        line.draw(self.__canvas,fill_color)
    
    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running :
            self.redraw()
        print("window closing...")

    def close(self):
        self.__window_running = False

class Point :
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

class Line :
    def __init__(self,point1:Point,point2:Point):
        self.point1 = point1
        self.point2 = point2
    def draw(self,canvas:Canvas,fill_color="black"):
        canvas.create_line(self.point1.x,self.point1.y,self.point2.x,self.point2.y,fill=fill_color,width=2)
        canvas.pack(fill=BOTH,expand=1)

class Cell :
    def __init__(self,win = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bot_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None 
        self. _win = win
        self._visited = False
        
    def draw(self,x1,y1,x2,y2):
        if self._win is None :
            return 
        
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        
        #left
        line = Line(Point(x1,y1),Point(x1,y2))
        self._win.draw_line(line,fill_color="black" if self.has_left_wall else "white")
        #right
        line = Line(Point(x2,y1),Point(x2,y2))
        self._win.draw_line(line,fill_color="black" if self.has_right_wall else "white")
        #bot
        line = Line(Point(x1,y2),Point(x2,y2))
        self._win.draw_line(line,fill_color="black" if self.has_bot_wall else "white")
        #top
        line = Line(Point(x1,y1),Point(x2,y1))
        self._win.draw_line(line,fill_color="black" if self.has_top_wall else "white")

    def draw_move(self,to_cell,undo = False ):
        if self._win is None : return 

        # find the center of current cell
        cx = (self._x1+self._x2)/2
        cy = (self._y1+self._y2)/2

        # find the center of the destination cell
        dx = (to_cell._x1 +to_cell._x2)/2
        dy = (to_cell._y1 + to_cell._y2)/2
        
        color = "gray" if undo else "red"
        
        #left 
        if self._x1 > to_cell._x1:
            line = Line(Point(cx,cy),Point(self._x1,cy))
            self._win.draw_line(line,fill_color=color)

            line =  Line(Point(dx,dy) , Point(to_cell._x2,dy))
            self._win.draw_line(line,fill_color=color)
        
        #right
        if self._x1 < to_cell._x1:
            line = Line(Point(self._x2,cy),Point(cx ,cy))
            self._win.draw_line(line,fill_color=color)

            line = Line(Point(dx,dy),Point(to_cell._x1,dy))
            self._win.draw_line(line,fill_color=color)

        #top 
        if self._y1 > to_cell._y1:
            line = Line(Point(cx,cy),Point(cx,self._y1))
            self._win.draw_line(line,fill_color=color)

            line = Line(Point(dx,dy),Point(dx,to_cell._y2))
            self._win.draw_line(line,fill_color=color)

        #bot 
        if self._y1 < to_cell._y1:
            line = Line(Point(cx,cy),Point(cx,self._y2))
            self._win.draw_line(line,fill_color=color)

            line = Line(Point(dx,dy),Point(dx,to_cell._y1))
            self._win.draw_line(line,fill_color=color)

            