"""
Code practices:
- Classes will start with capitals while functions will be lowercased.
- Use __ to signal private variables within classes.
- A positive x direction points towards the right direction, while a positive y direction indicates downward.
- Full caps to represent constant values.
"""

from global_variables import *


running = True
while running:
    screen.fill((14,154,215))
    dt = clock.tick(60) / 1024  # delta time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()
    for car in Cars:
        car.update(dt)

    background = pygame.image.load(f"sprites/road.jpg").convert_alpha()
    background = pygame.transform.scale(background, (background.get_width() * 1.1, background.get_height() * 1.1))
    screen.blit(background, (width/2 - background.get_width()/2,height/2 - background.get_height()/2))
    for item in Cars:
        screen.blit(item.rotated_sprite, (item.pos.x - item.rotated_sprite.get_width()/2,item.pos.y - item.rotated_sprite.get_height()/2))
        # pygame.draw.rect(screen, (255, 0, 0), (item.x-item.sprite.get_width()/2, item.y-item.sprite.get_height()/2, item.sprite.get_width(), item.sprite.get_height()), 2)

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
