import pygame  # pygame module import
import sys  # sys module import
import math  # math module import
import random  # random module import
from pygame.locals import *  # pygame 상수 작성 생략

BLACK = (0, 0, 0)  # 색 정의(검은색)
SILVER = (192, 208, 224)  # 색 정의(은색)
RED = (255, 0, 0)  # 색 정의(빨간색)
CYAN = (0, 224, 255)  # 색 정의(하늘색)

# 이미지 로딩
img_galaxy = pygame.image.load("image_gl/mainimg.png")  # 배경 별 이미지 로딩 변수
# 플레이어 기체 이미지 로딩 리스트
img_sship = [
    pygame.image.load("image_gl/mainchar.png"),
    pygame.image.load("image_gl/mainchar.png"),
    pygame.image.load("image_gl/mainchar.png"),
    pygame.image.load("image_gl/water2.png"),
]
# 플레이어 탄환 이미지 로딩 변수
img_weapon = pygame.image.load("image_gl/water1.png")
# 실드 이미지 로딩 변수
img_shield = pygame.image.load("image_gl/shield.png")
# 적 탄환 및 기체 이미지 로딩 변수
img_enemy = [
    pygame.image.load("image_gl/enemy01.png"),
    pygame.image.load("image_gl/segyun1.png"),
    pygame.image.load("image_gl/segyun2.png"),
    pygame.image.load("image_gl/segyun3.png"),
    pygame.image.load("image_gl/segyun4.png"),
    pygame.image.load("image_gl/boss.png"),
    pygame.image.load("image_gl/boss_at.png"),
]
# 폭발 연출 이미지 로딩 리스트
img_explode = [
    None,
    pygame.image.load("image_gl/explosion1.png"),
    pygame.image.load("image_gl/explosion2.png"),
    pygame.image.load("image_gl/explosion3.png"),
    pygame.image.load("image_gl/explosion4.png"),
    pygame.image.load("image_gl/explosion5.png"),
]
# 타이틀 화면 이미지 로딩 리스트
img_title = [
    pygame.image.load("image_gl/name.png"),
    pygame.image.load("image_gl/name.png"),
]

# SE 로딩 변수
se_barrage = None  # 탄약 발사 시 사용할 SE 로딩 변수
se_damage = None  # 데미지를 받을 시 사용할 SE 로딩 변수
se_explosion = None  # 보스 폭발 시 사용할 SE 로딩 변수
se_shot = None  # 탄환 발사 시 사용할 SE 로딩 변수

idx = 0  # 인덱스 변수
tmr = 0  # 타이머 변수
score = 0  # 점수 변수
hisco = 10000  # 최고 점수 변수
new_record = False  # 최고 점수 갱신용 플래그 변수
bg_y = 0  # 배경 스크롤용 변수

ss_x = 0  # 플레이어 기체의 x 좌표
ss_y = 0  # 플레이어 기체의 y 좌표
ss_d = 0  # 플레이어 기체의 기울기 변수
ss_shield = 0  # 플레이어 기체의 실드랑 변수
ss_muteki = 0  # 플레이어 기체의 무적 상태 변수
key_spc = 0  # 스페이스 키를 눌렸을 때 사용하는 변수
key_z = 0  # z 키를 눌렀을 때 사용하는 변수

MISSILE_MAX = 200  # 플레이어가 발사한 최대 탄환 수 정의
msl_no = 0  # 탄환 발사에 사용할 리스트 인덱스 변수
msl_f = [False] * MISSILE_MAX  # 탄환을 발사 중인지 관리하는 플래그 리스트
msl_x = [0] * MISSILE_MAX  # 탄환의 x좌표 리스트
msl_y = [0] * MISSILE_MAX  # 탄환의 y좌표 리스트
msl_a = [0] * MISSILE_MAX  # 탄환이 날아가는 각도 리스트

