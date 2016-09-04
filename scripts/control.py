import pygame
import lib.libardrone as libardrone

drone = None

def main():
    global drone

    pygame.init()
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    clock = pygame.time.Clock()
    running = True

    SPEED = {pygame.K_1 : 0.1,
             pygame.K_2 : 0.2,
             pygame.K_3 : 0.3,
             pygame.K_4 : 0.4,
             pygame.K_5 : 0.5,
             pygame.K_6 : 0.6,
             pygame.K_7 : 0.7,
             pygame.K_8 : 0.8,
             pygame.K_9 : 0.9,
             pygame.K_0 : 1.0
    }

    CONTROLS = {pygame.K_RETURN : drone.takeoff,
                pygame.K_SPACE : drone.land,
                pygame.K_BACKSPACE : drone.reset,
                pygame.K_w : drone.move_forward,
                pygame.K_s : drone.move_backward,
                pygame.K_a : drone.move_left,
                pygame.K_d : drone.move_right,
                pygame.K_UP : drone.move_up,
                pygame.K_DOWN : drone.move_down,
                pygame.K_LEFT : drone.turn_left,
                pygame.K_RIGHT : drone.turn_right
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.KEYUP:
                drone.hover()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drone.reset()
                    running = False
                # takeoff / lan
                else:
                    CONTROLS.get(event.key, test)()

                # speed
                drone.speed = SPEED.get(event.key, drone.speed)


        try:
            surface = pygame.image.fromstring(drone.image, (W, H), 'RGB')
            # battery status
            hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
            bat = drone.navdata.get(0, dict()).get('battery', 0)
            f = pygame.font.Font(None, 20)
            hud = f.render('Battery: %i%%' % bat, True, hud_color)
            screen.blit(surface, (0, 0))
            screen.blit(hud, (10, 10))
        except:
            pass

        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    print "Shutting down...",
    drone.halt()
    print "Ok."

def test():
    pass

if __name__ == '__main__':
    main()
