def classify_input(input_str):
    # 입력 문자열을 공백으로 분리하여 리스트로 변환
    input_list = [i for i in input_str.split(' ')]
    
    # 결과를 저장할 리스트 초기화
    insert_list = []
    delete_list = []
    search_list = []
    
    # 입력 리스트를 순회하면서 분류
    i = 0
    while i < len(input_list):
        # 현재 요소가 숫자인 경우
        if input_list[i].isdigit():
            next_i = i + 1
            # 다음 요소도 숫자인 경우
            if next_i < len(input_list) and input_list[next_i].isdigit():
                insert_list.append([int(input_list[i]), int(input_list[next_i])])
                i = next_i  # 다음 숫자도 처리됨
        else:
            # 현재 요소가 문자인 경우 (S 또는 D로 시작)
            command = input_list[i]
            num1 = int(input_list[i+1])
            num2 = int(input_list[i+2])
            if command == 'D':
                delete_list.append([num1, num2])
            elif command == 'S':
                search_list.append([num1, num2])
            i += 2  # 두 숫자를 건너뜀
        i += 1
    
    return insert_list, delete_list, search_list







def main() :
    # 예제 입력
    input_str = '123 50 224 30 123 25 24 25 123 40 224 77 S 123 25 D 123 25 D 123 40 D 224 100'
    insert_list, delete_list, search_list = classify_input(input_str)

    # 결과 출력
    print("Insert List:", insert_list)
    print("Delete List:", delete_list)
    print("Search List:", search_list)

if __name__ == '__main__':
    main()

