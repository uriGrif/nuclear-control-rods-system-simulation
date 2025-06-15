import pygame
import random
import math

# --- Configuración ---
WIDTH, HEIGHT = 700, 500
FPS = 60
NEUTRON_VELOCITY = 2
NEUTRON_RADIUS = 3
FUEL_RODS_AMOUNT = 5
CONTROL_RODS_AMOUNT = 2
NEUTRONS_PER_FISSION = 3

control_rods_height = 200 # valor inicial

# Slider para controlar el setpoint de neutrones
slider_x = 150
slider_y = 460
slider_width = 300
slider_height = 10
slider_handle_radius = 8
slider_active = False
neutron_target = 500  # valor inicial

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
reloj = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# --- Clases ---
class Neutron:
    def __init__(self, x, y):
        self.origin = (x, y)
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * NEUTRON_VELOCITY
        self.dy = math.sin(angle) * NEUTRON_VELOCITY

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
            return False # no contar colision con un neutron propio
        dx = self.x - neutron.x
        dy = self.y - neutron.y
        return dx * dx + dy * dy < (self.radius + NEUTRON_RADIUS) ** 2

class BarraControl:
    def __init__(self, x, altura):
        self.x = x
        self.altura = altura
        self.ancho = 10
        self.y = 20

    def move(self, nueva_altura):
        self.altura = nueva_altura
        self.y = HEIGHT // 2 - nueva_altura // 2

    def draw(self, display):
        pygame.draw.rect(display, (50, 50, 50), (self.x, self.y, self.ancho, self.altura))

    def colisions(self, neutron):
        return (self.x <= neutron.x <= self.x + self.ancho and
                self.y <= neutron.y <= self.y + self.altura)

# --- Inicialización ---
fuel_rods = [BarraCombustible(x, y) for x in range(100, 700, 120) for y in range(150, 450, 100)]
control_rods = [BarraControl(x, control_rods_height) for x in range(160, 600, 120)]
neutrons = []

def controller():
    """
    Función vacía para implementar control PID más adelante.
    """
    pass

def emit_neutrons(origin, cantidad):
    for _ in range(cantidad):
        neutrons.append(Neutron(origin.x, origin.y))

def position_to_neutron_value(pos_x):
    pos_x = max(slider_x, min(slider_x + slider_width, pos_x))
    rel = (pos_x - slider_x) / slider_width
    return int(rel * 1000)

# Emitimos neutrones iniciales
for rod in fuel_rods:
    emit_neutrons(rod, NEUTRONS_PER_FISSION)

# --- Bucle principal ---
corriendo = True
while corriendo:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            corriendo = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if slider_y - slider_height / 2 <= my <= slider_y + slider_height / 2 and slider_x <= mx <= slider_x + slider_width:
                slider_active = True
        elif ev.type == pygame.MOUSEBUTTONUP:
            slider_active = False
    
    if slider_active:
        mx, _ = pygame.mouse.get_pos()
        neutron_target = position_to_neutron_value(mx)

    display.fill((240, 240, 240))

    # Control PID (por ahora vacío)
    controller()

    # Mover y procesar neutrones
    for n in neutrons:
        n.bounce()
        n.move()

        # Colisión con barras de combustible
        colision = False
        for f in fuel_rods:
            if f.colisions(n):
                emit_neutrons(f, NEUTRONS_PER_FISSION)
                colision = True
                neutrons.remove(n)
                break

        # Colisión con barras de control
        if not colision:
            for c in control_rods:
                if c.colisions(n):
                    colision = True
                    neutrons.remove(n)
                    break

    # Dibujar elementos
    for f in fuel_rods:
        f.draw(display)
    for c in control_rods:
        c.draw(display)
    for n in neutrons:
        n.draw(display)


    # Mostrar contador
    texto = font.render(f"Neutrones activos: {len(neutrons)}", True, (0, 0, 0))
    display.blit(texto, (10, 10))

    # Mostrar barra de control
    # Barra base
    pygame.draw.rect(display, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))

    # Posición del handle
    handle_x = int(slider_x + (neutron_target / 1000) * slider_width)
    pygame.draw.circle(display, (100, 100, 255), (handle_x, slider_y + slider_height // 2), slider_handle_radius)

    # Mostrar valor
    slider_text = font.render(f"Setpoint de neutrones: {neutron_target}", True, (0, 0, 0))
    display.blit(slider_text, (slider_x, slider_y - 20))

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
