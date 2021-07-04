import sys
from bullet import Bullet
import pygame
from alien import Alien
from time import sleep


def check_keydown_events(event, stats, ai_settings, screen, ship, bullets):
    """响应按下按键"""
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        stats.active = False
    elif event.key == pygame.K_RIGHT:
        # 飞船向右移动标志
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets, stats)


def fire_bullets(ai_settings, screen, ship, bullets, stats):
    """ add a bullet to bullets group if the restrict numbers of bullets is lower than the allowed quantities"""
    if stats.active:
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            # create a bullet into the bullets group
            bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """响应松开按键"""
    if event.key == pygame.K_RIGHT:
        # 飞船向右移动标志
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """单击Play按钮开始游戏"""
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not stats.active:
        # reset game
        ai_settings.initialize_dynamic_settings()
        # hide the cursor
        pygame.mouse.set_visible(False)
        # reset stats information of game
        stats.reset_stats()
        stats.active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.show_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创造新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """相应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, stats, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查外星人和子弹的碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points * len(alien)
            sb.prep_score()
        check_high_score(stats, sb)

    # 检查是否外星人都被消灭，则更新外星人
    if len(aliens) == 0:
        # 如果外星人整体被消灭等级提高
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹位置"""
    # remove the disappeared bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
            # print(len(bullets))
    bullets.update()
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    numbers = available_space_y // (2 * alien_height)
    return numbers


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """create aliens group"""
    # calculate how many aliens a row can contain
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_numbers = (ai_settings.screen_width // alien_width - 1) // 2

    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # place each alien at (i,j) position
    for row_number in range(number_rows):
        for alien_number in range(alien_numbers):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """measures when collide with the edges"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """change direction of aliens"""
    # drop down after each changes of direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.drop_speed
    ai_settings.direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """response to ship hit"""
    if stats.ship_left > 0:
        stats.ship_left -= 1

        # 更新记分牌
        sb.prep_ships()
        # empty bullets and aliens
        aliens.empty()
        bullets.empty()
        # create a fleet of aliens, ship at the bottom
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.active = False
        pygame.mouse.set_visible(True)
        with open('high_score.txt', 'r+') as file_object:
            file_score = int(file_object.read())
            if stats.high_score > file_score:
                file_object.write(str(stats.high_score))



def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """check if the aliens drop on the bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # check collisions between aliens and ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # check if there is any alien dropping on the bottom
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """检查是否出现最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环都重   新绘制屏幕
    # 设置背景色
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    # 对分组调用draw，自动根据位置绘制，但必须是图形
    aliens.draw(screen)
    # for alien in aliens.sprites():
    #     alien.blitme()
    # bullets.draw(screen) 报错
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 显示得分
    sb.show_score()
    if not stats.active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()
