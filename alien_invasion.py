import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien





class AlienInvasion:
    #initialize the game, and create game resources
    def __init__(self) -> None :
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption('Alien Invasion')

        #create an instance to store game statistics
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        #set background cover
        self.bg_color = (230, 230, 230)
        self._create_fleet()

        #Make the button play
        self.play_button = Button(self, 'Play')

    def _create_fleet(self):
        #create an alien and find number of aliens in a row
        #spacing between each alien is equal to one alien width

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = int(available_space_x // (2*alien_width))
        #Determine the number of rows of aliens that fit on the screen

        ship_height = self.ship.rect.height

        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)






        #create full fleet of aliens.
        for row_number in range(number_rows):

         for alien_number in range (number_aliens_x) :
            self._create_alien(alien_number, row_number)



    def _create_alien(self, alien_number, row_number) :
            #create an alien and place it in the row.
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size

            alien_width = alien.rect.width
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien_height * row_number
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        #respond appropriately if any aliens have reached an edge\
         for alien in self.aliens.sprites() :
             if alien.check_edges() :
                 self._change_fleet_direction ()
                 break

    def _change_fleet_direction(self):
       #Drep the entire fleet and change the fleet's direction.
        for alien in self.aliens.sprites() :
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        #update position of bullets and get rid of old bullets
        #update bullet position 
        self.bullets.update()
        # Get rid of bullets which have expired
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions ()

    def _check_bullet_alien_collisions(self):
        #Responds to bullet aliens collions
        #Remove any bullets and aliens that have collided

                #check if any bullet has hit any alien
                #if so, get rid of the bullet and alien
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
            if collisions :
                for aliens in collisions.values():
                 self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()


            if not self.aliens:
                # Destroy existing bullets and create a new fleet
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()

                #increase level
                self.stats.level += 1
                self.sb.prep_level()

    def run_game(self):
        #start the main loop for the game
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens ()



            self._update_screen()

    def _check_events(self):
        #Respond to key presses and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)


            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button (mouse_pos)

    def _check_play_button(self, mouse_pos):
        #Starts a new game when the player clicks play.
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset the game settings
            self.settings.initialize_dynamic_settings()

            #reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #get rid of anything remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet
            self._create_fleet()
            self.ship.center_ship()
            #hide the mouse cursor
            pygame.mouse.set_visible(False)







    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullets(self):
        # Create a new bullet and add it to the b
        # Bullet groups
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _update_aliens (self):
        #check if the fleet is at the edge
        #updates the position of all aliens in the fleet
         self._check_fleet_edges()
         self.aliens.update()
        #look for alien ship collision
         if pygame.sprite.spritecollideany(self.ship, self.aliens):
             self._ship_hit ()
            #look for aliens hitting the bottom of the screen.
             self._check_aliens_bottom ()

    def _ship_hit (self):
          #respond to the ship being hit by alien.
         if self.stats.ships_left > 0:
          #decrement ships left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
         #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

        #create new fleet
            self._create_fleet()
            self.ship.center_ship()
         #Pause
            sleep(0.5)
         else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        #check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as ship got hit
                self._ship_hit ()
                break




    def _update_screen(self):
        #Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

            #Draw the score information
        self.sb.draw_score()

         #Draw the play button if the game is in active
        if not self.stats.game_active:
                self.play_button.draw_button()

        pygame.display.flip()



if __name__ == '__main__':
    a1 = AlienInvasion()
    a1.run_game()
