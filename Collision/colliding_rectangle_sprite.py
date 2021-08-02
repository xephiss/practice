import pygame

class CollidingRectangle(pygame.sprite.Sprite):
    def __init__(self, width, height, position, velocity, colour,
            window_size, rectangles_group: pygame.sprite.AbstractGroup):
        super().__init__(rectangles_group)

        self.width = width
        self.height = height

        self.position = pygame.math.Vector2(position[0], position[1])
        self.velocity = pygame.math.Vector2(velocity[0], velocity[1])
        self.window_size = window_size
        self.rectangles_group = rectangles_group

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        pygame.draw.rect(self.image, colour, width, height)

        self.rect = pygame.Rect(0,0, width, height)
        self.rect.center = position

        self.collision_normal = pygame.math.Vector2(0.0, 0.0)

    def update(self, time_delta):
        self.position += (self.velocity * time_delta)

        # collide off window edges and bounce
        if self.position.x + self.width >= self.window_size[0]:
            self.position.x = self.window_size[0] - self.width
            # the collision normal here is  representing a vector pointing inward
            # from one of the window edges. And because the window edges don't change
            # neither doe the vector
            self.collision_normal = pygame.math.Vector2(-1.0, 0.0)
            self.velocity.reflect_ip(self.collision_normal)

        if self.position.x - self.width <= 0.0:
            self.position.x = 0.0 + self.width
            self.collision_normal = pygame.math.Vector2(1.0, 0.0)
            self.velocity.reflect_ip(self.collision_normal)

        if self.position.y + self.height >= self.window_size[1]:
            self.position.y = self.window_size[1] - self.height
            self.collision_normal = pygame.math.Vector2(0.0, -1.0)
            self.velocity.reflect_ip(self.collision_normal)

        if self.position.y - self.height <= 0.0:
            self.position.y = 0.0 + self.height
            self.collision_normal = pygame.math.Vector2(0.0, 1.0)
            self.velocity.reflect_ip(self.collision_normal)

        for rectangle in self.rectangles_group.sprites():
            if rectangle != self:
                safe_distance = self.width + self.height
                if self.position.distance_to(rectangle.position) <= safe_distance:

                    # once we have detected that two circles are overlapping we create a
                    # normal vector for each based off the direction between the two sphere centres
                    # and use this to reflect the circles heading.
                    # it's not amazing physics but approximates a bounce, you could spend a lot
                    # of time making a better approximation accounting for objects passing their
                    # velocity onto things they collide with, object's mass, spin & friction
                    # and so on. This is very simple, and if you watch iut for a while you will see
                    # where it breaks down
                    self.collision_normal = (self.position - rectangle.position).normalize()
                    self.velocity.reflect_ip(self.collision_normal)

                    rectangle.collision_normal = (rectangle.position - self.position).normalize()
                    rectangle.velocity.reflect_ip(rectangle.collision_normal)

                    # we need to make sure that the circles are no longer touching before finishing
                    # otherwise they can get stuck overlapping, flipping the heading back and forth
                    # as the game loop progress between frames

                    # get the length of the overlap + 1 pixel in case they are just touching
                    overlap = (safe_distance - self.position.distance_to(rectangle.position)) + 1.0
                    # split it in half
                    half_overlap = overlap * 0.5
                    # then move the circles apart down the collision normal
                    self.position += (self.collision_normal * half_overlap)
                    rectangle.position += (rectangle.collision_normal * half_overlap)

        self.rect.center = self.position
