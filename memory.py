import pygame
from math import prod
from random import shuffle
from numpy import array, append


class Card():
    """Class for the card objects
    """
    global cards_size

    def __init__(self,pos,number):
        """Initialize the card by giving its position inside the screen and the
        number that appears when it is turned.

        Args:
            pos (list): x and y position of the top left of the card
            number (int): number that is displayed when the card is turned
        """
        self.pos = pos
        self.color = (255,255,255)
        self.border_color = (255,0,0)
        self.border_width = 3
        self.margin = 2
        self.number = number
        self.font = pygame.font.SysFont('ubuntu',70)
        self.text = self.font.render(str(self.number), True, self.border_color)
        self.text_center_x = int(self.pos[0]+cards_size[0]/2)
        self.text_center_y = int(self.pos[1]+cards_size[1]/2)
        self.text_rect = self.text.get_rect(center=(self.text_center_x, 
                                                    self.text_center_y))

    def draw_card(self,surface):
        """Draw the card by using pygame commands. The card is a white 
        rectangle with a red border.

        Args:
            surface (pygame.Surface): window where the cards are displayed.
        """
        pygame.draw.rect(
            surface, self.border_color, 
            (self.pos[0]+self.margin, self.pos[1]+self.margin, \
                cards_size[0]-2*self.margin,\
                cards_size[1]-2*self.margin)
        )
        pygame.draw.rect(
            surface, self.color, 
            (self.pos[0]+self.margin+self.border_width, \
                self.pos[1]+self.margin+self.border_width, \
                cards_size[0]-2*self.margin-2*self.border_width, \
                cards_size[1]-2*self.margin-2*self.border_width)
        )

    def turn(self,screen):
        """Function that displays the number of the card, simulating that the
        card is turned around

        Args:
            screen (pygame.Surface): window where the cards are displayed.
        """
        screen.blit(self.text, self.text_rect)


def update_screen(img, screen, card_dict):
    """When a card is turned around or its couple is found, the pygame window 
    needs to be updated to represent the changes

    Args:
        img (pygame.Surface): background image
        screen (pygame.Surface): window where the cards and image are displayed
        card_dict (dict): dictionary of card objects with its identification
    """
    pygame.display.update()
    screen.blit(img, (0,0))
    for c in card_dict.values():
        c[0].draw_card(screen)


def create_cards_dictionary():
    """Function that creates a dictionary of the cards which are identified by
    its position and the number that appears on each card is also displayed

    Returns:
        dictionary: already mentioned dictionary of cards
    """
    global cards_number, cards_distribution, cards_size
    card_dict = {}; i = 0
    card_number = array(range(1,int(cards_number/2)+1))
    card_number = append(card_number,card_number)
    shuffle(card_number)
    for x in range(cards_distribution[0]):
        for y in range(cards_distribution[1]):
            pipe_id = str(cards_size[0]*x)+'_'+str(cards_size[1]*y)
            card_dict[pipe_id] = [
                Card([cards_size[0]*x,cards_size[1]*y],card_number[i]),
                card_number[i]
            ]
            i += 1
    return card_dict


def main_memory():
    """Main function for the classic memory game, where a series of the cards 
    are laid face down on a surface and one card is flipped face up over each
    turn. The object of the game is to turn over pairs of matching cards.
    """
    global cards_number, cards_distribution, cards_size
    # Dimensions
    picture_size = [1920,1280]
    screen_factor = 3
    screen_size = [int(x/screen_factor) for x in picture_size]
    cards_distribution = [6,3]
    cards_number = prod(cards_distribution)
    cards_size = [int(x/y) for x, y in zip(screen_size,cards_distribution)]

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    img = pygame.image.load('figures/6_WinningPicture.jpg')

    card_dict = create_cards_dictionary()
    
    while True:
        update_screen(img, screen, card_dict,False)
        e = pygame.event.wait()
        if e.type == pygame.MOUSEBUTTONDOWN:
            break
        if e.type == pygame.QUIT:
            quit()

    last_card_id = 0; game = True
    while game:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            quit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            x_card = int(mx/cards_size[0])*cards_size[0]
            y_card = int(my/cards_size[1])*cards_size[1]
            pipe_id = str(x_card)+'_'+str(y_card)
            if pipe_id in card_dict.keys():
                card_dict[pipe_id][0].turn(screen)
                if last_card_id != pipe_id and last_card_id != 0 and \
                    card_dict[pipe_id][1] == card_dict[last_card_id][1]:
                        card_dict.pop(pipe_id)
                        card_dict.pop(last_card_id)
                        last_card_id = 0
                        update_screen(img, screen, card_dict,True)
                else:
                    last_card_id = pipe_id
            update_screen(img, screen, card_dict,True)

        if len(card_dict) == 0:
            game = False


main_memory()