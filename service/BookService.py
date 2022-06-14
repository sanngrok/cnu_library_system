import pymysql

from config.config_db import connection_db
from service.MemberService import member_match

# 도서목록 조회
def get_books():

    # 1. MariaDB Connection 성공하면
    conn = connection_db()  # Connection -> MariaDB

    try:
        curs = conn.cursor()             # 2. cursor() 객체를 사용해서 작업(노동자)
        sql = "SELECT * FROM tbl_book;"  # 3. MariaDB 실행 SQL문(실행 x)
        curs.execute(sql)                # 4. cursor() 객체를 통해서 SQL문 실행(실행 O)

        # fetchall()  -> 모든 row 반환
        # fetchone()  -> 1개 row 반환
        # fetchmany() -> n개 row 반환
        rows = curs.fetchall()           # 5. 실행 결과 받기
    finally:
        conn.close()                     # 6. MariaDB Connection 끊기

    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    print(':: ISBN\tTITLE\tWRITER\tPUBLISHER\tPRICE\tDATE')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    for row in rows:
        print(f'::{row.values()}')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')


# 도서 검색
def search_books():
    print(':: 검색하고 싶은 키워드를 입력하세요.')
    keyword = input('>> 검색 키워드: ')

    conn = connection_db()
    try:
        curs = conn.cursor()

        # keyword = "파이썬"
        # SELECT문 (DB로부터 데이터를 GET)
        #  3: SELECT *                            # 데이터의 어떤 Column을 가져올지
        #  1: FROM tbl_book                       # table 설정
        #  2: WHERE book_name LIKE '%{keyword}%'  # 필터: book_name에 keyword 포함:

        sql = f'''
                SELECT *
                FROM tbl_book
                WHERE book_name LIKE '%{keyword}
                      OR book_writer LIKE '%{keyword}%'
              '''
        curs.execute(sql)
        rows = curs.fetchall()
    finally:
        conn.close()

    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    print(':: ISBN\tTITLE\tWRITER\tPUBLISHER\tPRICE\tDATE')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    for row in rows:
        print(f'::{row.values()}')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')


# 도서 대출
def rental_books():
    # 1.회원 조회(tbl_member)
    print('::회원번호를 입력하세요.')
    member_num = input('>> 회원 번호: ')

    # result = 1(회원), 0(비회원)
    result = member_match(member_num)

    print(result)

    # 2.도서 대출 => 대출 정보 저장(tbl_rental)
    if result == 1:
        # 2-1. 대출 가능한 책인지 판단!
        print(':: 대출하고 싶은 도서 ISBN을 입력하세요.')
        book_isbn = input('>> ISBN:')
        count = book_yn(book_isbn, 'y')  # 도서 대출 가능 확인
        print(count)

        if count == 1:  # 대출 가능
            conn = connection_db()
            try:
                curs = conn.cursor()
                sql = f'''
                         INSERT INTO tbl_rental(book_ISBN, member_id)
                         VALUES({book_isbn}, {member_num})
                       '''
                curs.execute(sql)

                print(f'#MSG: "{member_num}"회원님 도서 "{book_isbn}" 1권 대출 완료하였습니다.')
                # 3.도서 보유 정보 수정 => 대출한 책 Count -1(tbl_book)
                book_update_yn(book_isbn, 'n')

            finally:
                conn.close()

        else:  # 대출 불가!
            # 경고 메세지 출력 후 메인화면 전환
            print(f'#Warning: "{book_isbn}"도서는 대출이 불가능합니다.')
            return

    else:
        # 경고 메세지 출력 후 메인화면 전환
        print('#Warning: 회원이 아닙니다. 회원 등록을 먼저 해주세요.')
        return



# 도서 대출 가능 확인
def book_yn(book_isbn, use_yn):
    conn = connection_db()
    try:
        curs = conn.cursor()
        sql = f'''
                 SELECT *
                 FROM tbl_book
                 WHERE book_isbn = "{book_isbn}"
                 AND useyn = "{use_yn}"
               '''
        curs.execute(sql)
        result = curs.rowcount
    finally:
        conn.close()
    return result


# tbl_book 테이블의 도서의 대출 유무를 변경(y->n or n->y)
def book_update_yn(book_isbn, use_yn):
    conn = connection_db()
    try:
        curs = conn.cursor()
        sql = f'''
                UPDATE tbl_book
                SET useyn = "{use_yn}"
                WHERE book_isbn = "{book_isbn}"
               '''
        curs.execute(sql)
    finally:
        conn.close()

# 도서반납
def return_books():
    print(':: 회원번호를 입력하세요.')
    member_num = input('>> 회원번호: ')
    # 회원이면 1, 아니면 0
    result = member_match(member_num)

    if result == 1:  # 회원인 경우
        print(':: 반납하고싶은 도서 ISBN을 입력하세요.')
        book_isbn = input('>> ISBN: ')
        count = book_yn(book_isbn, 'n')  # n = 대출이 된 도서(반납가능)

        if count == 1:  # 반납 가능
            conn = connection_db()
            try:
                curs = conn.cursor()
                sql = f'''
                        UPDATE tbl_rental SET
                        return_at = now()
                        WHERE book_ISBN = {book_isbn}
                        AND member_id = '{member_num}'
                       '''
                curs.execute(sql)
                book_update_yn(book_isbn, 'y')
                print(f'#MSG: "{member_num}"회원님의 도서 "{book_isbn}" 1권을 반납하였습니다.')
            finally:
                conn.close()
        else:  # 반납 불가
            print(f'#Warning: "{book_isbn}"은 반납이 불가합니다.')
            return

    else:  # 회원이 아닌경우
        print('#Warning: 회원이 아닙니다. 회원 등록을 먼저 해주세요.')
        return
