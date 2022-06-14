from config.config_db import connection_db


# 회원목록 조회
def get_members():
    conn = connection_db()

    try:
        curs = conn.cursor()
        sql = '''
                SELECT * 
                FROM tbl_member;
              '''
        curs.execute(sql)
        rows = curs.fetchall()
    finally:
        conn.close()

    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    print(':: ID\tNAME\tPHONE\tDATE')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    for row in rows:
        print(f'::{row.values()}')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')


# 회원유무 판단
def member_match(member_num):
    conn = connection_db()

    try:
        curs = conn.cursor()
        sql = f'''
                SELECT *
                FROM tbl_member
                WHERE member_id = "{member_num}"
               '''
        curs.execute(sql)
        result = curs.rowcount  # fetchall 데이터 다 가져옴
    finally:
        conn.close()

    return result
