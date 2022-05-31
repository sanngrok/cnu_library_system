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
