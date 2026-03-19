"""
Code practices:
- Classes will start with capitals while functions will be lowercased.
- Use __ to signal private variables within classes.
- A positive x direction points towards the right direction, while a positive y direction indicates downward.
- Full caps to represent constant values.
"""

from global_variables import *

road = Roads([
    Checkpoint(900, 440), 
    Checkpoint(1020, 300), 
    Checkpoint(1020, 120), 
    Checkpoint(900, 40), 
    Checkpoint(725, 30), 
    Checkpoint(600, 180), 
    Checkpoint(600, 400), 
    Checkpoint(600, 800), 
    Checkpoint(-100, 440),
    Checkpoint(300, -100),
    Checkpoint(225, 800)
])

Cars.append(Car(-100, 440, road.create_path([0, 1, 2, 3, 4, 5, 6, 7])))
Cars.append(Car(600, 800, road.create_path([6, 5, 4, 3, 2, 1, 0, 8])))
Cars.append(Car(300, 800, road.create_path([9])))
Cars.append(Car(225, -100, road.create_path([10])))

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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass
            # Baldwin's code after this
            elif event.key == pygame.K_PLUS:
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
        for i in range(len(road.road)):
            draw_text(screen, i, road[i].x, road[i].y,WHITE)

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