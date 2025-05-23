from pathlib import Path

class Settings:
    
    def __init__(self):
        """seetings that stay constant throughout entire game"""
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Background-4.png'
        self.difficulty_scale = 1.1
        self.score_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship3.png'
        self.ship_w = 40
        self.ship_h = 60

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'bullet_5.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'bullet_2_sound.mp3'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'monster_death_sound.mp3'



        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'sotrak_enemy.png'
        self.alien_w = 40
        self.alien_h = 40
        self.fleet_direction = 1

        self.button_w = 200 
        self.button_h = 50
        self.button_color = (0,135,50)

        self.text_color = (255,255,255)
        self.button_font_size = 48 
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'fonts' / 'Silkscreen' / 'stocky.ttf'

    
    def initalize_dynamic_settings(self):
        """settings that change as game progresses"""
        self.ship_speed = 5
        self.starting_ship_count = 3

        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_speed = 7
        self.bullet_amount = 5

        self.fleet_speed = 2
        self.fleet_drop_speed = 40
        self.alien_points = 50 

    def increase_difficulty(self):
        """increases our difficulty"""
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale





