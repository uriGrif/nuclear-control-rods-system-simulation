import pygame
import random
import math

WIDTH, HEIGHT = 700, 500
FPS = 60
NEUTRON_VELOCITY = 2
NEUTRON_RADIUS = 3
NEUTRONS_PER_FISSION = 3
CONTROL_RODS_HEIGHT = 500
MAXIMUM_NEUTRON_LIFESPAN = 200
K_PROPORTIONAL = 1.07
K_INTEGRAL = 0.0001
K_DERIVATIVE = 0.28
MAX_ACCUMULATED_ERROR = 5000

enable_P = True
enable_I = True
enable_D = True

slider_x = 150
slider_y = 460
slider_width = 300
slider_height = 10
slider_handle_radius = 8

class Neutron:
    def __init__(self, x, y):
        self.origin = (x, y)
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * NEUTRON_VELOCITY
        self.dy = math.sin(angle) * NEUTRON_VELOCITY
        self.lifespan = 0

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, display):
        pygame.draw.circle(display, (0, 0, 255), (int(self.x), int(self.y)), NEUTRON_RADIUS)

    def bounce(self):
        if self.x < 0 or self.x > WIDTH:
            self.dx = -self.dx
        if self.y < 0 or self.y > HEIGHT:
            self.dy = -self.dy

class BarraCombustible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20

    def draw(self, display):
        pygame.draw.circle(display, (0, 255, 0), (self.x, self.y), self.radius)

    def colisions(self, neutron):
        if neutron.origin == (self.x, self.y):
            return False
        dx = self.x - neutron.x
        dy = self.y - neutron.y
        return dx * dx + dy * dy < (self.radius + NEUTRON_RADIUS) ** 2

class BarraControl:
    def __init__(self, x, altura):
        self.x = x
        self.altura = altura
        self.ancho = 10
        self.y = 0

    def move(self, dy):
        if 0 <= self.y + self.altura + dy <= HEIGHT:
            self.y += dy

    def draw(self, display):
        pygame.draw.rect(display, (50, 50, 50), (self.x, self.y, self.ancho, self.altura))

    def colisions(self, neutron):
        return self.x <= neutron.x <= self.x + self.ancho and self.y <= neutron.y <= self.y + self.altura

