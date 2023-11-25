import random
import pygame
from customizze import *
from sprite import *



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.create_word_list()
    
    def create_word_list(self):
        with open("words.txt", "r") as file:
            self.words_list = file.read().splitlines()

    def new(self):
        self.word = random.choice(self.words_list).upper()
        self.text = ""
        self.current_row = 0
        self.tiles = []
        self.create_tiles()
        self.flip = True
        self.not_enough_letters = False
        self.timer = 0
    def create_tiles(self):
        for row in range(6):
            self.tiles.append([])
            for col in range(5):
                self.tiles[row].append(Tile((col *(TILESIZE +GAPSIZE)) + MARGIN_X, (row * (TILESIZE + GAPSIZE)) + MARGIN_Y))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.add_lettter()

    def add_lettter(self):
        for tile in self.tiles[self.current_row]:
            tile.letter = ""

        for i, letter in enumerate(self.text):
            self.tiles[self.current_row][i].letter = letter
            self.tiles[self.current_row][i].create_font()

    def draw_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen)

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.draw_tiles()
        pygame.display.flip()

    def row_anmation(self):
        self.not_enough_letters = True
        start_pos = self.tiles[0][0].x
        amount_move = 4
        move = 3
        screen_copy = self.screen.copy()
        screen_copy.fill(BGCOLOUR)
        for row in self.tiles:
            for tile in row:
                if row != self.tiles[self.current_row]:
                    tile.draw(screen_copy)

        while True:
            while self.tiles[self.current_row][0].x < start_pos + amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for tile in self.tiles[self.current_row]:
                    tile.x += move
                    tile.draw(self.screen)
                self.clock.tick(FPS)
                pygame.display.flip()

            while self.tiles[self.current_row][0].x > start_pos - amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for tile in self.tiles[self.current_row]:
                    tile.x -= move
                    tile.draw(self.screen)
                self.clock.tick(FPS)
                pygame.display.flip()

            amount_move -= 2
            if amount_move < 0:
                break


    def box_animation(self):
        for tile in self.tiles[self.current_row]:
            if tile.letter == "":
                screen_copy = self.screen.copy()
                for start, end,step in ((0, 6, 1), (0, -6, -1)):
                    for size in range(start, end, 2 * step):
                        self.screen.blit(screen_copy, (0, 0))
                        tile.x -= size
                        tile.y -= size
                        tile.width += size * 2
                        tile.height += size * 2
                        surface = pygame.Surface((tile.width, tile.height))
                        surface.fill(BGCOLOUR)
                        self.screen.blit(surface, (tile.x, tile.y))
                        tile.draw(self.screen)
                        pygame.display.flip()
                        self.clock.tick(FPS)
                    self.add_lettter()
                break

    def reveal_animation(self, tile, colour):
        screen_copy = self.screen.copy()

        while True:
            surface = pygame.Surface((tile.width + 5, tile.height + 5))
            surface.fill(BGCOLOUR)
            screen_copy.blit(surface, (tile.x ,tile.y))
            self.screen.blit(screen_copy, (0, 0))
            if self.flip:
                tile.y += 6
                tile.height -= 12
                tile.font_y += 4
                tile.font_height = max(tile.font_height - 8, 0)
            else:
                tile.colour = colour
                tile.y -= 6
                tile.height += 12
                tile.font_y -= 4
                tile.font_height = min(tile.font_height + 8, tile.font_size)
            if tile.font_height ==0:
                self.flip = False

            tile.draw(self.screen)
            pygame. display.update()
            self.clock.tick(FPS)

            if tile.font_height == tile.font_size:
                self.flip = True
                break
    

    def check_letters(self):
        copy_word = [x for x in self.word]
        for i, user_letter in enumerate(self.text):
            colour = red
            for j, letter in enumerate(copy_word):
                if user_letter == letter:
                    colour = yellow
                    if i == j:
                        colour = blue
                        copy_word[j] = "" 
                        break
            #  animation
            self.reveal_animation(self.tiles[self.current_row][i], colour)


    


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(self.text) == 5:
                        #check letters
                        self.check_letters()
                        if self.text == self.word or self.current_row + 1 == 6:
                            # Player lose
                            if self.text != self.word:
                                self.end_screen_text = UIElement(223, 590, f"THE WORD WAS: {self.word}", white)
                            
                            else:
                                #player win
                                self.end_screen_text = UIElement(223, 590, "CORRECT", green)
                            #restart game
                            self.playing = False
                            self.end_screen()
                            break
                        self.current_row +=1
                        self.text = ""
                    else:
                        # row animation, not enough letters message
                        self.row_anmation()

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 5 and event.unicode.isalpha():
                        self.text += event.unicode.upper()
                        self.box_animation()
    
    def end_screen(self):
        play_again = UIElement(223, 610, "PRESS ENTER TO PLAY AGAIN", white, 15)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.screen.fill(BGCOLOUR)
            self.draw_tiles()
            self.end_screen_text.fade_in()
            self.end_screen_text.draw(self.screen)
            play_again.fade_in()
            play_again.draw(self.screen)
            pygame.display.flip()


game = Game()
while True:
    game.new()
    game.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#Anjolaoluwa Obaduyi