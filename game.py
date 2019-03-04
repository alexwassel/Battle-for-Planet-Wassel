#Alex Wassel's Space Battle!

import gamebox
import pygame
import random

camera = gamebox.Camera(800, 600)

#BACKGROUND
background = gamebox.from_image(50, 100, 'space.jpg')
background.scale_by(0.8)


#BORDERS UP AND DOWN
borders = [
    gamebox.from_color(0, 600, 'black', 5000, 5),
    gamebox.from_color(0, 0, 'black', 5000, 5),
 ]

#METEORS
walls = []
for i in range(random.randrange(20,40)):
    meteor = gamebox.from_image(random.randrange(300,500), random.randrange(0,600), "spaceMeteors_002.png")
    meteor.scale_by(0.4)
    walls.append(meteor)


#COLLECTABLES
collectables = []
for i in range(10):
    coin = gamebox.from_image(
            random.randrange(100, 700),
            random.randrange(0, 600),
            'coin.png'
        )
    coin.scale_by(0.7)
    collectables.append(coin)



#SOUND
shooting_sound = gamebox.load_sound("sound-2.wav")
death_sound = gamebox.load_sound("Explosion+6.wav")


#SPACESHIPS
person1 = gamebox.from_image(20, 400, 'spaceShips_001 2.png')
person1.scale_by(0.5)
person2 = gamebox.from_image(780, 400, 'spaceShips_001.png')
person2.scale_by(0.5)

#BULLETS
shot1 = gamebox.from_image(200, 2200, "spaceMissiles_009.png")
shot1.scale_by(0.8)
shot1.life = 0

shot2 = gamebox.from_image(200, 2200, "spaceMissiles_009 2.png")
shot2.scale_by(0.8)
shot2.life = 0


#FRONT PAGE SCREEN
screen = True
ticks = 0

def splash(keys):
    global screen, ticks
    #camera.clear('cyan')
    back = gamebox.from_image(50, 100, 'stars.png')
    back.scale_by(1.5)
    camera.draw(back)

    text = gamebox.from_text(400, 100, "Battle for Planet Wassel", "Arial", 50, 'white')
    names = gamebox.from_text(400, 100, "By Alex Wassel", "Arial", 20, 'white')
    names.top = text.bottom
    camera.draw(text)
    camera.draw(names)
    directions = gamebox.from_text(400,300, "Player 1: use W to move your spaceship up and S to move it down. Use the Space Bar to shoot.", "Arial", 17, 'white')
    directions1 = gamebox.from_text(400,300, "Player 2: use the Up and Down arrow keys to move your spaceship. Use the comma key to shoot.", "Arial", 17, 'white')
    directions2 = gamebox.from_text(400,300, "Press SPACE to start", "Arial", 20, 'yellow')
    camera.draw(directions)
    directions1.top = directions.bottom
    directions2.top = directions1.bottom
    camera.draw(directions1)
    camera.draw(directions2)

    if pygame.K_SPACE in keys:
        screen = False
    camera.display()


timing = 0
coins1 = 0
coins2 = 0

def tick(keys):
    global coins1
    global coins2
    global ticks
    ticks += 1

    global timing
    if ticks%30==0 and not screen:
        timing += 1

    if screen:
        splash(keys)
        return

    camera.clear('white')
    camera.draw(background)

    #TIMER
    time = gamebox.from_text(100, 100, str(timing), 'Arial', 30, 'white')
    time.top = camera.top
    time.right = camera.right
    camera.draw(time)



    if pygame.K_UP in keys:
        person2.y += -15
    if pygame.K_DOWN in keys:
        person2.y += 15

    if pygame.K_w in keys:
        person1.y += -15
    if pygame.K_s in keys:
        person1.y += 15

    for wall in borders:
        if person1.touches(wall):
            person1.speedy = 0
            person1.move_to_stop_overlapping(wall)
    for wall in borders:
        if person2.touches(wall):
            person2.speedy = 0
            person2.move_to_stop_overlapping(wall)

    for coin1 in collectables:
        camera.draw(coin1)
        if coin1.touches(shot1):
            collectables.remove(coin1)
            coins1 += 1
    score1 = gamebox.from_text(60,580,"P1 Coins: "+str(coins1), "Arial", 20, 'white')
    camera.draw(score1)

    for coin2 in collectables:
        camera.draw(coin2)
        if coin2.touches(shot2):
            collectables.remove(coin2)
            coins2 += 1
    score2 = gamebox.from_text(740, 580, "P2 Coins: " + str(coins2), "Arial", 20, 'white')
    camera.draw(score2)



#DRAWING THE METEORS
    for wall in walls:
        camera.draw(wall)


#BULLET FUNCTIONS
    if pygame.K_SPACE in keys and shot1.life > 30:
        shooting_sound.play()
        shot1.center = person1.center
        shot1.speedx = 50
        shot1.life = 0
    shot1.move_speed()
    shot1.life += 1
    if pygame.K_COMMA in keys and shot2.life > 30:
        shooting_sound.play()
        shot2.center = person2.center
        shot2.speedx = -50
        shot2.life = 0
    shot2.move_speed()
    shot2.life += 1


#REMOVING METEOR WALLS
    for w in walls:
        if w.touches(shot1):
            walls.remove(w)
            shot1.x = 1000
            shot1.speedx = 0

    for w in walls:
        if w.touches(shot2):
            walls.remove(w)
            shot2.x = 1000
            shot2.speedx = 0


#DEATH
    if shot1.touches(person2):
        death_sound.play()
        gamebox.pause()
        camera.draw(gamebox.from_text(400, 300, "It took "+str(timing)+" seconds for Player 1 to Win with "+str(coins1)+" coins!", "Arial", 25, "Red", True))

    if shot2.touches(person1):
        death_sound.play()
        gamebox.pause()
        camera.draw(gamebox.from_text(400, 300, "It took "+str(timing)+" seconds for Player 2 to Win with "+str(coins2)+" coins!", "Arial", 25, "Red", True))


    camera.draw(shot1)
    camera.draw(shot2)
    camera.draw(person1)
    camera.draw(person2)
    camera.display()

ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)
