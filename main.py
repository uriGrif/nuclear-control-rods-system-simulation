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
control_rods = [BarraControl(x, 300) for x in range(160, 600, 120)]
neutrons = []

def controller():
    """
    Función vacía para implementar control PID más adelante.
    """
    pass

def emit_neutrons(origin, cantidad):
    for _ in range(cantidad):
        neutrons.append(Neutron(origin.x, origin.y))

# Emitimos neutrones iniciales
for rod in fuel_rods:
    emit_neutrons(rod, NEUTRONS_PER_FISSION)

# --- Bucle principal ---
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

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

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
