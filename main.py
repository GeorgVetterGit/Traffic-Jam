import math
import pygame
import asyncio

HEIGHT = 500
WIDTH = 500
SIDEBAR = 150
FPS = 60
MAX_VEL = 1

ACCEL = 0.01
BREAK_RANGE = 15
NUM_CARS = 15

COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "BACKGROUND": (50, 49, 48),
    "HIGHLIGHT": (242, 203, 5),
    "FRAME": (242, 135, 5),
    "SIDEBAR": (40, 39, 38)
}
TRACK_DIAMETER = 200
CENTER_TRACK = (WIDTH // 2, HEIGHT // 2)

CAR_IMG = pygame.image.load("assets/car_sprite.png")
CAR_IMG = pygame.transform.scale(CAR_IMG, (30, 20))

LEFT_ARROW = pygame.image.load("assets/left_arrow.png")
LEFT_ARROW = pygame.transform.scale(LEFT_ARROW, (10, 10))

RIGHT_ARROW = pygame.image.load("assets/right_arrow.png")
RIGHT_ARROW = pygame.transform.scale(RIGHT_ARROW, (10, 10))


pygame.init()
screen = pygame.display.set_mode((WIDTH + SIDEBAR, HEIGHT))
pygame.display.set_caption("Traffic Jam Simulator")
clock = pygame.time.Clock()

cars = pygame.sprite.Group()

class Car(pygame.sprite.Sprite):

    def __init__(self, center, groups):
        super().__init__(groups)
        self.center = center
        self.orig_image = CAR_IMG
        self.image = self.orig_image
        self.velocity = 0
        self.angle = 0
        self.initiated = False
        self.x_pos = center[0]
        self.y_pos = center[1] - TRACK_DIAMETER + 6

    def accelerate(self, MAX_VEL, ACCEL, fleet_list, BREAK_RANGE):
        if self.slower(fleet_list, BREAK_RANGE) > 0:
            self.velocity = max(0, self.velocity - self.slower(fleet_list, BREAK_RANGE))
        else:
            self.velocity = min(self.velocity + ACCEL, MAX_VEL)

    def slower(self, fleet_list, BREAK_RANGE):
        slow_down = 0
        for car in fleet_list:
            if car != self and car.initiated:
                distance = (car.angle - self.angle) % 360
                if distance < BREAK_RANGE:
                    slow_down += (BREAK_RANGE - distance) / BREAK_RANGE * MAX_VEL
        return slow_down
    
    def update_position(self, TRACK_DIAMETER):
        self.angle += self.velocity
        self.x_pos = self.center[0] + (TRACK_DIAMETER - 5) * math.cos(math.radians(self.angle))
        self.y_pos = self.center[1] + (TRACK_DIAMETER - 5) * math.sin(math.radians(self.angle))

    def update(self, *args, **kwargs):
        self.accelerate(MAX_VEL, ACCEL, cars, BREAK_RANGE)
        self.update_position(TRACK_DIAMETER)

        self.rot_image = pygame.transform.rotate(self.orig_image, -self.angle - 90)
        self.rect = self.rot_image.get_rect(center=(self.x_pos, self.y_pos))
        self.image = self.rot_image
        return super().update(*args, **kwargs)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

def text_center(screen: pygame.Surface, text_string: str, x: int, y: int, font_size: int, color: tuple =(255, 255, 255), bg_color: tuple =COLORS["BACKGROUND"]) -> pygame.Surface:
    font = pygame.font.SysFont("freesansbold.ttf", font_size)
    text = font.render(text_string, True, color,COLORS["BACKGROUND"])
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    return screen


car_list = [Car(CENTER_TRACK, cars)]
car_list[-1].initiated = True

running = True
async def main():
    global ACCEL, BREAK_RANGE, NUM_CARS, running, cars, car_list, screen, clock, FPS, MAX_VEL, WIDTH, HEIGHT, SIDEBAR, CENTER_TRACK, TRACK_DIAMETER, COLORS, LEFT_ARROW, RIGHT_ARROW, CAR_IMG
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    cars.empty()
                    car_list = [Car(CENTER_TRACK, cars)]
                    car_list[-1].initiated = True
                if event.key == pygame.K_s:
                    ACCEL = 0.01
                    BREAK_RANGE = 15
                    NUM_CARS = 15
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3)[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    #decrease number of cars
                    if WIDTH + SIDEBAR // 2 - 30 < mouse_pos[0] < WIDTH + SIDEBAR // 2 - 20 and 75 < mouse_pos[1] < 85:
                        NUM_CARS = max(1, NUM_CARS - 1)
                    #increase number of cars
                    if WIDTH + SIDEBAR // 2 + 20 < mouse_pos[0] < WIDTH + SIDEBAR // 2 + 30 and 75 < mouse_pos[1] < 85 and NUM_CARS > 1:
                        NUM_CARS += 1
                    #decrease acceleration
                    if WIDTH + SIDEBAR // 2 - 30 < mouse_pos[0] < WIDTH + SIDEBAR // 2 - 20 and 125 < mouse_pos[1] < 135 and ACCEL > 0.001:
                        ACCEL = max(0.005, ACCEL - 0.005)
                    #increase acceleration
                    if WIDTH + SIDEBAR // 2 + 20 < mouse_pos[0] < WIDTH + SIDEBAR // 2 + 30 and 125 < mouse_pos[1] < 135:
                        ACCEL += 0.005
                    #decrease break range
                    if WIDTH + SIDEBAR // 2 - 30 < mouse_pos[0] < WIDTH + SIDEBAR // 2 - 20 and 185 < mouse_pos[1] < 195 and BREAK_RANGE > 1:
                        BREAK_RANGE = max(1, BREAK_RANGE - 1)
                    #increase break range
                    if WIDTH + SIDEBAR // 2 + 20 < mouse_pos[0] < WIDTH + SIDEBAR // 2 + 30 and 185 < mouse_pos[1] < 195:
                        BREAK_RANGE += 1

        
        # check if starting position is free
        new_car = True
        for car in cars:
            if (car.angle % 360) < BREAK_RANGE or (car.angle % 360) > (360 - BREAK_RANGE):
                new_car = False
                break
        if new_car and len(car_list) < NUM_CARS:
            car_list.append(Car(CENTER_TRACK, cars))
            car_list[-1].initiated = True
        if len(car_list) > NUM_CARS:
            car_list[0].kill()
            car_list.pop(0)
        
        cars.update(MAX_VEL, ACCEL, cars, BREAK_RANGE)

        mean_velocity = sum(car.velocity for car in cars) / len(cars) if cars else 0
        max_velocity = max(car.velocity for car in cars) if cars else 0
        min_velocity = min(car.velocity for car in cars) if cars else 0

        screen.fill(COLORS["BACKGROUND"])

        #outer circle
        pygame.draw.circle(screen, COLORS["FRAME"], CENTER_TRACK, TRACK_DIAMETER - + 25, width=5)

        #inner circle
        pygame.draw.circle(screen, COLORS["FRAME"], CENTER_TRACK, TRACK_DIAMETER - - 20, width=5)
        pygame.draw.rect(screen, COLORS["BACKGROUND"], (0, HEIGHT/2 - 70, WIDTH, 140))
        pygame.draw.line(screen, COLORS["FRAME"], (92, HEIGHT/2 - 73), (WIDTH - 92, HEIGHT/2 - 73), width=5)
        pygame.draw.line(screen, COLORS["FRAME"], (92, HEIGHT/2 + 72), (WIDTH - 92, HEIGHT/2 + 72), width=5)

        #draw race track
        pygame.draw.circle(screen, (111,111,111), CENTER_TRACK, TRACK_DIAMETER, width=10)

        cars.draw(screen)

        #display variables
        screen = text_center(screen, f"Number of Cars: {len(car_list)}/{NUM_CARS}", CENTER_TRACK[1], CENTER_TRACK[0] + 35, 14)
        screen = text_center(screen, "Velocity", CENTER_TRACK[1], CENTER_TRACK[0] - 35, 20)
        screen = text_center(screen, f'Max: {max_velocity:.2f}', CENTER_TRACK[1] + 140, CENTER_TRACK[0] - 10, 12)
        screen = text_center(screen, f'Min: {min_velocity:.2f}', CENTER_TRACK[1] - 130, CENTER_TRACK[0] - 10, 12)
        screen = text_center(screen, f'Mean: {mean_velocity:.2f}', CENTER_TRACK[1], CENTER_TRACK[0] + 10, 12)

        #draw velocity bar
        pygame.draw.line(screen, (38,115,101), ((CENTER_TRACK[1] - (0.5 - min_velocity) * 200), CENTER_TRACK[0] - 10), ((CENTER_TRACK[1] + (max_velocity - 0.5) * 200), CENTER_TRACK[0] - 10), width=10)
        
        pygame.draw.line(screen, COLORS["HIGHLIGHT"], ((CENTER_TRACK[1] - 100 + mean_velocity * 200), CENTER_TRACK[0] - 15), ((CENTER_TRACK[1] - 100 + mean_velocity * 200), CENTER_TRACK[0] - 5), width=3)
        
        #draw title
        screen = text_center(screen, "TRAFFIC JAM:", CENTER_TRACK[1], CENTER_TRACK[0] - 73, 30)
        screen = text_center(screen, "SIMULATOR", CENTER_TRACK[1], CENTER_TRACK[0] + 73, 30)

        #draw sidebar
        pygame.draw.rect(screen, COLORS["SIDEBAR"], (WIDTH, 0, SIDEBAR, HEIGHT))
        screen = text_center(screen, "Controls", WIDTH + SIDEBAR // 2, 30, 30, bg_color=COLORS["SIDEBAR"])
        #number of cars
        screen = text_center(screen, "Number of Cars:", WIDTH + SIDEBAR // 2, 60, 16, bg_color=COLORS["SIDEBAR"])
        screen = text_center(screen, f"{NUM_CARS}", WIDTH + SIDEBAR // 2, 80, 16, bg_color=COLORS["SIDEBAR"])
        screen.blit(LEFT_ARROW, (WIDTH + SIDEBAR // 2 - 30, 75))
        screen.blit(RIGHT_ARROW, (WIDTH + SIDEBAR // 2 + 20, 75))
        
        #acceleration
        screen = text_center(screen, "Acceleration:", WIDTH + SIDEBAR // 2, 110, 16, bg_color=COLORS["SIDEBAR"])
        screen = text_center(screen, f"{ACCEL:.3f}", WIDTH + SIDEBAR // 2, 130, 16, bg_color=COLORS["SIDEBAR"])
        screen.blit(LEFT_ARROW, (WIDTH + SIDEBAR // 2 - 30, 125))
        screen.blit(RIGHT_ARROW, (WIDTH + SIDEBAR // 2 + 20, 125))

        #break range
        screen = text_center(screen, "Break Range:", WIDTH + SIDEBAR // 2, 170, 16, bg_color=COLORS["SIDEBAR"])
        screen = text_center(screen, f"{BREAK_RANGE}", WIDTH + SIDEBAR // 2, 190, 16, bg_color=COLORS["SIDEBAR"])
        screen.blit(LEFT_ARROW, (WIDTH + SIDEBAR // 2 - 30, 185))
        screen.blit(RIGHT_ARROW, (WIDTH + SIDEBAR // 2 + 20, 185))

        #restart info
        screen = text_center(screen, "(r) for restart", WIDTH + SIDEBAR // 2, HEIGHT - 20, 14, bg_color=COLORS["SIDEBAR"])
        #reset info
        screen = text_center(screen, "(s) for reset", WIDTH + SIDEBAR // 2, HEIGHT - 40, 14, bg_color=COLORS["SIDEBAR"])    

        pygame.display.flip()
        await asyncio.sleep(0)  # Let other tasks run

    #pygame.quit()

asyncio.run(main())