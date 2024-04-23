import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
 
def black_out():  # 文字を画面上に出力する、black_outの機能はない
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",True, (255,255,255))
    screen.blit(txt, [650, 450])
    toumei : int = 128  #型ヒント
    return toumei

def check_bound(obj_rct:pg.rect):
    """
    こうかとんrect、または、爆弾rectの画面内外判定用の関数
    引数：こうかとんrect、爆弾rect
    戻り値：よこ、たて結果判定(画面うちTrue:画面外Flase)
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    font = pg.font.Font(None, 100)
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    gg_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)  # gameoverの画像
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):  # こうかとんが爆弾にぶつかると終了
            # 5秒を数える始める
            hani = pg.Rect(0,0,WIDTH,HEIGHT)
            pg.draw.rect(screen,(0,0,0), hani)  # ブラックアウトする
            toumei = black_out()
            bg_img.set_alpha(toumei)
            screen.blit(bg_img,[0, 0])  # 透明化した画像を出力
            screen.blit(gg_img,[600, 450])  # こうかとんを出力
            pg.display.flip()
            time.sleep(5)  #時間を5秒たつと終了させる
            return
            
        screen.blit(bg_img, [0, 0]) 
        #こうかとんの移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
               sum_mv[0] += v[0]
               sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        # こうかとんのはみだし反射
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 爆弾の移動と表示
        bd_rct.move_ip(vx, vy)       
        screen.blit(bd_img, bd_rct)
        # 爆弾のはみだし反射
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx = -vx
        if not tate:
            vy = -vy

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()