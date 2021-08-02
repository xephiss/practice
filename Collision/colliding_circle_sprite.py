import pygame


class CollidingCircle(pygame.sprite.Sprite):
    def __init__(self, radius, position, velocity, colour,
                 window_size, circles_group: pygame.sprite.AbstractGroup):
        super().__init__(circles_group)

        self.radius = radius
        # Note: using pygame's vector class for the position and velocity of the circles
        # this is because it uses floating point values, unlike the Rect class, so we can move
        # tiny amounts per frame rather than always a whole pixel - and it has some useful helper
        # functions.
        self.position = pygame.math.Vector2(position[0], position[1])
        self.velocity = pygame.math.Vector2(velocity[0], velocity[1])
        self.window_size = window_size
        self.circles_group = circles_group

        # This just draws a circle onto a surface with a transparent background
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, colour, (radius, radius), radius)

        self.rect = pygame.Rect(0, 0, radius*2, radius*2)
        self.rect.center = position

        self.collision_normal = pygame.math.Vector2(0.0, 0.0)

    def update(self, time_delta):
        self.position += (self.velocity * time_delta)

        # collide off window edges and bounce
        if self.position.x + self.radius >= self.window_size[0]:
            self.position.x = self.window_size[0] - self.radius
            # the collision normal here is  representing a vector pointing inward
            # from one of the window edges. And because the window edges don't change
            # neither doe the vector
            self.collision_normal = pygame.math.Vector2(-1.0, 0.0)
            self.velocity.reflect_ip(self.collision_normal)

        if self.position.x - self.radius <= 0.0:
            self.position.x = 0.0 + self.radius
            self.collision_normal = pygame.math.Vector2(1.0, 0.0)
            self.velocity.reflect_ip(self.collision_normal)

        if self.position.y + self.radius >= self.window_size[1]:
            self.position.y = self.window_size[1] - self.radius
            self.collision_normal = pygame.math.Vector2(0.0, -1.0)
            self.velocity.reflect_ip(self.collision_normal)

        if self.position.y - self.radius <= 0.0:
            self.position.y = 0.0 + self.radius
            self.collision_normal = pygame.math.Vector2(0.0, 1.0)
            self.velocity.reflect_ip(self.collision_normal)

        for circle in self.circles_group.sprites():
            if circle != self:
                safe_distance = self.radius + circle.radius
                if self.position.distance_to(circle.position) <= safe_distance:

                    # once we have detected that two circles are overlapping we create a
                    # normal vector for each based off the direction between the two sphere centres
                    # and use this to reflect the circles heading.
                    # it's not amazing physics but approximates a bounce, you could spend a lot
                    # of time making a better approximation accounting for objects passing their
                    # velocity onto things they collide with, object's mass, spin & friction
                    # and so on. This is very simple, and if you watch iut for a while you will see
                    # where it breaks down
                    self.collision_normal = (self.position - circle.position).normalize()
                    self.velocity.reflect_ip(self.collision_normal)

                    circle.collision_normal = (circle.position - self.position).normalize()
                    circle.velocity.reflect_ip(circle.collision_normal)

                    # we need to make sure that the circles are no longer touching before finishing
                    # otherwise they can get stuck overlapping, flipping the heading back and forth
                    # as the game loop progress between frames

                    # get the length of the overlap + 1 pixel in case they are just touching
                    overlap = (safe_distance - self.position.distance_to(circle.position)) + 1.0
                    # split it in half
                    half_overlap = overlap * 0.5
                    # then move the circles apart down the collision normal
                    self.position += (self.collision_normal * half_overlap)
                    circle.position += (circle.collision_normal * half_overlap)

        self.rect.center = self.position
