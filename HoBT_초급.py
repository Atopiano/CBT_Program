import pandas as pd
import time
import sys

# 데이터셋 로딩
df = pd.read_csv('HoJikBT_1.1.csv')

# 문제대분류 기준으로 데이터프레임을 셔플하고, 상위 20개를 선택합니다.
df = df.sample(frac=1).groupby('문제대분류').head(2)
df = df[0:20]
df.reset_index(inplace=True, drop=True)
df.문제대분류.value_counts()

# 문제 출력 정제 함수
def wrap_text(text):
    # 줄바꿈 처리된 문자열을 저장할 리스트
    lines = []
    # 현재 줄에 쌓인 단어들을 저장할 문자열
    current_line = ""
    # 입력된 문자열을 공백을 기준으로 단어를 분리하여 처리
    for word in text.split():
        if word.endswith(".") or word.endswith("?"):
            # 단어가 마침표(.)나 물음표(?)로 끝나면,
            # 현재 줄에 단어를 추가한 후, 현재 줄을 처리하고 다음 줄로 이동
            current_line += " " + word
            lines.append(current_line.strip())
            # 출력 결과에 공백이 없도록 다음 줄에 대해 개행 문자를 추가하지 않음
            current_line = ""
        else:
            # 현재 줄에 단어를 추가할 수 있는 경우 추가
            if len(current_line) + len(word) + 1 <= 50:
                current_line += " " + word
            # 현재 줄에 더 이상 단어를 추가할 수 없는 경우 다음 줄로 이동
            else:
                lines.append(current_line.strip())
                current_line = word
    # 남은 단어를 처리하여 출력 결과 생성
    if current_line:
        lines.append(current_line.strip())
    return "\n".join(lines)

df['정제된문제'] = df['문제'].apply(wrap_text)
df['유사답안'].fillna('없음', inplace=True)

my_list = list(df.정제된문제)  # 데이터프레임에서 정제된문제 컬럼을 리스트로 가져옵니다.

score = 0  # 맞춘 문제 수를 기록하는 변수입니다.
questions_count = 0  # 출제된 문제 수를 기록하는 변수입니다.

# 시험 규칙을 출력합니다.
print("-" * 80)
print("정처기 실기 시험을 시작합니다.")
print("초급 버전은 ncs모듈별로 문제가 고르게 출제되어\n여러번 풀경우 같은 문제가 많이 보일 수 있습니다.\n실력을 향상시켜 중급버전도 풀어보세요!")
print("-" * 80)
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
    if score >= 14:
        print("*" * 80)
        print(f"축하합니다! 합격입니다!\n프로그램을 다시 시작해서 새로운 문제를 풀어보세요!")
        print("*" * 80)
    elif 12 <= score <14:
        print("*" * 80)
        print(f"축하합니다! 합격입니다!\n점수를 70점까지 올려보세요!")
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