def run_simulador(q):
    pygame.init()
    global enable_P, enable_I, enable_D
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    reloj = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    neutron_target = 500
    accumulated_error = 0
    previous_error = 0
    slider_active = False
    frame_count = 0

    fuel_rods = [BarraCombustible(x, y) for x in range(100, 700, 120) for y in range(150, 450, 100)]
    control_rods = [BarraControl(x, CONTROL_RODS_HEIGHT) for x in range(40, 720, 120)]
    neutrons = []
    for rod in fuel_rods:
        for _ in range(NEUTRONS_PER_FISSION):
            neutrons.append(Neutron(rod.x, rod.y))

    corriendo = True
    perturbation1 = 0
    perturbation2 = 0

    while corriendo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if slider_y - slider_height / 2 <= my <= slider_y + slider_width:
                    slider_active = True
                elif 20 <= mx <= 180 and 400 <= my <= 430:
                    # Perturbación 1: aumento de neutrones
                    for _ in range(200):
                        neutrons.append(Neutron(random.randint(100, 600), random.randint(100, 400)))
                    perturbation1 = 200
                elif 200 <= mx <= 360 and 400 <= my <= 430:
                    # Perturbación 2: mover barras aleatoriamente
                    perturbation2 = random.choice([-200, 200])
                    for rod in control_rods:
                        rod.move(perturbation2)
                # Interruptor P
                elif 380 <= mx <= 460 and 400 <= my <= 430:
                    enable_P = not enable_P
                elif 470 <= mx <= 550 and 400 <= my <= 430:
                    enable_I = not enable_I
                elif 560 <= mx <= 640 and 400 <= my <= 430:
                    enable_D = not enable_D

            elif ev.type == pygame.MOUSEBUTTONUP:
                slider_active = False

        if slider_active:
            mx, _ = pygame.mouse.get_pos()
            pos_x = max(slider_x, min(slider_x + slider_width, mx))
            rel = (pos_x - slider_x) / slider_width
            neutron_target = int(rel * 1000)

        # PID

        Kp = K_PROPORTIONAL if enable_P else 0
        Ki = K_INTEGRAL if enable_I else 0
        Kd = K_DERIVATIVE if enable_D else 0


        error = neutron_target - len(neutrons)
        accumulated_error += error * (1/FPS)
        derivative = (error - previous_error) / (1 / FPS)
        previous_error = error
        proportional_control = Kp * error
        derivative_control = Kd * derivative
        integral_control = Ki * accumulated_error
        
        control_signal = (
           proportional_control +
            derivative_control +
            integral_control
        )

        for rod in control_rods:
            rod.move(-control_signal * 0.05)

        new_neutrons = []
        for n in neutrons[:]:
            n.bounce()
            n.move()
            n.lifespan += 1
            if n.lifespan > MAXIMUM_NEUTRON_LIFESPAN:
                neutrons.remove(n)
                continue
            colision = False
            for f in fuel_rods:
                if f.colisions(n):
                    for _ in range(NEUTRONS_PER_FISSION):
                        new_neutrons.append(Neutron(f.x, f.y))
                    neutrons.remove(n)
                    colision = True
                    break
            if not colision:
                for c in control_rods:
                    if c.colisions(n):
                        neutrons.remove(n)
                        break
        neutrons.extend(new_neutrons)
        if len(neutrons) < 1:
            for rod in fuel_rods:
                for _ in range(NEUTRONS_PER_FISSION):
                    neutrons.append(Neutron(rod.x, rod.y))

        # Enviar el error a la cola
        q.put((error, proportional_control,derivative_control,integral_control, neutron_target, len(neutrons), perturbation1, perturbation2))

        # Dibujar
        display.fill((240, 240, 240))
        for f in fuel_rods: f.draw(display)
        for c in control_rods: c.draw(display)
        for n in neutrons: n.draw(display)
        texto = font.render(f"Neutrones activos: {len(neutrons)}", True, (0, 0, 0))
        display.blit(texto, (10, 10))
        pygame.draw.rect(display, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))
        handle_x = int(slider_x + (neutron_target / 1000) * slider_width)
        pygame.draw.circle(display, (100, 100, 255), (handle_x, slider_y + slider_height // 2), slider_handle_radius)
        slider_text = font.render(f"Setpoint de neutrones: {neutron_target}", True, (0, 0, 0))
        display.blit(slider_text, (slider_x, slider_y - 20))

        # Botón Perturbación 1
        pygame.draw.rect(display, (255, 180, 180), (20, 400, 160, 30))
        text1 = font.render("Perturbación 1", True, (0, 0, 0))
        display.blit(text1, (30, 405))

        # Botón Perturbación 2
        pygame.draw.rect(display, (180, 200, 255), (200, 400, 160, 30))
        text2 = font.render("Perturbación 2", True, (0, 0, 0))
        display.blit(text2, (210, 405))

        perturbation1 = 0
        perturbation2 = 0

        # Botones interruptores PID
      # Botones interruptores PID a la derecha de los de perturbación
        pygame.draw.rect(display, (180, 255, 180) if enable_P else (255, 180, 180), (380, 400, 80, 30))
        textP = font.render("P ON" if enable_P else "P OFF", True, (0, 0, 0))
        display.blit(textP, (390, 405))

        pygame.draw.rect(display, (180, 255, 180) if enable_I else (255, 180, 180), (470, 400, 80, 30))
        textI = font.render("I ON" if enable_I else "I OFF", True, (0, 0, 0))
        display.blit(textI, (480, 405))

        pygame.draw.rect(display, (180, 255, 180) if enable_D else (255, 180, 180), (560, 400, 80, 30))
        textD = font.render("D ON" if enable_D else "D OFF", True, (0, 0, 0))
        display.blit(textD, (570, 405))


        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
