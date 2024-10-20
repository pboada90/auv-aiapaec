import pygame

pygame.init()
pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

def init_joystick():
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        return joystick
    else:
        raise Exception("No joystick detected...")
    
def get_joystick_events():
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.append("QUIT")

        if event.type == pygame.JOYBUTTONDOWN:
            button_id = event.button
            events.append(("BUTTONDOWN", button_id))

        if event.type == pygame.JOYBUTTONUP:
            button_id = event.button
            events.append(("BUTTONUP", button_id))

        if event.type == pygame.JOYAXISMOTION:
            if abs(pygame.joystick.Joystick(0).get_axis(2)) > 0.1:
                events.append(("axis_2", pygame.joystick.Joystick(0).get_axis(2)))
            if abs(pygame.joystick.Joystick(0).get_axis(3)) > 0.1:
                events.append(("axis_3", pygame.joystick.Joystick(0).get_axis(3)))

    return events