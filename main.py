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
            if event.key == pygame.K_PLUS:
                pass
            elif event.key == pygame.K_MINUS:
                pass

    mouse = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()

    for car in Cars:
        car.update(dt)

    background = pygame.image.load(f"sprites/road.jpg").convert_alpha()
    background = pygame.transform.scale(background, (background.get_width() * 1.1, background.get_height() * 1.1))
    screen.blit(background, (width/2 - background.get_width()/2,height/2 - background.get_height()/2))
    for item in Cars:
        screen.blit(item.rotated_sprite, (item.pos.x - item.rotated_sprite.get_width()/2,item.pos.y - item.rotated_sprite.get_height()/2))
        item.raycast.render(screen)
        # pygame.draw.rect(screen, (255, 0, 0), (item.x-item.sprite.get_width()/2, item.y-item.sprite.get_height()/2, item.sprite.get_width(), item.sprite.get_height()), 2)

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
        
        print(Cars[0].path_list)
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



    stats_left = [
        f"ACCELERATION: {ACCELERATION}",
        f"FRICTION: {FRICTION}",
        f"MOUSE X: {mouse[0]}",
        f"MOUSE Y: {mouse[1]}"
    ]
    for i in range(len(stats_left)):
        draw_text(screen,stats_left[i],10,100+22*i, (255, 240, 237))

    pygame.display.flip()

pygame.quit()