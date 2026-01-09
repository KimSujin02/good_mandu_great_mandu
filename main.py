import time
import random
import art
import datetime
import msvcrt

# DB 연동하기 전 랭킹 리스트
ranking = []

mode = 'e'

# 마지막에 다 보여주기!
user_info = {
    "name" : ""
    , "total_score" : 0
    , "step_1_score" : 0 # 재료 점수
    , "step_2_score" : 0 # 양념 점수
    , "step_3_score" : 0 # 다지기 점수
    , "step_4_score" : 0 # 찜기 점수
}

# 1단계 재료 리스트 (정답 리스트 총 50)
# best 점수 : 40
# good 점수 : 20 ~ 39
# not_good 점수 : 19점 이하
ingredient_list = [
    {"name": "돼지고기", "score": 10},
    {"name": "두부", "score": 10},
    {"name": "부추", "score": 10},
    {"name": "대파", "score": 5},
    {"name": "양배추", "score": 5},
    {"name": "양파", "score": 5},
    {"name": "당면", "score": 5},
    {"name": "쑥", "score": -5},
    {"name": "미나리", "score": -5},
    {"name": "마늘쫑", "score": -5},
    {"name": "베이컨", "score": -15},
    {"name": "소시지", "score": -15},
    {"name": "깻잎", "score": -15},
    {"name": "샐러리", "score": -15},
    {"name": "브로콜리", "score": -15}
]

# 2단계 양념 재료 리스트 (정답 리스트 총 40)
# best 점수 : 25
# good 점수 : 20 ~ 24
# not_good 점수 : 19점 이하
seasoning_list = [
    {"name": "다진마늘", "score": 5},
    {"name": "간장", "score": 5},
    {"name": "참기름", "score": 5},
    {"name": "후추", "score": 5},
    {"name": "소금", "score": 5},
    {"name": "설탕", "score": 5},
    {"name": "슬라이스치즈", "score": -5},
    {"name": "크림치즈", "score": -5},
    {"name": "버터", "score": -5},
    {"name": "마요네즈", "score": -5},
    {"name": "라면스프", "score": -5},
    {"name": "떡볶이", "score": -5},
    {"name": "식빵", "score": -5},
    {"name": "사과", "score": -5}
]

judge_list = [
    "만두 장인 [백두산]",
    "전통요리연구가 [명지광]",
    "미각명인 [좌청룡]",
    "만두대법관 [엄덕구]",
    "찜기의 수호자 [탁귀핑]",
    "속재료 감정관 [왕대협]",
    "국물의 신 [사마귀]",
    "만두왕국 대심사관 [팔광구]"
]

# 키보드로 다지기 점수
# best : 200자
# 	점수 : 100
# good : 150자 ~ 199자
# 	점수 : 50
# not_good : 149자 이하
# 	점수 : 10

# 게임 끝나면 user_list 초기화 하는 메서드
def game_done() :
    global user_info
    ranking.append({"name" : user_info['name'], 'total_score' : user_info['total_score']})
    user_info = {
        "name" : ""
        , "total_score" : 0
        , "step_1_score" : 0 # 재료 점수
        , "step_2_score" : 0 # 양념 점수
        , "step_3_score" : 0 # 다지기 점수
        , "step_4_score" : 0 # 찜기 점수
    }

# 게임 끝나면 랭킹 리스트 정렬해서 보여줌!
def show_ranking() :
    print("""
          🥟🥟🥟🥟🥟 만 두 게 임 랭 킹 🥟🥟🥟🥟🥟
          """)
    ranking.sort(key=lambda x: x["total_score"], reverse=True)
    for i, user in enumerate(ranking[:5]):
        print(f"{i+1}등 : {user['name']} ({user['total_score']}점)")
    
    input("다시 시작하려면 엔터를 눌러주세요!")
    game_start()

# 최종 점수 구하기!
def get_total_score() :
    user_info['total_score'] += user_info['step_1_score']
    user_info['total_score'] += user_info['step_2_score']
    user_info['total_score'] += user_info['step_3_score']
    user_info['total_score'] += user_info['step_4_score']

def get_judge_thresholds(mode: str):
    if mode == 'e':
        return 120, 80   # best, good
    else:  # 'h'
        return 150, 110

def judge_mandu():
    get_total_score()
    time.sleep(1)

    best, good = get_judge_thresholds(mode)

    print(art.judge_face1)
    print(art.judge_msg_box.format(f'안녕하세요 심사위원 {random.choice(judge_list)}입니다.'))
    time.sleep(1)
    print(art.judge_msg_box.format('흠.. 오호.. 그렇구나...'))
    time.sleep(1)
    print(art.judge_msg_box.format(f"총 점수는 {user_info['total_score']}입니다."))

    if user_info['total_score'] >= best:
        print(art.judge_face4)
        print(art.judge_msg_box.format('?!'))
        time.sleep(1)
        print(art.judge_msg_box.format('우오오!!!'))
        time.sleep(1)
        print(art.judge_msg_box.format('너무 맛있습니다!!!❤️❤️❤️❤️❤️❤️❤️❤️❤️'))
    elif good <= user_info['total_score'] < best:
        print(art.judge_face2)
        print(art.judge_msg_box.format('음… 나쁘진 않은데요.'))
    else:
        print(art.judge_face3)
        print(art.judge_msg_box.format("제 인생 최악의 만두입니다. 으어어어어얽."))
    time.sleep(2)


