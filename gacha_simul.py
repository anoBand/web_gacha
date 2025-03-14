import random

# 전역 변수 선언
guaranteed_4star_pickup = False
guaranteed_5star_pickup = False
four_star_count = 0
five_star_count = 0

items = {
    "3성": {
        "확률": 93.2,
        "목록": ["3성 직검", "3성 대검", "3성 총", "3성 건틀렛", "3성 증폭기"]
    },
    "4성": {
        "확률": 6.0,
        "픽업": ["설지", "산화", "유호"],
        "목록": ["4성 직검", "4성 대검", "4성 총", "4성 건틀렛", "4성 증폭기"]
    },
    "5성": {
        "확률": 0.8,
        "픽업": ["카를로타"],
        "목록": ["능양"]
    }
}
items["4성"]["목록"].append(items["4성"]["픽업"])
items["5성"]["목록"].append(items["5성"]["픽업"])

def select_josa(word, josa_type): ##가끔씩 word[-1]을 word로 인식하는 오류 있음. 확인할 것!
    """단어에 맞는 한국어 조사를 선택 (을/를)"""
    if josa_type == "을/를":
        last_char = word[-1]
#        print(last_char)
        if ord(last_char) - 44032 >= 0:  # 한글인지 확인
            jongseong = (ord(last_char) - 44032) % 28
            return "을" if jongseong else "를"
        return "를"  # 기본값
    return ""

def gacha_simulator():
    print("가챠 시뮬레이터를 시작합니다. 실행하시겠습니까? (Y/N)")
    total_pulls = 0  # 누적 뽑기 횟수

    while True:
        user_input = input("입력: ").strip().upper()
        if user_input == 'Y':
            while True:
                print("10회 뽑기를 시작합니다!")
                total_pulls += run_gacha()  # 가챠 실행 및 횟수 누적
                print(f"현재까지 총 {total_pulls}회 뽑았습니다.")

                # 다시 시행 여부
                retry = input("다시 뽑기를 시행하시겠습니까? (Y/N): ").strip().upper()
                if retry != 'Y':  # N 또는 기타 입력 시 종료
                    print("가챠 시뮬레이터를 종료합니다.")
                    return  # 루프 종료
        elif user_input == 'N':
            print("종료합니다.")
            return  # 프로그램 종료
        else:
            print("올바르지 않은 값 입력, 다시 입력하세요.")

def run_gacha():
    global guaranteed_4star_pickup, guaranteed_5star_pickup
    global four_star_count, five_star_count
    global items

    pulls = 0
    for _ in range(10):
        pulls += 1
        five_star_count+=1
        four_star_count+=1
        roll = random.uniform(0, 100)
#        print(f"roll={roll}")
        cumulative_probability = 0

        for rarity, data in items.items():
            selected_item=None

            cumulative_probability += data["확률"]
            if roll <= cumulative_probability:

                if five_star_count == 80:
                    data=items["5성"]
                    print("\n\t★★★ ",end='')
                    five_star_count=0
                    if guaranteed_5star_pickup:
                        #이전에 픽업이 안나왔을때
                        selected_item = random.choice(data["픽업"])
                        guaranteed_5star_pickup = False
                        josa = select_josa(selected_item, "을/를")
                        print(f"축하합니다! {selected_item}{josa} 획득하셨습니다! (5성 & 픽업 천장)")
                    else:
                        #이전에 픽업이 나왔을때
                        selected_item = random.choice(data["목록"])
                        if selected_item not in data["픽업"]:
                            guaranteed_5star_pickup = True
                        josa = select_josa(selected_item, "을/를")
                        print(f"축하합니다! {selected_item}{josa} 획득하셨습니다! (5성 천장)")
                    if four_star_count == 10:
                    #4성과 겹친다면 하나 미룸
                        four_star_count-=1
                    break

                if rarity == "5성":
                    data=items["5성"]
                    print("\n\t★★★ ",end='')
                    five_star_count=0
                    if guaranteed_5star_pickup:
                        selected_item = random.choice(data["픽업"])
                        guaranteed_5star_pickup = False
                        josa = select_josa(selected_item, "을/를")
                        print(f"축하합니다! {selected_item}{josa} 획득하셨습니다! (픽업 천장)")
                        break
                    else:
                        selected_item = random.choice(data["목록"])
                        if selected_item not in data["픽업"]:
                            guaranteed_5star_pickup = True
                    if four_star_count == 10:
                        #4성과 겹친다면 하나 미룸
                        four_star_count-=1

                if four_star_count == 10:
                    data=items["4성"]
                    print("\t★ ",end='')
                    four_star_count=0
                    if guaranteed_4star_pickup:
                        #이전에 픽업이 안나왔을때
                        selected_item = random.choice(data["픽업"])
                        guaranteed_4star_pickup = False
                        josa = select_josa(selected_item, "을/를")
                        print(f"축하합니다! {selected_item}{josa} 획득하셨습니다! (4성 & 픽업 천장)")
                    else:
                        #이전에 픽업이 나왔을때
                        selected_item = random.choice(data["목록"])
                        if selected_item not in data["픽업"]:
                            #픽업 아이템이 아니면 다음은 픽업
                            guaranteed_4star_pickup = True
                        josa = select_josa(selected_item, "을/를")
                        print(f"축하합니다! {selected_item}{josa} 획득하셨습니다! (4성 천장)")
                    break

                if rarity == "4성":
                    data=items["4성"]
                    print("\t★ ",end='')
                    four_star_count=0
                    if guaranteed_4star_pickup:
                        selected_item = random.choice(data["픽업"])
                        guaranteed_4star_pickup = False
                        josa = select_josa(selected_item, "을/를")
                        print(f"축하합니다! {selected_item}{josa} 획득하셨습니다! (픽업 천장)")
                        break
                    else:
                        selected_item = random.choice(data["목록"])
                        if selected_item not in data["픽업"]:
                            guaranteed_4star_pickup = True
                else:
                    selected_item = random.choice(data["목록"])
                
                josa = select_josa(selected_item, "을/를")
                print(f"축하합니다! {selected_item}{josa} 획득하셨습니다!")
                break
                
    return pulls

# 프로그램 실행
gacha_simulator()
