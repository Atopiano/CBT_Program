import pandas as pd
import time
import sys

# 데이터셋 로딩
df = pd.read_csv('HoBT_1.1.csv')

# 문제대분류 기준으로 데이터프레임을 셔플하고, 상위 20개를 선택합니다.
df = df.sample(frac=1).groupby('문제대분류').head(2)
df = df[0:20]
df.reset_index(inplace=True, drop=True)
df.문제대분류.value_counts()

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
print("총 문항 수는 20문제입니다. 12문제 이상 맞추면 합격입니다.")
print("불합격하셨을경우 문제를 다시 푸는 것을 추천드립니다.")
print("\n사용 방법\n")
print("pass를 입력하면 다음 문제로 넘어갑니다.")
print("end를 입력하면 시험이 강제 종료됩니다.")
print("answer를 입력하시면 정답을 확인할 수 있습니다.")
print("최대한 많은 문제를 맞춰보세요!")

num_questions = 20

while True:
    # 시험 진행
    for i in range(num_questions):
            
        # 랜덤 문제 선택
        value = df.정제된문제[i]
        answer = df.정답[i]
        similar_answer = df.유사답안[i]
        large_keyword = df.문제대분류[i]
        small_keyword = df.문제소분류[i]
        appearence_date = df.출제연도[i]
        
        # 문제 출력
        print("=" * 80)
        print("=" * 80)
        print(f"출제연도: {appearence_date}")
        print(f"문제대분류: {large_keyword}")
        print(f"문제소분류: {small_keyword}")
        print(f"\n문제: {value}")
        
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
            print("\n정답:", answer)
            print("유사답안:", similar_answer)
            continue
        # end를 입력한 경우 시험 강제 종료
        elif first_answer.lower() == "end":
            print("\n강제 종료.\n")
            break
        else:
            while True:
                print(f'\n작성답안: {first_answer}')
                print("실제답안:", answer)
                print("유사답안:", similar_answer)
                judge = input("\n당신의 답이 정답이라고 생각하십니까?(정답: '1', 오답: '2'로 입력해주세요.): ")
                # 정답인 경우
                if judge == "1":
                    questions_count += 1
                    score += 1
                    num_questions -= 1
                    print(f"\n축하드립니다! 현재 맞춘문제수는 {score}개입니다. 다음 문제로 넘어갑니다.")
                    break
                elif judge == "2":
                    questions_count += 1
                    num_questions -= 1
                    print(f"\n유감입니다! 현재 맞춘문제수는 {score}개입니다. 다음 문제로 넘어갑니다.")
                    break
                else:
                    print("\n잘못된 입력입니다. 다시 입력해주세요.")
                    print("정답: '1', 오답: '2'로 입력해주세요.")
        
        # 남은 문항 수 출력
        print(f"남은 문항 수: {num_questions}개")

    print("\n모든 문항을 풀었습니다. 시험 종료!")
    print(f"맞춘 문항 수는 {score}개, 틀린 문항 수는 {questions_count - score}개입니다.\n")
    if score >= 12:
        print("*" * 80)
        print(f"축하합니다! 합격입니다!\n프로그램을 다시 시작해서 새로운 문제를 풀어보세요!")
        print("*" * 80)
    else:
        print("*" * 80)
        print(f"불합격입니다! 문제를 다시 풀어보세요!")
        print("*" * 80)
    print(f"\n문제를 다시 풀고 싶으면 're'를, 종료하고 싶으면 'exit'를 입력해주세요!\n")

    while True:               
        user_decision = input("re/exit 중 입력해주세요: ")
        
        if user_decision == "re":
            num_questions = 20
            score = 0  # 맞춘 문제 수를 기록하는 변수입니다.
            questions_count = 0  # 출제된 문제 수를 기록하는 변수입니다.
            break
        elif user_decision == "exit":
            print("\n시험을 종료합니다.")
            print("5초후에 자동 종료됩니다.")
            time.sleep(5)
            sys.exit()
        else:
            print("잘못된 입력입니다.")
        continue