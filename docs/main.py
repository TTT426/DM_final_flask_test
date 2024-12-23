from flask import Flask, render_template, request, redirect, flash, session, jsonify
from datetime import datetime
import mysql.connector


# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'hw3user',
    'password': 'hw3password',
    'database': 'final'
}

try:
    conn = mysql.connector.connect(**db_config)
    print("資料庫連線成功！")
    conn.close()
except mysql.connector.Error as err:
    print(f"資料庫連線失敗: {err}")

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@ app.route('/')
def index():
    # delete.html作為首頁
    return render_template('Delete.html')

# Delete Page - winlist （ for delete winlist table)
@app.route('/winlist', methods=['POST', 'GET'])
def winlist():
    data = request.json
    year = data.get('year')
    try:
        # 連接資料庫
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 刪除對應年份的資料
        delete_query = "DELETE FROM winlist WHERE years = %s"
        cursor.execute(delete_query, (year,))
        conn.commit()

        # 檢查刪除的行數
        if cursor.rowcount > 0:
            return jsonify({"message": f"刪除年份 {year} 的資料"}), 200
        else:
            return jsonify({"message": f"未找到年份 {year} 的資料"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": f"資料庫錯誤: {err}"}), 500

    finally:
        # 確保連線釋放
        if conn.is_connected():
            cursor.close()
            conn.close()

# Delete page - game ( for delete game_info and plate_appearance)
@app.route('/game', methods=['GET'])
def game():
    try:
        # 取得前端傳來的查詢參數
        date = request.args.get('date')

        # 檢查參數是否完整
        if not date:
            return jsonify({"error": "缺少必要的查詢參數 'date'"}), 400

        # 驗證日期格式
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "日期格式不正確，應為 YYYY-MM-DD"}), 400

        # 查詢資料庫
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM game_info WHERE game_date = %s", (date,))
        games = cursor.fetchall()
        conn.close()

        # 如果沒有比賽資料
        if not games:
            return jsonify({"error": "該日期沒有比賽資料"}), 404

        # 整理比賽資料
        game_list = []
        for game in games:
            game_list.append({
                "game_date": game["game_date"],
                "home_team": game["home_team"],
                "away_team": game["away_team"],
                "home_score": game["home_score"],
                "away_score": game["away_score"],
                "mvp_player": game["mvp_player"],
                "game_number": game["game_number"]
            })

        # 回傳比賽資料
        return jsonify({"message": "查詢成功", "games": game_list}), 200

    except Exception as e:
        # 錯誤處理
        return jsonify({"error": str(e)}), 500

# Delete-game 
@app.route('/delete_game', methods=['POST'])
def delete_game():
    try:
        # 獲取前端傳來的 game_date 和 game_number
        data = request.json
        game_date = data.get('game_date')
        game_number = data.get('game_number')
        if not game_date or not game_number:
            return jsonify({"error": "缺少必要的參數"}), 400

        # 連接資料庫並執行刪除操作
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM game_info WHERE game_date = %s AND game_number = %s",
            (game_date, game_number),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "比賽已成功刪除"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
