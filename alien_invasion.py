from pygame.sprite import Group
import pygame
from game_stats import GameStats
from settings import Settings
import game_function as gf
from ship import Ship
from button import Button
from scoreboard import ScoreBoard


def run_games():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # create button
    play_button = Button(ai_settings, screen, "Play")
    # save information, 并创建记分牌
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)

    # 创建飞船
    ship = Ship(ai_settings, screen)

    # create a bullet group
    bullets = Group()

    # create alien group
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.active:
            # 绘制飞船确保它出现在绘制背景后面
            ship.update()
            # bullets.update()
            # draw all bullets after the draw of ship
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # draw alien, 对编组调用draw会自动绘制元素
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button)


run_games()
