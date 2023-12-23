import random
from collections import deque
from itertools import chain

import pygame as pg

from settings import *
from sprites import *


def poprandom(deque):
    """
    Removes the element at the given index from the deque.
    """
    index = random.randint(0, len(deque) - 1)

    if index == 0:
        return deque.popleft()
    elif index == len(deque) - 1:
        return deque.pop()
    else:
        deque.rotate(-index)
        elem = deque.popleft()
        deque.rotate(index)
        return elem


class Game():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(NAME)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.playing = True
        self.all_sprites = pg.sprite.Group()
        self.rooms = []
        self.corridors = []

        # Sampling NxM generated dungeons, and spreading them in the screen
        N = 7
        M = 6

        for i in range(N):
            for j in range(M):
                X = i * WIDTH / N + WIDTH / (2 * N)
                Y = j * HEIGHT / M + HEIGHT / (2 * M)

                gen_rooms, gen_corridors = self.generate_dungeon_expand(
                    "RFS", X, Y)
                self.rooms.extend(gen_rooms)
                self.corridors.extend(gen_corridors)

    def generate_dungeon_expand(self, type, x=WIDTH / 2, y=HEIGHT / 2):
        """
        Generates a dungeon using the expansion part of search algorithms.
        In particular, it uses the path expansion of:

        - BFS: Breadth First Search.
        - DFS: Depth First Search.
        - RFS: Random First Search.

        It uses a deque for all methods, what changes is the way elements are removed from the deque.
        For BFS it uses popleft(),  for DFS it uses pop() and RFS it pops a random element.

        type: "BFS", "DFS", "RFS"
        """
        rooms = []
        corridors = []

        # define the actual room as the first room of the dungeon
        actual_room = Room(self, x, y, 10, 10, R_START)
        rooms.append(actual_room)

        # define a deque to store the rooms that we need to visit
        frontier = deque()
        frontier.append(actual_room)

        # define the generation queue to decide the order of the rooms
        gen_queue = deque(GENERATION_QUEUE)

        # while the frontier is not empty and we don't have enough rooms
        while len(frontier) != 0 and len(rooms) < N_ROOMS and len(gen_queue) != 0:
            # pop the next element of the frontier
            if type == 'BFS':
                actual_room = frontier.popleft()
            elif type == 'DFS':
                actual_room = frontier.pop()
            else:
                actual_room = poprandom(frontier)

            # For RFS, we shuffle the directions
            if type == 'RFS':
                random.shuffle(actual_room.allowed_connections)

            # for each direction of the actual room
            for dir in actual_room.allowed_connections:
                # if we don't have any more rooms to build, then we stop
                if len(gen_queue) == 0:
                    break

                # get the next room type and size from the generation queue
                room_type, room_sizes, should_expand = gen_queue.popleft()

                corridor_lenght = 2
                room_size = random.choice(room_sizes)
                room = self.make_room(
                    actual_room, dir, corridor_lenght, room_size, room_type, should_expand)

                # check if the room collides with any other element in the dungeon
                for elem in chain(rooms, corridors):
                    if elem.hit_rect.colliderect(room.hit_rect):
                        # if it does, then we can't build in that direction
                        gen_queue.appendleft(
                            (room_type, room_sizes, should_expand))
                        break
                else:
                    # if it doesn't, then we can build the room and the corridor
                    rooms.append(room)
                    corridors.append(self.make_corridor(
                        actual_room, room, dir))

                    # and add the room to the frontier
                    frontier.append(room)

                # if we are using RFS, we only build one room per iteration
                if type == 'RFS':
                    break

            # if we are using RFS, we only build one room per iteration
            # we remove the used dir, add the actual room to the frontier
            if type == 'RFS' and len(actual_room.allowed_connections) > 1:
                actual_room.allowed_connections.remove(dir)
                frontier.append(actual_room)

        return rooms, corridors

    def make_room(self, actual_room, dir, corridor_lenght, size, color, should_expand):
        """
        Given a room, and a direction, generates a new room
        """

        w, h = size, size
        x, y = 0, 0

        if dir == "up":
            x = actual_room.rect.centerx - w / 2
            y = actual_room.rect.y - corridor_lenght - h

        if dir == "down":
            x = actual_room.rect.centerx - w / 2
            y = actual_room.rect.y + corridor_lenght + actual_room.rect.height

        if dir == "left":
            x = actual_room.rect.x - corridor_lenght - w
            y = actual_room.rect.centery - h / 2

        if dir == "right":
            x = actual_room.rect.x + corridor_lenght + actual_room.rect.width
            y = actual_room.rect.centery - h / 2

        return Room(self, x, y, w, h, color, should_expand)

    def make_corridor(self, actual_room, r, dir):
        """
        Builds a corridor between `actual_room` and `r` in the given direction
        """
        c = None

        if dir == "up":
            c = Corridor(self, actual_room.rect.centerx - 2, r.rect.bottom,
                         4, actual_room.rect.top - r.rect.bottom, GREY)

        if dir == "down":
            c = Corridor(self, actual_room.rect.centerx - 2, actual_room.rect.bottom,
                         4, r.rect.top - actual_room.rect.bottom, GREY)

        if dir == "left":
            c = Corridor(self, r.rect.right, r.rect.centery - 2,
                         actual_room.rect.x - r.rect.right, 4, GREY)

        if dir == "right":
            c = Corridor(self, actual_room.rect.right, actual_room.rect.centery -
                         2, r.rect.x - actual_room.rect.right, 4, GREY)

        return c

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.drawing()

    def events(self):
        # game loop events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing == True:
                    self.playing = False
                self.running = False

            # new code
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

    def update(self):
        self.all_sprites.update()

    def drawing(self):
        self.window.fill(BLACK)
        self.all_sprites.draw(self.window)

        for room in self.rooms:
            room.draw(self.window)

        for corridor in self.corridors:
            corridor.draw(self.window)

        pg.display.flip()


game = Game()
while game.running:
    game.new()
    game.run()

pg.quit()
