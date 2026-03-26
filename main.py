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

Car_coordinates = []
for i in range(len(order)):
    Car_coordinates.append([points[order[i][0]]["x"]-1,points[order[i][0]]["y"]-1])


for i in range(len(Car_coordinates)):
    x, y = Car_coordinates[i]
    PENDING_CARS.append((x, y, order[i]))

global Selected_car
Selected_car = None
prev_zoom = camara.zoom
prev_offset = camara.offset.copy()
debug_surface = None
def mouse_col(mouse,obj):
    global Selected_car
    if obj.rect.collidepoint(mouse):
        if pygame.mouse.get_pressed()[0]:
            Selected_car = obj
backgroundImage = pygame.image.load(f"sprites/Earth_000.jpeg").convert_alpha()

running = True
while running:
    screen.fill((14,154,215))
    dt = clock.tick(144) / 1024  # delta time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                global_variables.DEBUGGER = not global_variables.DEBUGGER
            elif event.key == pygame.K_f:
                F_down = not F_down
            elif event.key == pygame.K_g:
                G_down = not G_down
            elif event.key == pygame.K_m:
                M_down = not M_down
            elif event.key == pygame.K_SPACE:
                Pause = not Pause


    mouse = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_EQUALS]:
        camara.zoom *= 1.01
    if keys[pygame.K_MINUS]:
        camara.zoom /= 1.01
    if keys[pygame.K_UP]:
        camara.offset.y += 5
    if keys[pygame.K_DOWN]:
        camara.offset.y -= 5
    if keys[pygame.K_LEFT]:
        camara.offset.x += 5
    if keys[pygame.K_RIGHT]:
        camara.offset.x -= 5
    if not Pause:

    still_pending = []
    for (x, y, path) in PENDING_CARS:
        if all(math.hypot(car.X - x, car.Y - y) >= MIN_SPAWN_DISTANCE for car in Cars):
            Cars.append(Car(x, y, path, road))
            if Selected_car is None:
                Selected_car = Cars[0]
        else:
            still_pending.append((x, y, path))
    PENDING_CARS = still_pending
    for car in Cars:
        car.update(dt)
        mouse_col(mouse,car)
    
    background = pygame.transform.scale(backgroundImage, (camara.zoom * width, camara.zoom * height))
    screen.blit(background, (offset.x - background.get_width() / 2, offset.y - background.get_height() / 2))
    for item in Cars:
        screen.blit(pygame.transform.scale(item.rotated_sprite, (item.rotated_sprite.get_width() * camara.zoom / 16, item.rotated_sprite.get_height() * camara.zoom / 16)), 
            (scale(item.pos) - pygame.Vector2(item.rotated_sprite.get_width(), item.rotated_sprite.get_height()) * camara.zoom / 32)
        )
        item.raycast.render(screen)
        if item == Selected_car and DEBUGGER:
            pygame.draw.circle(screen, BLUE, scale(pygame.Vector2(item.pos.x, item.pos.y)), DOT_SIZE * camara.zoom)

    if global_variables.DEBUGGER:
        
        camera_moved = (camara.zoom != prev_zoom or camara.offset != prev_offset)

        if debug_surface is None or camera_moved:
            debug_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            for i in range(len(Cars)):
                initial_pos = pygame.Vector2(Cars[i].X, Cars[i].Y)
                for j in range(len(Cars[i].pathOG)):
                    final_pos = pygame.Vector2(Cars[i].pathOG[j].x, Cars[i].pathOG[j].y)
                    pygame.draw.line(debug_surface, WHITE, scale(initial_pos), scale(final_pos), 1)
                    initial_pos = final_pos

            for i in range(len(points)):
                pos = scale(pygame.Vector2(points[i]["x"], points[i]["y"]))
                pygame.draw.circle(debug_surface, RED, pos, DOT_SIZE * camara.zoom)
                draw_text(debug_surface, i, pos.x, pos.y, GREEN, int(30 * camara.zoom))

            prev_zoom = camara.zoom
            prev_offset = camara.offset.copy()

        screen.blit(debug_surface, (0, 0))
        

        if F_down:
            F_down = not F_down
            with open("data.json", "r") as f:
                points = json.load(f)
                
            points.append({"x":mouse[0],"y":mouse[1],"n":len(points)})
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

    if M_down:
        stats_top = [
                f"Estadísticas automovilístas:",
                f"Aproximádamente 2,096 muertes anuales",
                f"Aproximádamente 217 accidentes anuales",
                f"Promedio de 16,717 personas lesionadas anuálmente",
                f"El 70% de los accidentes corresponde a motoristas",
                f"El 99.6% de los motoristas NO tienen licencia",
                f"El 13% de las víctimas son peatones",
                f"Total de accidentes anuales aproximado: 79,205",
                f"34.6 muertes por cada 100,000 habitantes",
                f"La República Dominicana es el país más",
                f"peligroso para conducir en las Américas"
        ]
        debug_rect = pygame.Rect(INFOX-10,INFOY-10,465,len(stats_top)*22+20)
            
        if debug_rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                INFOX = mouse[0] - (230/2)
                INFOY = mouse[1] - (len(stats_top)*22+10)/2

        pygame.draw.rect(screen, (BLUE),debug_rect)
        for i in range(len(stats_top)):
            draw_text(screen,stats_top[i],INFOX,INFOY+22*i, WHITE, 30)
        
        stats_left = [
                f"Estadisticas:",
                f"FPS:{round(clock.get_fps())}",
                f"Number of Cars {len(order)}",
                f"Aceleración: {ACCELERATION}",
                f"Fricción: {FRICTION}",
                f"MOUSE X: {mouse[0]}",
                f"MOUSE Y: {mouse[1]}",
                f"Zoom: {camara.zoom:.2f}"
        ]
        debug_rect = pygame.Rect(DEBUGX-10,DEBUGY-10,235,len(stats_left)*22+15)
            
        if debug_rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                DEBUGX = mouse[0] - 230/2
                DEBUGY = mouse[1] - (len(stats_left)*22+10)/2

        pygame.draw.rect(screen, (GREY),debug_rect)
        for i in range(len(stats_left)):
            draw_text(screen,stats_left[i],DEBUGX,DEBUGY+22*i, WHITE, 30)
    if Pause:
        M_down = False
        rect_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        rect_surf.fill((180, 180, 180, 128))
        screen.blit(rect_surf, (0, 0))
        draw_text(screen,"<Presiona Espacio para Reanudar>",width/2-260,20,WHITE,40)
    pygame.display.flip()

pygame.quit()
"""
citas
https://listindiario.com/la-republica/20251128/muertes-accidentes-transito-siguen-aumento-pais-registra-promedio-2-000-decesos-anuales_884160.html
https://www.diariolibre.com/actualidad/ciudad/2025/03/11/accidentes-de-transito-por-dia-en-rd-en-2025/3030049#:~:text=Este%20a%C3%B1o%20se%20registra%20un,por%20d%C3%ADa%20en%20el%20pa%C3%ADs&text=En%20los%2069%20d%C3%ADas%20que,coordinaci%C3%B3n%20con%20las%20autoridades%20competentes.
https://datos.gob.do/dataset/estadistica-de-fallecimientos-por-accidentes-de-transito?utm_source=chatgpt.com
https://www.one.gob.do/datos-y-estadisticas/temas/estadisticas-sociales/seguridad-publica-y-justicia/accidentales-y-violentas

"""