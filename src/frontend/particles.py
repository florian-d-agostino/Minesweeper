import arcade
import random
import math

class Particle(arcade.SpriteCircle):
    def __init__(self, x, y):
        # Random size
        radius = random.randint(4, 10)

        # Initial electric blue color
        super().__init__(radius=radius, color=(80, 180, 255))

        self.center_x = x
        self.center_y = y

        # Random direction
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 5)
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed

        # Rotation
        self.change_angle = random.uniform(-5, 5)

        # Transparency
        self.alpha = 255

        # Lifespan
        self.fade_speed = random.uniform(1.5, 3)

    def update(self, delta_time=0):
        # Movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rotation
        self.angle += self.change_angle

        # Fade-out
        self.alpha -= self.fade_speed
        if self.alpha < 0:
            self.alpha = 0

        # Blue → cyan → white gradient
        r = min(255, int(80 + (255 - 80) * (1 - self.alpha / 255)))
        g = min(255, int(180 + (255 - 180) * (1 - self.alpha / 255)))
        b = min(255, int(255 + (255 - 255) * (1 - self.alpha / 255)))

        self.color = (r, g, b, int(self.alpha))

        # Removal
        if self.alpha <= 0:
            self.remove_from_sprite_lists()


class EnergyWave:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1
        self.alpha = 200

    def update(self, delta_time=0):
        self.radius += 6
        self.alpha -= 4
        if self.alpha < 0:
            self.alpha = 0

    def draw(self):
        arcade.draw_circle_outline(
            self.x,
            self.y,
            self.radius,
            (120, 200, 255, int(self.alpha)),
            border_width=4
        )

    @property
    def finished(self):
        return self.alpha <= 0


class Explosion:
    def __init__(self, x, y, count=50):
        self.particles = arcade.SpriteList()
        for _ in range(count):
            self.particles.append(Particle(x, y))

        self.wave = EnergyWave(x, y)

    def update(self, delta_time=0):
        self.particles.update()
        self.wave.update()

    def draw(self):
        self.particles.draw()
        self.wave.draw()

    @property
    def finished(self):
        return len(self.particles) == 0 and self.wave.finished