import sys

#텍스트 파일에서 학생 데이터를 읽어와 전역 딕셔너리에 저장하는 함수
def load_stu():
    if len(sys.argv) == 1 : #파일명을 입력하지 않을 경우 default('student.txt')설정
        filename = 'students.txt' 
    else :
        filename = sys.argv[1]
    f = open(filename, 'r') #파일 읽어오기
    
    stu_dic = {}    
    for line in f:
        parts = line.split('\t') #탭을 기준으로 split하여 딕셔너리로 초기화.
        stu_id = parts[0]
        stu_name = parts[1]
        mid = int(parts[2])
        final = int(parts[3])
        avg = (mid + final) / 2
        grade = get_grade(avg)
        
        stu_dic[stu_id] = {
            'id' : stu_id, 
            'name' : stu_name, 
            'mid' : mid, 
            'final' : final, 
            'avg' : avg, 
            'grade' : grade
        }
    f.close()
    return stu_dic


#학점 계산 함수
def get_grade(avg): #평균을 입력받아 학점 반환
    if avg >= 90 :
        grade = 'A'
    elif avg >= 80 :
        grade = 'B'
    elif avg >= 70 :
        grade = 'C'
    elif avg >= 60:
        grade = 'D'
    else :
        grade = 'F'
    return grade


#상단 메뉴 출력 함수
def show_table_header():
    print("{:<10} {:>15} {:^10} {:^10} {:^10} {:^10}".format("Student", "Name", "Midterm", "Final", "Average", "Grade"))
    print("-----------------------------------------------------------------------")


#모든 학생의 정보를 정렬하여 출력하는 함수
def show_all_stu(): 
    sorted_stu_dic = sorted(stu_dic.items(), key=lambda x: x[1]['avg'], reverse=True) #딕셔너리 내림차순 정렬
    show_table_header() #상단 메뉴 출력
    for i in sorted_stu_dic: #전 학생 출력
        print("{:<10} {:>15} {:^10} {:^10} {:^10} {:^10}".format(i[1]['id'], i[1]['name'], i[1]['mid'], i[1]['final'], i[1]['avg'],  i[1]['grade']))


#특정 학생 출력 함수
def show_stu(stu_id): #학번을 입력받아 해당 학생 출력
    print("{:<10} {:>15} {:^10} {:^10} {:^10} {:^10}".format(stu_dic[stu_id]['id'], stu_dic[stu_id]['name'], stu_dic[stu_id]['mid'], stu_dic[stu_id]['final'], stu_dic[stu_id]['avg'], stu_dic[stu_id]['grade']))


#검색한 학생 출력 함수
def show_searched_stu():
    stu_id = input("Student ID: ") #학번 입력
    if stu_id in stu_dic: #학번 검색
        show_table_header() #상단 메뉴 출력
        show_stu(stu_id) #찾은 학생 출력
    else: #해당 학번의 학생 찾지 못하면 error message
        print("NO SUCH PERSON")


#학점 수정 함수
def change_score():
    stu_id = input("Student ID: ") #학번 입력
    if stu_id in stu_dic: #학번 검색
        exam = input("Mid/Final? ") #중간 or 기말 선택
        if exam in ["mid", "final"]:
            new_score = int(input("Input new score: ")) #새 점수 입력
            if 0 <= new_score <= 100: #점수는 0~100 사이의 값만 가능
                show_table_header() #상단 메뉴 출력
                show_stu(stu_id) #변경 전의 학생 정보 출력
                print("Score changed.")
                stu_dic[stu_id][exam] = new_score # 학점 계산 및 변경
                if exam == "mid":
                    avg = (new_score + stu_dic[stu_id]["final"]) / 2
                else:
                    avg = (stu_dic[stu_id]["mid"] + new_score) / 2
                stu_dic[stu_id]["avg"] = avg
                stu_dic[stu_id]["grade"] = get_grade(avg)
                show_stu(stu_id) #변경 후의 학생 정보 출력
    else: #해당 학번의 학생 찾지 못하면 error message
        print("NO SUCH PERSON")


#학점 검색 함수
def search_grade():
    grade = input("Grade to search: ") #학점 입력
    if grade in ['A', 'B', 'C', 'D', 'F']:#입력받은 학점이 A,B,C,D,F 인지 확인
        l = []
        for stu_id, info in stu_dic.items(): #해당 학생 검색
            if info['grade'] == grade:
                l.append(stu_id) #해당 학점을 가진 학생 아이디를 리스트에 저장
        if l: #리스트가 비어있지 않다면 (학생 검색 성공) 
            show_table_header() #상단 메뉴 출력
            for stu in l: #리스트를 순회하면 해당 학생을 출력
                show_stu(stu)
        else: #해당 학점이 없다면 erroer message
            print("NO RESULTS") 


#학생 추가 함수 
def add_stu():
    stu_id = input("Student ID: ") #학번 입력
    if stu_id not in stu_dic: #학번이 없다면 새로 학생 만들어 딕셔너리에 추가
        new_name = input("Name: ")
        new_mid = int(input("Midterm Score: "))
        new_final = int(input("Final Score: "))
        new_avg = (new_mid + new_final) / 2
        new_grade = get_grade(new_avg)
        stu_dic[stu_id] = {'id' : stu_id, 
			'name' : new_name, 
			'mid' : new_mid, 
			'final' : new_final, 
			'avg' : new_avg, 
			'grade' : new_grade}
        print("Student added.")
    else: #학번이 이미 있다면 error message
        print("ALREADY EXISTS.")


#학생 삭제 함수
def remove_stu():
    if not stu_dic: #딕셔너리가 비었다면 error message
        print("List is empty.")
    else: 
        stu_id = input("Student ID: ") #학번 입력
        if stu_id in stu_dic: #해당 학번 학생이 있다면 딕셔너리 삭제
            del stu_dic[stu_id]
            print("Student removed.")
        else: #해당 학번 학생이 없다면 error message
            print("NO SUCH PERSON.")


#프로그램 종료 함수
def quit():
    user_input = input("Save Data?[yes/no] ") #저장 여부 입력
    if user_input == "yes":
        filename = input("File name: ") #저장할 파일 이름 입력
        with open(filename, "w") as f:
            sorted_stu_dic = sorted(stu_dic.items(), key=lambda x: x[1]['avg'], reverse=True) #딕셔너리 내림차순 정렬
            for i in sorted_stu_dic: #정렬된 데이터를 한 줄씩 파일에 쓰기
                data = "{:<10} {:>15} {:^10} {:^10}".format(i[1]['id'], i[1]['name'], i[1]['mid'], i[1]['final']) + "\n"
                f.write(data)


#main 함수
stu_dic = load_stu() #프로그램 실행시키면 텍스트 파일로부터 데이터를 읽어옴

while(True):
    user_input = input("# ").lower() #사용자 명령어 입력 (대소문자 구분하지 않음)
    if user_input == "show":
        show_all_stu()
    elif user_input == "search":
        show_searched_stu()
    elif user_input == "changescore":
        change_score()
    elif user_input == "searchgrade":
        search_grade()
    elif user_input == "add":
        add_stu()
    elif user_input == "remove":
        remove_stu()
    elif user_input == "quit":
        quit()
        break



