class Settings:
    """储存所有设置类 """

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (203, 230, 230)

        # 飞船的设置
        # self.ship_speed_factor = .8
        self.ship_limit = 3

        # 子弹设置
        # self.bullet_speed = 1.5
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        # set limits to the quantities of bullets
        self.bullets_allowed = 5

        # alien settings
        # self.alien_move_right_or_left = .3
        self.drop_speed = 100
        # self.direction = 1

        # 加速设置
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = .8
        self.bullet_speed = 3
        self.alien_move_right_or_left = .3
        self.direction = 1
        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置和外星人点数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_move_right_or_left *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)


