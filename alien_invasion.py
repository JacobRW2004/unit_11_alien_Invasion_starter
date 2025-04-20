import sys
import random
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
#from alien import Alien
from alien_fleet import AlienFleet
from time import sleep
from button import Button
from hud import HUD

class AlienInvasion:
    """Our main class AlienInvasion"""
   
    def __init__(self) -> None:
        """initalizes everything for our AlienInvasion"""
        pygame.init()
        self.settings = Settings()
        self.settings.initalize_dynamic_settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w,self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
            (self.settings.screen_w, self.settings.screen_h)
            )

        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(1)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()
        self.play_button = Button(self, 'Play')
        self.game_active = False  

    def run_game(self):
        """runs the game, also checks for collisions, updates the screen and fleet etc."""
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        """checks for collisions, has certain ourpurs for events like destroying a ship"""
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()

        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()
        
        
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(700)
            self.game_stats.update(collisions)
            self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self.level_pick()
     
            self.settings.increase_difficulty()
            self.game_stats.update_level()
            self.HUD.update_level()

    def level_pick(self):
        """gets us our level we will be playing"""
        level_choice = self.get_level() 
        if level_choice == 1:
            self._reset_level()
        elif level_choice == 2:
            self._reset_level_2()

    def get_level(self):
        """gets a number 1 or 2 which will decide what level we play"""
        level_choice = random.choice([1,2])
        return level_choice

    def _check_game_status(self):
        """checks the amount of lives we have after a death and will end game if lives are less than zero"""

        if self.game_stats.ship_left > 0:
            self.game_stats.ship_left -= 1
            self.level_pick()
            sleep(1)
        else:
            self.game_active = False

        print(self.game_stats.ship_left)
            

    def _reset_level(self):
        """resets the level and returns the og fleet"""
        #self._reset_level()
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def _reset_level_2(self):
        """resets level and returns the traingle fleet"""
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet_2()

    def restart_game(self):
        """restarts the entire game, so everything goes back to its original things"""
        self.settings.initalize_dynamic_settings()
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)
        


    def _update_screen(self):
        """draws all assets within our game"""
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()


        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self):
        """this checks the buttons that are clicked and has a corresponding event"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.QUIT()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        """checks if our play button is pressed and has its response"""
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()
    
    def _check_keyup_events(self, event):
        """if not pressing on left or right key we dont move"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    


    def _check_keydown_events(self, event):
        """gives actions when we press certain keys"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.QUIT()
            sys.exit()
            
    



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()