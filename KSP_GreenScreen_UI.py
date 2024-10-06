from threading import Thread
import configparser
import pygame

from pygame_ui import Gauge
from KerbalSimpit import *

from ctypes import windll
windll.user32.SetProcessDPIAware()


craft_vel = None
craft_alt = None
craft_throttle = None
craft_lf = None


def message_handler(message_type, message):
    global craft_vel, craft_alt, craft_throttle, craft_lf
    message = parse_message(message_type, message)
    if message is None:
        return
    match message_type:
        case OutboundPackets.VELOCITY_MESSAGE:
            craft_vel = message
        case OutboundPackets.LF_MESSAGE:
            craft_lf = message
        case OutboundPackets.ALTITUDE_MESSAGE:
            craft_alt = message
        case OutboundPackets.THROTTLE_CMD_MESSAGE:
            craft_throttle = message


def ksp_thread_worker():
    while True:
        ksp.update(message_handler, print_debug=True)


def draw_vel(message:VelocityMessage):
    if message is None:
        return
    gauge_speed.update_surf(message.surface)
    gauge_speed.draw(window)

def draw_alt(message:AltitudeMessage):
    if message is None:
        return
    gauge_altitude.update_surf(message.surface)
    gauge_altitude.draw(window)

def draw_lf(message:ResourceMessage):
    if message is None or message.total == 0:
        return
    gauge_fuel.update_surf(message.available/message.total*100)
    gauge_fuel.draw(window)

def draw_throttle(message:ThrottleMessage):
    if message is None:
        return
    gauge_throttle.update_surf(message.throttle/327.68)
    gauge_throttle.draw(window)


config = configparser.ConfigParser()
config.read('Settings.cfg')

port = config.get('Communication', 'port')
baudrate = config.getint('Communication', 'baud_rate')
resolution_x = config.getint("Window", 'width')
resolution_y = config.getint("Window", 'height')
target_fps = config.getint("Window", 'target_fps')


ksp = KerbalSimpit(port, baudrate=baudrate)

if ksp.hand_shake():
    print("Handshake success")

ksp.register_channel(OutboundPackets.VELOCITY_MESSAGE)
ksp.register_channel(OutboundPackets.ALTITUDE_MESSAGE)
ksp.register_channel(OutboundPackets.THROTTLE_CMD_MESSAGE)
ksp.register_channel(OutboundPackets.LF_MESSAGE)

ksp_thread = Thread(target=ksp_thread_worker, daemon=True)
ksp_thread.start()

pygame.init()
pygame.font.init()

resolution = (resolution_x, resolution_y)
window = pygame.display.set_mode(resolution, pygame.SRCALPHA)
clock = pygame.time.Clock()

pygame.display.set_caption("KSP GreenScreen UI")
pygame.display.set_icon(pygame.image.load("icon.png"))


gauge_speed = Gauge((20, 20), (0, 1000), "Speed", "m/s")
gauge_altitude = Gauge((240, 20), (0, 1000), "Alt", "m")
gauge_throttle = Gauge((resolution_x-440, 20), (0, 100), "Throttle", "%")
gauge_fuel = Gauge((resolution_x-220, 20), (0, 100), "Fuel", "%")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    window.fill(0x00ff00)

    draw_vel(craft_vel)
    draw_alt(craft_alt)
    draw_throttle(craft_throttle)
    draw_lf(craft_lf)

    pygame.display.flip()
    clock.tick(target_fps)
    pygame.event.pump()

ksp.close()
pygame.quit()
print("exit")
    