import pygame
import game

running = True
mygame = game.Game()
mygame.start()

while running:
    if (mygame.points1 >= 13):
        print("Pobednik je igrac 1")
        running = False
    if (mygame.points1 >= 13):
        print("Pobednik je igrac 2")
        running = False
    
    mygame.reset_state()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        mygame.draw()
        mygame.detect_collision()

        if mygame.next_turn():
            #provera jel runda gotova
            if mygame.end_round():
                mygame.add_points()
                break

            #postavljanje sledece lopte na centar
            mygame.next_ball()
            
            #sledeci igrac
            while running:
                if not mygame.next_turn():
                    break
                
                mygame.draw()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEMOTION:
                        if event.buttons[0]:
                            is_ok, mouse = mygame.correct_pos()
                            if is_ok and mouse != None:
                                mygame.mouse = mouse
                    if event.type == pygame.MOUSEBUTTONUP:
                        is_ok, mouse = mygame.correct_pos()
                        mygame.mouse = None
                        if is_ok:
                            mygame.ball_move(mouse)
                

pygame.quit()