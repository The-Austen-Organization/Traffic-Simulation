"""
Code practices:
- Classes will start with capitals while functions will be lowercased.
- Use __ to signal private variables within classes.
- A positive x direction points towards the right direction, while a positive y direction indicates downward.
- Full caps to represent constant values.
"""

from global_variables import *

Roads_list = []
with open("data.json", "r") as f:
	points = json.load(f)

checkpoints = [Checkpoint(p["x"], p["y"]) for p in points]
road = Roads(checkpoints)

with open("order.json", "r") as f:
	order = json.load(f)

Car_coordinates = [
    [-100, 440],
    [600, 800],
    [300, 800],
    [225, -100]
]


for i in range(len(Car_coordinates)):
    Cars.append(Car(Car_coordinates[i][0],Car_coordinates[i][1], order[i],road))
global Selected_car
Selected_car = Cars[0]
def mouse_col(mouse,obj):
    global Selected_car
    if obj.rect.collidepoint(mouse):
        if pygame.mouse.get_pressed()[0]:
            Selected_car = obj
background = pygame.image.load(f"sprites/Earth_000.jpeg").convert_alpha()
background = pygame.transform.scale(background, (background.get_width() /3.2, background.get_height() /3.2))
running = True
while running:
    screen.fill((14,154,215))
    dt = clock.tick(60) / 1024  # delta time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                DEBUGGER = not DEBUGGER
            elif event.key == pygame.K_f:
                F_down = not F_down
            elif event.key == pygame.K_g:
                G_down = not G_down
            # Baldwin's code after this
            if event.key == pygame.K_EQUALS:
                pass
            elif event.key == pygame.K_MINUS:
                pass

    mouse = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()

    for car in Cars:
        car.update(dt)
        mouse_col(mouse,car)

   
    screen.blit(background, (width/2 - background.get_width()/2,height/2 - background.get_height()/2))
    for item in Cars:
        screen.blit(item.rotated_sprite, (item.pos.x - item.rotated_sprite.get_width()/2,item.pos.y - item.rotated_sprite.get_height()/2))
        item.raycast.render(screen)
        if item == Selected_car:
            pygame.draw.rect(screen, (255, 0, 0), (item.pos.x-item.sprite.get_width()/2, item.pos.y-item.sprite.get_height()/2, item.sprite.get_width(), item.sprite.get_height()), 2)

    if DEBUGGER:
        
        for i in range(len(Cars)):
            initial_pos = (Cars[i].X, Cars[i].Y)
            final_pos = ()
            for j in range(len(Cars[i].pathOG)):
                final_pos = ((Cars[i].pathOG[j].x,Cars[i].pathOG[j].y))
                Cars[i].pathOG[j].draw_dot()
                Cars[i].pathOG[j].draw_line(initial_pos,final_pos)
                initial_pos = ((Cars[i].pathOG[j].x,Cars[i].pathOG[j].y))

        with open("data.json", "r") as f:
            points = json.load(f)
            for i in range(len(points)):
                draw_text(screen, i, points[i]["x"], points[i]["y"],WHITE)
        

        if F_down:
            F_down = not F_down
            with open("data.json", "r") as f:
                points = json.load(f)
                
            points.append({"x":mouse[0],"y":mouse[1]})
            with open("data.json", "w") as f:
                f.write("[\n")
                for i, p in enumerate(points):
                    line = json.dumps(p)
                    if i < len(points) - 1:
                        line += ","
                    f.write("\t" + line + "\n")
                f.write("]")
            with open("order.json", "r") as g:
                orders = json.load(g)
            orders[Cars.index(Selected_car)].append(len(points)-1)
            with open("order.json", "w") as g:
                g.write("[\n")
                for i, row in enumerate(orders):
                    line = json.dumps(row)
                    if i < len(orders) - 1:
                        line += ","
                    g.write("\t" + line + "\n")
                g.write("]")
        if G_down:
            G_down = not G_down
            with open("data.json", "r") as f:
                points = json.load(f)
            if points:  # safety check (avoid error if empty)
                points.pop()
            with open("data.json", "w") as f:
                f.write("[\n")
                for i, p in enumerate(points):
                    line = json.dumps(p)
                    if i < len(points) - 1:
                        line += ","
                    f.write("\t" + line + "\n")
                f.write("]")
            with open("order.json", "r") as g:
                orders = json.load(g)
            if orders[Cars.index(Selected_car)]:
                orders[Cars.index(Selected_car)].pop()
            with open("order.json", "w") as g:
                g.write("[\n")
                for i, row in enumerate(orders):
                    line = json.dumps(row)
                    if i < len(orders) - 1:
                        line += ","
                    g.write("\t" + line + "\n")
                g.write("]")



    stats_left = [
        f"{round(clock.get_fps())}",
        f"ACCELERATION: {ACCELERATION}",
        f"FRICTION: {FRICTION}",
        f"MOUSE X: {mouse[0]}",
        f"MOUSE Y: {mouse[1]}"
    ]
    for i in range(len(stats_left)):
        draw_text(screen,stats_left[i],10,100+22*i, (255, 240, 237))

    pygame.display.flip()

pygame.quit()