ENEMY_MAX = 100  # 적 최대 수 정의
emy_no = 0  # 적 등장 시 사용할 리스트 인덱스 변수
emy_f = [False] * ENEMY_MAX  # 적 등장 여부 관리 플래그 리스트
emy_x = [0] * ENEMY_MAX  # 적의 x좌표 리스트
emy_y = [0] * ENEMY_MAX  # 적의 y좌표 리스트
emy_a = [0] * ENEMY_MAX  # 적의 비행 각도 리스트
emy_type = [0] * ENEMY_MAX  # 적의 종류 리스트
emy_speed = [0] * ENEMY_MAX  # 적의 속도 리스트
emy_shield = [0] * ENEMY_MAX  # 적의 실드 리스트
emy_count = [0] * ENEMY_MAX  # 적 움직임 등을 관리할 리스트

EMY_BULLET = 0  # 적의 탄환 번호를 관리할 상수
EMY_ZAKO = 1  # 적 일반 기체 번호를 관리할 상수
EMY_BOSS = 5  # 보스 기체 번호를 관리할 상수
LINE_T = -80  # 적이 나타나는(사라지는) 위쪽 좌표
LINE_B = 800  # 적이 나타나는(사라지는) 아래쪽 좌표
LINE_L = -80  # 적이 나타나는(사라지는) 왼쪽 좌표
LINE_R = 1040  # 적이 나타나는(사라지는) 오른쪽 좌표

EFFECT_MAX = 100  # 폭발 연출 최대 수 정의
eff_no = 0  # 폭발 연출 시 사용할 리스트 인덱스 변수
eff_p = [0] * EFFECT_MAX  # 폭발 연출 이미지 번호 리스트
eff_x = [0] * EFFECT_MAX  # 폭발 연출 x좌표 리스트
eff_y = [0] * EFFECT_MAX  # 폭발 연출 y좌표 리스트

# 두 점 사이 거리 계산 함수 (제곱한 값 반환 *루트 미 사용)
def get_dis(x1, y1, x2, y2):
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)


# 입체적인 문자 표시 함수
def draw_text(scrn, txt, x, y, siz, col):
    fnt = pygame.font.Font(None, siz)  # 폰트 객체 생성
    cr = int(col[0] / 2)  # 빨간색 성분에서 어두운 값 계산
    cg = int(col[1] / 2)  # 초록색 성분에서 어두운 값 계산
    cb = int(col[2] / 2)  # 파란색 성분에서 어두운 값 계싼
    sur = fnt.render(txt, True, (cr, cg, cb))  # 어두운 색 문자열을 그린 Surface 생성
    x = x - sur.get_width() / 2  # 중심선 표시 x좌표 계산
    y = y - sur.get_height() / 2  # 중심선 표시 y좌표 계산
    scrn.blit(sur, [x + 1, y + 1])  # 해당 surface를 화면에 전송
    cr = col[0] + 128  # 빨간색 성분에서 밝은 값 계산
    if cr > 255:
        cr = 255
    cg = col[1] + 128  # 초록색 성분에서 밝은 값 계산
    if cg > 255:
        cg = 255
    cb = col[2] + 128  # 파란색 성분에서 밝은 값 계산
    if cb > 255:
        cb = 255
    sur = fnt.render(txt, True, (cr, cg, cb))  # 밝은 색 문자열을 그린 surface 생성
    scrn.blit(sur, [x - 1, y - 1])  # 해당 surface를 화면에 전송
    sur = fnt.render(txt, True, col)  # 인수 색으로 문자열을 그린 surface 생성
    scrn.blit(sur, [x, y])  # 해당 surface를 화면에 전송


