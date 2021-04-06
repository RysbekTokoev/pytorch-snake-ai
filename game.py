import pygame, sys, time, random
import constants



class Game():
    def __init__(self):
        check_errors = pygame.init()
        # if check_errors[1] > 0:
        #     print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        #     sys.exit(-1)
        # else:
        #     print('[+] Game successfully initialised')

        # Initialise game window
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode((constants.frame_size_x, constants.frame_size_y))
        self.reset()

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

    # Score
    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (constants.frame_size_x/10, 15)
        else:
            score_rect.midtop = (constants.frame_size_x/2, constants.frame_size_y/1.25)
        self.game_window.blit(score_surface, score_rect)
        # pygame.display.flip()

    # Game Over
    def game_over(self):
        my_font = pygame.font.SysFont('times new roman')
        game_over_surface = my_font.render('YOU DIED', True, constants.red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (constants.frame_size_x / 2, constants.frame_size_y / 4)
        self.game_window.fill(constants.black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.show_score(0, constants.red, 'times', 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def reset(self):
        self.direction = 2
        self.change_to = self.direction
        self.score = 0
        self.player = constants.player
        # Game variables
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

        self.food_pos = [random.randrange(1, (constants.frame_size_x // 10)) * 10, random.randrange(1, (constants.frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.is_game_over = False
        self.frame_iteration = 0


    # Make chosen move
    def make_move(self, way):
        # 0 1 2 3
        # U L R D
        if not constants.player:
            way = self._way_to_direction(way)

        if (self.direction + way) != 3:
            self.direction = way
        self.snake_pos[constants.moves[self.direction][0]] += constants.moves[self.direction][1]

        # Snake body growing mechanism
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
            return 10
        else:
            self.snake_body.pop()
            return 0

    def _way_to_direction(self, way):
        if (self.direction == 1 and way == [0, 1, 0]) or (self.direction == 2 and way == [1, 0, 0]):
            return 0
        elif (self.direction == 1 and way == [1, 0, 0]) or (self.direction == 2 and way == [0, 1, 0]):
            return 3
        elif (self.direction == 0 and way == [1, 0, 0]) or (self.direction == 3 and way == [0, 1, 0]):
            return 1
        elif (self.direction == 0 and way == [0, 1, 0]) or (self.direction == 3 and way == [1, 0, 0]):
            return 2
        else:
            return self.direction
    # Generate Food
    def food(self):
        # Spawning food on the screen
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (constants.frame_size_x // 10)) * 10,
                             random.randrange(1, (constants.frame_size_y // 10)) * 10]
        self.food_spawn = True

        # GFX
        self.game_window.fill(constants.black)
        for pos in self.snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(self.game_window, constants.green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(self.game_window, constants.white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

    # Get inputed move and Make it

    # Main block
    def play(self, action):
        self.frame_iteration += 1;
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if constants.player:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.change_to = 0
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.change_to = 3
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.change_to = 1
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.change_to = 2

        if not constants.player:
            self.change_to = action

        reward = self.make_move(self.change_to)
        self.food()


        if self.is_colision():
            self.is_game_over = True
            reward -= 10;

        self.show_score(1, constants.white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        self.fps_controller.tick(constants.difficulty)

        return reward, self.is_game_over, self.score

    # Game Over conditions
    def is_colision(self, pt=None):
        if not pt:
            pt = self.snake_pos
        if (pt[0] < 0 or pt[0] > constants.frame_size_x-10) \
                or (pt[1] < 0 or pt[1] > constants.frame_size_y-10) \
                or (self.frame_iteration > 100*(self.score+3)):
            return True

        # Touching the snake body
        for block in self.snake_body[1:]:
            if pt[0] == block[0] and pt[1] == block[1]:
                return True
        return False


if __name__ == "__main__":
    game = Game()
    while True:
        reward, game_over, score = game.play()
        if game_over:
            game.reset()

    pygame.quit()
