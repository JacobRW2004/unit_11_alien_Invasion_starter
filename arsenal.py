import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
class Arsenal:
    def __init__(self, game: "AlienInvasion"):
        """initalize everything in arsenal"""
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        """calls removes bullets that go off screen and update our aresenal"""
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """remove bullet that goes offscreen"""
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)


    def draw(self):
        """draws our bullet"""
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self):
        """fires our bullet"""
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False
       
