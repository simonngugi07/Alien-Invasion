import pygame
from pygame.sprite import Sprite
class Ship(Sprite):

    def __init__(self,a1_game):
        #initialize the ship and set its starting position
        super().__init__()
        self.screen = a1_game.screen
        self.settings = a1_game.settings
        self.screen_rect = a1_game.screen.get_rect()

        #load the ship image and get its react.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        #store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
        #movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #update the ships position based on the movement of the flag
        #update the ship's x value, not the rect.
         if self.moving_right and self.rect.right < self.screen_rect.right:
             self.x +=self.settings.ship_speed

         if self.moving_left and self.rect.left > 0:
             self.x -=self.settings.ship_speed
        #update rect object from self.x.
         self.rect.x = self.x

    def center_ship(self):
        #Center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        #Draw the ship at its current location
        self.screen.blit(self.image,self.rect)