class GameStats:
    """track the statistics information of the game"""

    def __init__(self, ai_settings):
        """init the statistics information"""
        self.active = False
        self.ai_settings = ai_settings
        self.reset_stats()
        # 在任何情况下都不应该重置最高分
        self.get_highest_score('high_score.txt')
        self.level = 1

    def reset_stats(self):
        """"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_highest_score(self, file_name):
        with open(file_name, 'r+') as file_object:
            try:
                self.high_score = int(file_object.read())
            except TypeError:
                self.high_score = 0