# 플레이어 기체 이동
def move_starship(scrn, key):
    # 전역변수 선언
    global idx, tmr, ss_x, ss_y, ss_d, ss_shield, ss_muteki, key_spc, key_z
    ss_d = 0  # 기체 기울기 변수에 0(기울지 않음) 대입
    if key[K_UP] == 1:  # 위쪽 방향 키를 눌렀다면
        ss_y = ss_y - 20  # Y 좌표 감소
        if ss_y < 80:  # Y 좌표가 80보다 크다면
            ss_y = 80  # Y 좌표에 80dmf 대입
    if key[K_DOWN] == 1:  # 아래쪽 방향 키를 눌렀다면
        ss_y = ss_y + 20  # Y 좌표 증가
        if ss_y > 640:  # Y 좌표가 640보다 크다면
            ss_y = 640  # Y 좌표에 640 대입
    if key[K_LEFT] == 1:  # 왼쪽 방향 키를 눌렀다면
        ss_d = 1  # 기체 기울기 변수에 1(왼쪽) 대입
        ss_x = ss_x - 20  # X 좌표 감소
        if ss_x < 40:  # X 좌표가 40보다 작다면
            ss_x = 40  # X 좌표에 40 대입
    if key[K_RIGHT] == 1:  # 오른쪽 방향 키를 눌렀다면
        ss_d = 2  # 기체 기울기 변수에 2(오른쪽) 대입
        ss_x = ss_x + 20  # X 좌표 증가
        if ss_x > 920:  # X 좌표가 920보다 크다면
            ss_x = 920  # X 좌표에 920 eodlq
    key_spc = (key_spc + 1) * key[K_SPACE]  # 스페이스 키를 누르는 동안 변수 값 증가
    if key_spc % 5 == 1:  # 스페이스 키를 처음 누른 후, 5프레임마다 탄환 발사
        set_missile(0)  # 탄환 발사
        se_shot.play()  # 발사음 출력
    key_z = (key_z + 1) * key[K_z]  # Z 키를 누른 동안 변수 값 증가
    if key_z == 1 and ss_shield > 10:  # 1번 눌렀을 때 실드량이 10보다 크다면
        set_missile(10)  # 탄막 치기
        ss_shield = ss_shield - 10  # 실드량 10 감소
        se_barrage.play()  # 발사음 출력

    if ss_muteki % 2 == 0:  # 무적 상태에서 깜빡이기 위한 if 구문
        scrn.blit(img_sship[3], [ss_x - 8, ss_y + 40 + (tmr % 3) * 2])  # 엔진 불꽃 그리기
        scrn.blit(img_sship[ss_d], [ss_x - 37, ss_y - 48])  # 플레이어 기체 그리기

    if ss_muteki > 0:  # 무적 상태라면
        ss_muteki = ss_muteki - 1  # ss_muteki 값 감소
        return  # 함수를 벗어남(적과 히트 체크 미 수행)
    elif idx == 1:  # 무적 상태가 아니고, idx 1이면
        for i in range(ENEMY_MAX):  # 반복(적 기체와 히트 체크 수행)
            # 적 기체가 존재한다면
            if emy_f[i] == True:
                w = img_enemy[emy_type[i]].get_width()  # 적 기체 이미지 폭
                h = img_enemy[emy_type[i]].get_height()  # 적 기체 이미지 높이
                r = int((w + h) / 4 + (74 + 96) / 4)  # 히트 체크 거리 계산
                # 적 기체와 플레이어 기체 사이의 거리가 히트 체크 거리보다 작으면
                if get_dis(emy_x[i], emy_y[i], ss_x, ss_y) < r * r:
                    set_effect(ss_x, ss_y)  # 폭발 연출 설정
                    ss_shield = ss_shield - 10  # 실드량 감소
                    if ss_shield <= 0:  # ss_shield 값이 0 이하이면
                        ss_shield = 0  # ss_shield 값에 0 대입
                        idx = 2  # 게임 오버로 이동
                        tmr = 0
                    if ss_muteki == 0:  # 무적 상태가 아니면
                        ss_muteki = 60  # 무적 상태로 설정
                        se_damage.play()  # 데미지 효과음 출력
                    if emy_type[i] < EMY_BOSS:  # 접촉한 기체가 보스가 아니면
                        emy_f[i] = False  # 적 기체 삭제


# 플레이어 기체에서 발사하는 탄환 설정 함수
def set_missile(typ):
    global msl_no  # 전역 변수 선언
    if typ == 0:  # 탄환(단발)인 경우
        msl_f[msl_no] = True  # 탄환 발사 플래그 True 설정
        msl_x[msl_no] = ss_x  # 탄환 x 좌표 대입(플레이어 기체 앞 끝)
        msl_y[msl_no] = ss_y - 50  # 탄환 y 좌표 대입
        msl_a[msl_no] = 270  # 탄환 발사 각도
        msl_no = (msl_no + 1) % MISSILE_MAX  # 다음 설정을 위한 번호 계산
    if typ == 10:  # 탄막인 경우
        for a in range(180, 540, 10):  # 반복해서 방사형으로 탄환 발사
            msl_f[msl_no] = True  # 탄환 발사 플래그 True 설정
            msl_x[msl_no] = ss_x  # 탄환 x 좌표 대입(기체 앞 끝)
            msl_y[msl_no] = ss_y - 50  # 탄환 y 좌표 대입
            msl_a[msl_no] = a  # 탄환 발사 각도
            msl_no = (msl_no + 1) % MISSILE_MAX  # 다음 설정을 위한 번호 계산