def choice_step(step_num) :
    print(f'{step_num}단계!\n재료를 5가지 선택해주세요!🥗')
    
    if step_num == 1 : 
        choice_list = ingredient_list
    else :
        choice_list = seasoning_list
    random.shuffle(choice_list)
    
    for idx, obj in enumerate(choice_list) :
        if idx % 5 == 0 :
            print()
        print(f'[{obj['name']}]', end='  ')
    print()
    choice_score = 0
    selected_list = []
    
    choice_names = [item["name"] for item in choice_list]
    for n in range(0, 5) :
        print()
        while True:
            temp = str(input(f'{n+1}번째 재료를 입력해주세요! : '))
            if temp in selected_list :
                print('이미 선택한 재료입니다! 다시 입력해주세요.')
                print(f'현재 선택한 재료 리스트 : {selected_list}')
                continue
            elif not (temp in choice_names):
                print('재료 리스트에 존재하지 않는 값입니다!!')
                continue
            else :
                for item in choice_list:
                    if item["name"] == temp:
                        choice_score += item["score"]
                selected_list.append(temp)
                break
    time.sleep(1)
    print('⭐⭐⭐재료 선택이 완료 되었어요!⭐⭐⭐')
    time.sleep(1)
    print(selected_list)
    if step_num == 1 :
        user_info['step_1_score'] = choice_score
        ingredient_score_calc()
    else :
        user_info['step_2_score'] = choice_score
        seasoning_score_calc()
        
def ingredient_score_calc() :
    score = user_info['step_1_score']
    eval = ""
    print(f'재료 점수는 : {score}점 입니다!')
    # best 점수 : 40
    # good 점수 : 20 ~ 39
    # not_good 점수 : 19점 이하
    if score >=40 :
        eval = "최고!! 🥰🥰🥰"
    elif 20 <= score <= 39 :
        eval ="굿 😋"
    else :
        eval ='최악!!!!!!!!!! 🤮🤮🤮🤮🤮🤮'
    print(f'평가(최고/굿/최악) : {eval}')
    time.sleep(1)
        
def seasoning_score_calc() :
    score = user_info['step_2_score']
    eval = ""
    print(f'재료 점수는 : {score}점 입니다!')
    # best 점수 : 25
    # good 점수 : 20 ~ 24
    # not_good 점수 : 19점 이하
    if score >=25 :
        eval = "최고!! 🥰🥰🥰"
    elif 20 <= score <= 24 :
        eval ="굿 😋"
    else :
        eval ='최악!!!!!!!!!! 🤮🤮🤮🤮🤮🤮'
    print(f'평가(최고/굿/최악) : {eval}')
    time.sleep(1)

def chopping_step() :
    print('\n\n이제 선택한 재료들을 다져볼게요!')
    print('3초동안 키보드에서 아무 문자를 입력해서 재료를 다져주세요!')
    print("\n\n⚠⚠⚠ 영문 키보드 상태에서 입력하세요 ⚠⚠⚠")
    input('엔터를 누르면 시작됩니다!')
    
    count = 0
    start = time.time()
    limit = 3  # 3초

    print('\n다져주세요!!!')
    while time.time() - start < limit:
        if msvcrt.kbhit():          # 키가 눌렸는지 확인
            msvcrt.getch()          # 눌린 키 하나 가져오기
            count += 1
    print(f'총 {count}번 다지셨네요!')
    
    time.sleep(1.5)
    
    if count >= 80 :
        print('\n축하합니다!! 완벽하게 다져졌어요!🍴')
        user_info['step_3_score'] += 100
    elif 50 <= count <= 79 :
        print('\n보통정도로 다져졌네요.🍴')
        user_info['step_3_score'] += 50
    else :
        print('\n흠... 재료가 다 안 다져진거 같은데요.. 🤔')
        user_info['step_3_score'] -= 10
    
    time.sleep(1)
    
    

def ready_to_steam() :
    print(art.ready_to_steam)
    input("이제 만두를 완성하러 가볼까요?😋😋😋 (엔터를 눌러주세요!)")
    
def steamer() :
    messages = art.messages

    for msg in messages:
        print(msg)
        time.sleep(0.5)
    
    steamer_score = random.randint(-20, 100)
    if steamer_score < 0 :
        print(f'으악 만두를 찌다가 문제가 생겼어요.. 😭 : {steamer_score}점')
    else :
        print(f'찜이 잘 돼서 보너스 포인트를 받았어요! 🥰 : +{steamer_score}점')
    user_info['step_4_score'] += steamer_score
    time.sleep(1)
    input('만두 완성!! 이제 심사위원한테 평가를 받아볼게요.')

def mode_select() :
    # 게임 시작하면 먼저 user name 받기
    user_info['name'] = str(input('안녕하세요! 만두게임 도전자 이름을 입력해주세요! :'))
    global mode
    
    while True :
        print('모드를 선택해주세요! 이지모드는 e, 하드모드는 h를 입력해주세요!')
        mode = str(input('입력 (e/h) :')).lower()
        if mode in (['e', 'h']) :
            break
    

def game_start() :
    # 모드 선택
    mode_select()
    # 1단계
    choice_step(1)
    # 하드모드인 경우 2단계까지
    if mode == 'h' :
        choice_step(2)
    # 다지기
    chopping_step()
    ready_to_steam()
    # 찌기
    steamer()
    judge_mandu()
    game_done()
    show_ranking()
    
game_start()