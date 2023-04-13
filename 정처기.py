import pandas as pd
import random  # 랜덤한 문제를 선택하기 위해 random 모듈을 import합니다.
import time

# 데이터셋 로딩
df = pd.read_csv('./정처기 실기 문제ver1.5.csv')

# 온점(`.`)을 기준으로 문자열을 나누고, 줄바꿈 문자를 추가하여 새로운 정제된문제 컬럼 만드는 함수
def wrap_text(text):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) <= 50:
            current_line += " " + word
        else:
        
            lines.append(current_line.strip())
            current_line = word
    if current_line:
        lines.append(current_line.strip())
    return "\n".join(lines)

df['정제된문제'] = df['문제'].apply(wrap_text)
df['유사답안'].fillna('없음', inplace=True)

my_list = list(df.정제된문제)  # 데이터프레임에서 정제된문제 컬럼을 리스트로 가져옵니다.

score = 0  # 맞춘 문제 수를 기록하는 변수입니다.
questions_count = 0  # 출제된 문제 수를 기록하는 변수입니다.

# 시험 규칙을 출력합니다.
print("정처기 실기 시험을 시작합니다.")
print("\n사용 방법\n")
print("pass를 입력하면 다음 문제로 넘어갑니다.")
print("end를 입력하면 시험이 강제 종료됩니다.")
print("answer를 입력하시면 정답을 확인할 수 있습니다.")
print("최대한 많은 문제를 맞춰보세요!")

# 문항수
num_questions = 20

# 시험 진행
for i in range(num_questions):
    # 문항 수가 다 풀리면 게임 종료
    if num_questions == 0:
        print("\n모든 문항을 풀었습니다. 게임 종료!")
        print(f"맞춘 문항 수는 {score}개, 틀린 문항 수는 {questions_count - score}개입니다.")
        break
        
    # 랜덤 문제 선택
    random_value = random.choice(my_list)
    random_index = my_list.index(random_value)
    random_answer = df.정답[random_index]
    random_similar_answer = df.유사답안[random_index]
    random_large_keyword = df.문제대분류[random_index]
    random_small_keyword = df.문제소분류[random_index]
    random_appearence_date = df.출제연도[random_index]
    
    # 문제 출력
    print("=" * 80)
    print("=" * 80)
    print(f"출제연도: {random_appearence_date}")
    print(f"문제대분류: {random_large_keyword}")
    print(f"문제소분류: {random_small_keyword}")
    print(f"\n문제: {random_value}")
    
    first_answer = input("\n정답을 입력해주세요: ")

    # pass를 입력한 경우 다음 문제로 넘어감
    if first_answer.lower() == "pass":
        questions_count += 1
        num_questions -= 1
        print("\n다음 문제로 넘어갑니다.")
        continue
    # answer를 입력한 경우 정답 공개
    elif first_answer.lower() == "answer":
        questions_count += 1
        print("\n정답:", random_answer)
        print("유사답안:", random_similar_answer)
        continue
    # end를 입력한 경우 시험 강제 종료
    elif first_answer.lower() == "end":
        print("\n강제 종료.\n")
        print(f"맞춘 문항 수는 {score}개, 틀린 문항 수는 {questions_count - score}개입니다.")
        break
    else:
        while True:
            print(f'\n작성답안: {first_answer}')
            print("실제답안:", random_answer)
            print("유사답안:", random_similar_answer)
            answer = input("\n당신의 답이 정답이라고 생각하십니까?('정답/오답'으로 입력해주세요.): ")
            # 정답인 경우
            if answer == "정답":
                questions_count += 1
                score += 1
                num_questions -= 1
                print(f"\n축하드립니다! 현재 맞춘문제수는 {score}개입니다. 다음 문제로 넘어갑니다.")
                break
            elif answer == "오답":
                questions_count += 1
                num_questions -= 1
                print(f"\n유감입니다! 현재 맞춘문제수는 {score}개입니다. 다음 문제로 넘어갑니다.")
                break
            else:
                print("\n잘못된 입력입니다. 다시 입력해주세요.")
                print("'정답' 혹은 '오답'으로 입력해주세요.")
    
    # 남은 문항 수 출력
    print(f"남은 문항 수: {num_questions}개")
time.sleep(15)