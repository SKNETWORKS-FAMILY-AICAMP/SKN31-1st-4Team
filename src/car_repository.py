# car_repository.py >> 모든 DB 쿼리 메소드

import mysql.connecter
import streamlit as st

# 공통 접속정보
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "본인비밀번호",
    "database": "used_car_db",
    "charset":  "utf8mb4"
}

# [시세 조회 페이지] 차량 목록 조회
# 사이드바 필터(연료, 사고이력, 가격범위, 연식)를 받아 결과 반환

def get_cars(fuel_list, accident, price_min, price_max, year_min, year_max, sort):
    conn   = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    

    sql    = "SELECT * FROM cars WHERE price BETWEEN %s AND %s"
    params = [price_min, price_max]

    # 연료 필터
    if fuel_list:
        placeholders = ", ".join(["%s"] * len(fuel_list))
        sql   += f" AND fuel IN ({placeholders})"
        params += fuel_list
 
    # 사고 필터
    if accident == False:
        sql    += " AND (accident IS NULL OR accident = '' OR accident = '조회실패')"
    elif accident == True:
        sql    += " AND accident NOT IN ('', '조회실패') AND accident IS NOT NULL"
 
    # 연식 필터 (연식 컬럼이 '202104.0' 형태라 앞 4자리만 비교)
    sql    += " AND CAST(LEFT(year, 4) AS UNSIGNED) BETWEEN %s AND %s"
    params += [year_min, year_max]
 
    # 정렬
    sort_map = {
        "가격 낮은순":    "price ASC",
        "가격 높은순":    "price DESC",
        "연식 최신순":    "year DESC",
        "주행거리 낮은순": "mileage ASC"
    }
    sql += f" ORDER BY {sort_map.get(sort, 'price ASC')}"
 
    cursor.execute(sql, params)
    result = cursor.fetchall()
 
    cursor.close()
    conn.close()
    return result

# [시세 조회 페이지] 전체 건수 (검색 결과 N건 표시용)

def count_cars(fuel_list, accident, price_min, price_max, year_min, year_max):
    conn   = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
 
    sql    = "SELECT COUNT(*) FROM cars WHERE price BETWEEN %s AND %s"
    params = [price_min, price_max]
 
    if fuel_list:
        placeholders = ", ".join(["%s"] * len(fuel_list))
        sql   += f" AND fuel IN ({placeholders})"
        params += fuel_list
 
    if accident == False:
        sql    += " AND (accident IS NULL OR accident = '' OR accident = '조회실패')"
    elif accident == True:
        sql    += " AND accident NOT IN ('', '조회실패') AND accident IS NOT NULL"
 
    sql    += " AND CAST(LEFT(year, 4) AS UNSIGNED) BETWEEN %s AND %s"
    params += [year_min, year_max]
 
    cursor.execute(sql, params)
    result = cursor.fetchone()[0]
 
    cursor.close()
    conn.close()
    return result

# ─────────────────────────────────────────────────────────────
# [내 차 시세 페이지] 차량명 검색으로 유사 매물 시세 조회
# ─────────────────────────────────────────────────────────────

def search_my_car(keyword):
    conn   = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
 
    sql = """
        SELECT car_name, price, year, mileage, fuel, accident,
               avg_price, min_price, max_price, source
        FROM   cars
        WHERE  car_name LIKE %s
        ORDER  BY price ASC
    """
    cursor.execute(sql, (f"%{keyword}%",))
    result = cursor.fetchall()
 
    cursor.close()
    conn.close()
    return result
