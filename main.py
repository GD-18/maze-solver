from graphics import *

def main():
    win = Window(800,600)
    cell_1 = Cell(win)
    cell_1.draw(20,20,100,100)
    win.wait_for_close()

main()