# 탄환 이동 함수
def move_missile(scrn):
    for i in range(MISSILE_MAX):  # 반복해서
        if msl_f[i] == True:  # 탄환이 발사된 상태라면
            msl_x[i] = msl_x[i] + 36 * math.cos(math.radians(msl_a[i]))  # x 좌표 계산
            msl_y[i] = msl_y[i] + 36 * math.sin(math.radians(msl_a[i]))  # y 좌표 계산
            img_rz = pygame.transform.rotozoom(
                img_weapon, 90 - msl_a[i], 1.0
            )  # 날아가는 각도의 회전 이미지 생성
            scrn.blit(
                img_rz,
                [msl_x[i] - img_rz.get_width() / 2, msl_y[i] - img_rz.get_height() / 2],
            )  # 탄환 이미지 그리기
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960:  # 탄환이 화면 밖으로 나가면
                msl_f[i] = False  # 탄환 삭제


# 적 기체 등장 함수
def bring_enemy():
    sec = tmr / 30  # 게임 진행 시간(초 단위)을 sec에 대입
    if 0 < sec and sec < 25:  # 0~25초
        if tmr % 15 == 0:  # 해당 타이밍에
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1)  # 적 1 등장
    if 30 < sec and sec < 55:  # 30~55초
        if tmr % 10 == 0:  # 해당 타이밍에
            set_enemy(
                random.randint(20, 940), LINE_T, 90, EMY_ZAKO + 1, 12, 1
            )  # 적 2 등장
    if 60 < sec and sec < 85:  # 60~85초
        if tmr % 15 == 0:  # 해당 타이밍에
            set_enemy(
                random.randint(100, 860),
                LINE_T,
                random.randint(60, 120),
                EMY_ZAKO + 2,
                6,
                3,
            )  # 적 3 등장
    if 90 < sec and sec < 115:  # 90~115초
        if tmr % 20 == 0:  # 해당 타이밍에
            set_enemy(
                random.randint(100, 860), LINE_T, 90, EMY_ZAKO + 3, 12, 2
            )  # 적 4 등장
    if 120 < sec and sec < 145:  # 120~145초, 2종류
        if tmr % 20 == 0:  # 해당 타이밍에
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1)  # 적 1 등장
            set_enemy(
                random.randint(100, 860),
                LINE_T,
                random.randint(60, 120),
                EMY_ZAKO + 2,
                6,
                3,
            )  # 적 3 등장
    if 150 < sec and sec < 175:  # 150~175초, 2종류
        if tmr % 20 == 0:  # 해당 타이밍에
            set_enemy(
                random.randint(20, 940), LINE_B, 270, EMY_ZAKO, 8, 1
            )  # 적 1 아래에서 위로 등장
            set_enemy(
                random.randint(20, 940),
                LINE_T,
                random.randint(70, 110),
                EMY_ZAKO + 1,
                12,
                1,
            )  # 적 2 등장
    if 180 < sec and sec < 205:  # 180~205초, 2종류
        if tmr % 20 == 0:  # 해당 타이밍에
            set_enemy(
                random.randint(100, 860),
                LINE_T,
                random.randint(60, 120),
                EMY_ZAKO + 2,
                6,
                3,
            )  # 적 3 등장
            set_enemy(
                random.randint(100, 860), LINE_T, 90, EMY_ZAKO + 3, 12, 2
            )  # 적 4 등장
    if 210 < sec and sec < 235:  # 210~235초, 2종류
        if tmr % 20 == 0:  # 해당 타이밍에
            set_enemy(LINE_L, random.randint(40, 680), 0, EMY_ZAKO, 12, 1)  # 적 1 등장
            set_enemy(
                LINE_R, random.randint(40, 680), 180, EMY_ZAKO + 1, 18, 1
            )  # 적 2 등장
    if 240 < sec and sec < 265:  # 240~265초, 총공격
        if tmr % 30 == 0:  # 해당 타이밍에
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1)  # 적 1 등장
            set_enemy(
                random.randint(20, 940), LINE_T, 90, EMY_ZAKO + 1, 12, 1
            )  # 적 2 등장
            set_enemy(
                random.randint(100, 860),
                LINE_T,
                random.randint(60, 120),
                EMY_ZAKO + 2,
                6,
                3,
            )  # 적 3 등장
            set_enemy(
                random.randint(100, 860), LINE_T, 90, EMY_ZAKO + 3, 12, 2
            )  # 적 4 등장

    # 보스 출현
    if tmr == 30 * 270:  # tmr 값이 조건에 맞는 경우
        set_enemy(480, -210, 90, EMY_BOSS, 4, 200)  # 보스 기체 등장


