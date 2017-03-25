import pygame as pg
from math import factorial, log, sin



def evaluate(expression, x):
    expression = expression.replace("x", "(" + str(x) + ")")
    return eval(expression)



##function = raw_input("input function :\ny = ")
##function = function.replace("^", "**")   
##
##
##x_range = raw_input("\n\ninput x-range (minx, maxx):\n")
##print x_range
##x_range = [int(x) for x in x_range.replace("(", "").replace(")", "").replace(" ", "").split(",")]
##
##y_range = raw_input("\n\ninput y-range (miny, maxy):\n")
##y_range = [int(y) for y in y_range.replace("(", "").replace(")", "").replace(" ", "").split(",")]


function = "sin(x)"
x_range = [-10,10]
y_range = [-10,10]





print x_range, y_range



#x| -5 -4 -3 -2 -1 0 1 2 3  4  5|
#y| 25 16  9  4  1 0 1 4 9 16 25|
table = [
    range(x_range[0], x_range[1] + 1),
    [None for y in range(x_range[1] - x_range[0] + 1)]
]

for i in range(len(table[0])):
    table[1][i] = evaluate(function, table[0][i])

print table[0], "\n", table[1]




black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)




screen = pg.display.set_mode((800,600))

screen.fill(white)
pg.draw.rect(screen, black, pg.Rect(0,0,800,600), 2)


x_step = 800.0/(x_range[1]-x_range[0])
y_step = 600.0/(y_range[1]-y_range[0])

origin = (abs(x_range[0])*x_step, 600-abs(y_range[0])*y_step)
print origin


#draw x-axis
pg.draw.line(screen, black, (0,origin[1]), (800,origin[1]), 1)

for x in table[0]:
    pixel_x = origin[0]+x_step*x
    pg.draw.line(screen, black, (pixel_x,origin[1]-10), (pixel_x,origin[1]+10), 1)

#draw y-axis
pg.draw.line(screen, black, (origin[0],0), (origin[0],600), 1)

for y in range(y_range[0], y_range[1]+1):
    pixel_y = origin[1]-y_step*y
    pg.draw.line(screen, black, (origin[0]-10,pixel_y), (origin[0]+10,pixel_y), 1)



#draw points
points = []
for i in range(len(table[0])):
    pos = (int(table[0][i]*x_step+origin[0]), int(origin[1]-table[1][i]*y_step))
    points.append(pos)
    pg.draw.circle(screen, blue, (pos), 4)

#connect points
pg.draw.lines(screen, blue, False, points, 1)


pg.display.update()




clock = pg.time.Clock()


done = False
while not done:
    clock.tick(60)

    #user input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            done = True