# 적 기체 설정
# 적 기체 리스트 좌표 및 각도 설정 함수
def set_enemy(x, y, a, ty, sp, sh):
    global emy_no  # 전역 변수 선언
    while True:  # 무한 반복
        if emy_f[emy_no] == False:  # 리스트가 비었다면
            emy_f[emy_no] = True  # 플래그 설정
            emy_x[emy_no] = x  # X 좌표 대입
            emy_y[emy_no] = y  # Y 좌표 대입
            emy_a[emy_no] = a  # 각도 대입
            emy_type[emy_no] = ty  # 적 종류 대입
            emy_speed[emy_no] = sp  # 적 속도 대입
            emy_shield[emy_no] = sh  # 적 실드량 개입
            emy_count[emy_no] = 0  # 움직임 등을 관리하는 리스트에 0 대입
            break  # 반복 이탈
        emy_no = (emy_no + 1) % ENEMY_MAX  # 다음 설정을 위한 번호 계산


# 적 기체 이동
# 적 기체 이동 함수
def move_enemy(scrn):
    global idx, tmr, score, hisco, new_record, ss_shield  # 전역 변수 설정
    for i in range(ENEMY_MAX):  # 반복
        if emy_f[i] == True:  # 적 기체가 존재한다면
            ang = -90 - emy_a[i]  # ang에 이미지 회전 각도 대입
            png = emy_type[i]  # png에 이미지 번호 대입
            # 적 일반 기체 이동
            if emy_type[i] < EMY_BOSS:  # 적 일반 기체라면
                emy_x[i] = emy_x[i] + emy_speed[i] * math.cos(
                    math.radians(emy_a[i])
                )  # X 좌표 변화
                emy_y[i] = emy_y[i] + emy_speed[i] * math.sin(
                    math.radians(emy_a[i])
                )  # Y 좌표 변화
                # 진행 방향을 변경하는 적
                if emy_type[i] == 4:  # 진행 방향을 변경하는 적이면
                    emy_count[i] = emy_count[i] + 1  # emy_count 증가
                    ang = emy_count[i] * 10  # 이미지 회전 각도 계산
                    if emy_y[i] > 240 and emy_a[i] == 90:  # Y 좌표가 240 보다 크다면
                        emy_a[i] = random.choice([50, 70, 110, 130])  # 무작위로 방향 변경
                        set_enemy(emy_x[i], emy_y[i], 90, EMY_BULLET, 6, 0)  # 탄환 발사
                if (
                    emy_x[i] < LINE_L
                    or LINE_R < emy_x[i]
                    or emy_y[i] < LINE_T
                    or LINE_B < emy_y[i]
                ):  # 화면 상하좌우에서 벗어났다면
                    emy_f[i] = False  # 적 기체 삭제
            # 보스 기체
            else:  # 그렇지 않다면(보스 기체라면)
                if emy_count[i] == 0:  # emy_count 값이 0이면
                    emy_y[i] = emy_y[i] + 2  # 아래쪽으로 내려 보냄
                    if emy_y[i] >= 200:  # 아래까지 내려왔다면
                        emy_count[i] = 1  # 왼쪽방향으로 이동
                elif emy_count[i] == 1:  # emy_count 값이 1이면
                    emy_x[i] = emy_x[i] - emy_speed[i]  # 왼쪽으로 이동
                    if emy_x[i] < 200:  # 왼쪽까지 왔다면
                        for j in range(0, 10):  # 반복
                            set_enemy(
                                emy_x[i], emy_y[i] + 80, j * 20, EMY_BULLET, 6, 0
                            )  # 탄환 발사
                        emy_count[i] = 2  # 오른쪽으로 이동
                else:  # emy_count가 0, 1이 아니면
                    emy_x[i] = emy_x[i] + emy_speed[i]  # 오른쪽으로 이동
                    if emy_x[i] > 760:  # 오른쪽으로 왔다면
                        for j in range(0, 10):  # 반복
                            set_enemy(
                                emy_x[i], emy_y[i] + 80, j * 20, EMY_BULLET, 6, 0
                            )  # 탄환 발사
                        emy_count[i] = 1  # 왼쪽으로 이동
                if emy_shield[i] < 100 and tmr % 30 == 0:  # 실드 값 100 미만시 해당 타이밍에
                    set_enemy(
                        emy_x[i],
                        emy_y[i] + 80,
                        random.randint(60, 120),
                        EMY_BULLET,
                        6,
                        0,
                    )  # 탄환 발사

            # 적 탄환 이외, 플레이어 기체 발사 탄환과 히트 체크
            if emy_type[i] != EMY_BULLET:
                w = img_enemy[emy_type[i]].get_width()  # 적 기체 이미지 폭(픽셀 수)
                h = img_enemy[emy_type[i]].get_height()  # 적 기체 이미지 높이(픽셀 수)
                r = int((w + h) / 4) + 12  # 히트 체크에 사용할 거리 계산
                er = int((w + h) / 4)  # 폭발 연출 표시 값 계산
                for n in range(MISSILE_MAX):  # 반복
                    # 플레이어 기체 탄환과 접촉 여부 판단
                    if (
                        msl_f[n] == True
                        and get_dis(emy_x[i], emy_y[i], msl_x[n], msl_y[n]) < r * r
                    ):
                        msl_f[n] = False  # 탄환 삭제
                        set_effect(
                            emy_x[i] + random.randint(-er, er),
                            emy_y[i] + random.randint(-er, er),
                        )  # 폭발 이펙트
                        # 보스 기체 깜빡임 처리
                        if emy_type[i] == EMY_BOSS:  # 보스 기체라면
                            png = emy_type[i] + 1  # 플래시용 이미지 번호
                        emy_shield[i] = emy_shield[i] - 1  # 적 기체 실드량 감소
                        score = score + 100  # 점수 증가
                        if score > hisco:  # 최고 점수를 넘었다면
                            hisco = score  # 최고 점수 갱신
                            new_record = True  # 최고 점수 플래그 설정
                        if emy_shield[i] == 0:  # 적 기체를 격추했다면
                            emy_f[i] = False  # 적 기체 삭제
                            if ss_shield < 100:  # 플레이어 실드량 100 미만이면
                                ss_shield = ss_shield + 1  # 실드량 증가
                            # 보스를 격추시키면 클리어
                            if emy_type[i] == EMY_BOSS and idx == 1:  # 보스를 쓰러뜨렸다면
                                idx = 3  # idx 3 대입
                                tmr = 0  # 게임 클리어로
                                for j in range(10):  # 반복해서
                                    set_effect(
                                        emy_x[i] + random.randint(-er, er),
                                        emy_y[i] + random.randint(-er, er),
                                    )  # 보스 폭발 연출
                                se_explosion.play()  # 폭발 효과음

            img_rz = pygame.transform.rotozoom(
                img_enemy[png], ang, 1.0
            )  # 적 기체를 회전시킨 이미지 생성
            scrn.blit(
                img_rz,
                [emy_x[i] - img_rz.get_width() / 2, emy_y[i] - img_rz.get_height() / 2],
            )  # 적 기체 이미지 그리기


# 폭발 연출 설정 함수
def set_effect(x, y):
    global eff_no  # 전역 변수 선언
    eff_p[eff_no] = 1  # 폭발 연출 이미지 번호 대입
    eff_x[eff_no] = x  # 폭발 연출 x 좌표 대입
    eff_y[eff_no] = y  # 폭발 연출 y 좌표 대입
    eff_no = (eff_no + 1) % EFFECT_MAX  # 다음 설정을 위한 번호 계산


# 폭발 연출 표시 함수
def draw_effect(scrn):
    for i in range(EFFECT_MAX):  # 반복
        if eff_p[i] > 0:  # 폭발 연출 중이면
            scrn.blit(img_explode[eff_p[i]], [eff_x[i] - 48, eff_y[i] - 48])  # 폭발 연출 표시
            eff_p[i] = eff_p[i] + 1  # eff_p 값 1 증가
            if eff_p[i] == 6:  # eff_p가 6이 되었다면
                eff_p[i] = 0  # eff_p에 0 대입 후 연출 종료


# 메인 처리 수행 함수
def main():
    # 전역 변수 선언
    global idx, tmr, score, new_record, bg_y, ss_x, ss_y, ss_d, ss_shield, ss_muteki
    global se_barrage, se_damage, se_explosion, se_shot

    pygame.init()  # pygame 모듈 초기화
    pygame.display.set_caption("Dentist Game")  # 윈도우 타이틀 지정
    screen = pygame.display.set_mode((960, 720))  # 그릴 화면(스크롤) 초기화
    clock = pygame.time.Clock()  # clock 객체 초기화
    se_barrage = pygame.mixer.Sound("sound_gl/barrage.ogg")  # SE 로딩
    se_damage = pygame.mixer.Sound("sound_gl/damage.ogg")  # SE 로딩
    se_explosion = pygame.mixer.Sound("sound_gl/explosion.ogg")  # SE 로딩
    se_shot = pygame.mixer.Sound("sound_gl/shot.ogg")  # SE 로딩

    while True:  # 무한 반복
        tmr = tmr + 1  # tmr 값 1 증가
        for event in pygame.event.get():  # pygame 이벤트 반복 처리
            if event.type == QUIT:  # 윈도우의 x 버튼을 누른 경우
                pygame.quit()  # pygame 모듈 초기화 해제
                sys.exit()  # 프로그램 종료
            if event.type == KEYDOWN:  # 키를 누르는 이벤트 발생시
                if event.key == K_F1:  # F1 키라면
                    screen = pygame.display.set_mode(
                        (960, 720), FULLSCREEN
                    )  # 풀 스크린 모드로 전환
                if event.key == K_F2 or event.key == K_ESCAPE:  # F2키 혹은 Esc 키라면
                    screen = pygame.display.set_mode((960, 720))  # 일반 화면 모드로 전환

        # 배경 스크롤
        # bg_y = (bg_y + 16) % 720  # 배경 스크롤 위치 계산
        screen.blit(img_galaxy, [0, bg_y - 720])  # 배경 그리기(위쪽)
        screen.blit(img_galaxy, [0, bg_y])  # 배경 그리기(아래쪽)

        key = pygame.key.get_pressed()  # key에 모든 키 상태 대입

        # 타이틀 화면
        if idx == 0:  # idx 0 처리(타이틀 화면)
            # img_rz = pygame.transform.rotozoom(
            #     img_title[0], -tmr % 360, 1.0
            # )  # 로고 뒤, 회전하는 소용돌이 이미지
            # screen.blit(
            #     img_rz, [480 - img_rz.get_width() / 2, 280 - img_rz.get_height() / 2]
            # )  # 이미지를 화면에 그리기
            screen.blit(img_title[1], [70, 160])  # 로고 그리기

            draw_text(screen, "Press [SPACE] to Start!", 480, 600, 50, SILVER)  # 문자 표시
            if key[K_SPACE] == 1:  # 스페이스 키를 눌렀다면
                idx = 1  # idx에 1 대입
                tmr = 0  # 타이머에 0 대입
                score = 0  # 점수에 0 대입
                new_record = False  # 최고 점수 갱신 플래그 False
                ss_x = 480  # 시작 시 플레이어 기체 X 좌표
                ss_y = 600  # 시작 시 플레이어 기체 Y 좌표
                ss_d = 0  # 플레이어 기체 기울기 0
                ss_shield = 100  # 실드량 100
                ss_muteki = 0  # 무적 상태 시간 0
                for i in range(ENEMY_MAX):  # 반복
                    emy_f[i] = False  # 적 기체 등장하지 않는 상태
                for i in range(MISSILE_MAX):  # 반복
                    msl_f[i] = False  # 플레이어 탄환 미발사 상태
                pygame.mixer.music.load("sound_gl/mainbgm.ogg")  # BGM 로딩
                pygame.mixer.music.play(-1)  # BGM 무한 반복 출력

        # 게임 플레이 중
        if idx == 1:  # idx 1 처리
            move_starship(screen, key)  # 플레이어 기체 이동
            move_missile(screen)  # 플레이어 탄환 이동
            bring_enemy()  # 적 기체 등장
            move_enemy(screen)  # 적 기체 이동

        # 게임 오버
        if idx == 2:  # idx 2 처리
            move_missile(screen)  # 플레이어 기체 탄환 이동
            move_enemy(screen)  # 적 기체 이동
            if tmr == 1:  # tmr 값이 1이면
                pygame.mixer.music.stop()  # BGM 정지
            if tmr <= 90:  # tmr 값이 90 이하이면
                if tmr % 5 == 0:  # tmr % 5의 값이 0이면
                    set_effect(
                        ss_x + random.randint(-60, 60), ss_y + random.randint(-60, 60)
                    )  # 플레이어 기체 폭발 연출
                if tmr % 10 == 0:  # tmr % 10의 값이 0이면
                    se_damage.play()
            if tmr == 120:  # tmr 값이 120이면
                pygame.mixer.music.load("sound_gl/gameover.ogg")  # BGM 로드
                pygame.mixer.music.play(0)  # BGM 플레이
            if tmr > 120:  # tmr 값이 120보다 크면
                draw_text(screen, "GAME OVER", 480, 300, 80, RED)  # 문자 표시
                if new_record == True:  # 최고 점수를 갱신했다면
                    draw_text(
                        screen, "NEW RECORD " + str(hisco), 480, 400, 60, CYAN
                    )  # 문자 표시
            if tmr == 400:  # tmr 값이 400이면
                idx = 0  # idx에 0 대입, 타이틀 화면으로
                tmr = 0  # tmr에 0 대입

        # 게임 클리어
        if idx == 3:  # idx 3 처리
            move_starship(screen, key)  # 플레이어 기체 이동
            move_missile(screen)  # 플레이어 탄환 이동
            if tmr == 1:  # tmr 값이 1이면
                pygame.mixer.music.stop()  # BGM 정지
            if tmr < 30 and tmr % 2 == 0:  # tmr 값이 30 미만, 1프레임마다
                pygame.draw.rect(
                    screen, (192, 0, 0), [0, 0, 960, 720]
                )  # 보스 폭발 연출, 화면 빨간색 칠함
            if tmr == 120:  # tmr 값이 120이면
                pygame.mixer.music.load("sound_gl/gameclear.ogg")  # 게임 클리어 BGM 로딩
                pygame.mixer.music.play(0)  # 게임 클리어 BGM 재싱
            if tmr > 120:  # tmr 값이 120보다 크면
                draw_text(screen, "GAME CLEAR", 480, 300, 80, SILVER)  # 문자 표시
                if new_record == True:  # 최고 점수를 갱신했다면
                    draw_text(
                        screen, "NEW RECORD " + str(hisco), 480, 400, 60, CYAN
                    )  # 문자 표시
            if tmr == 400:  # tmr 값이 400이면
                idx = 0  # idx에 0 대입, 타이틀 화면으로
                tmr = 0  # tmr에 0 대입

        draw_effect(screen)  # 폭발 연출
        draw_text(screen, "SCORE " + str(score), 200, 30, 50, SILVER)  # 점수 표시
        draw_text(screen, "HISCORE " + str(hisco), 760, 30, 50, CYAN)  # 최고 점수 표시

        # 실드 표시
        if idx != 0:  # idx 값이 0이 아니면(타이틀 화면 외)
            screen.blit(img_shield, [40, 680])  # 실드 이미지 그리기
            pygame.draw.rect(
                screen,
                (64, 32, 32),
                [40 + ss_shield * 4, 680, (100 - ss_shield) * 4, 12],
            )  # 실드가 줄어든 만큼 사각형 칠함

        pygame.display.update()  # 화면 업데이트
        clock.tick(30)  # 프레임 레이트 지정


# 프로그램 직접 실행시 main() 함수 호출
if __name__ == "__main__":
    main()
