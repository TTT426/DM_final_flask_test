from flask import Flask, render_template, jsonify, request
import mysql.connector
from datetime import datetime

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'hw3user',
    'password': '********',
    'database': 'final'
}

try:
    conn = mysql.connector.connect(**db_config)
    print("資料庫連線成功！")
    conn.close()
except mysql.connector.Error as err:
    print(f"資料庫連線失敗: {err}")

# Function to get a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Register Routes
#主頁連結
@app.route('/')
def home():
    return render_template('index.html')

#一次顯示所有球員
@app.route('/allPlayersWithoutTeam')
def all_players():
    return render_template('allPlayersWithoutTeam.html')

#球賽紀錄
@app.route('/score')
def score():
    return render_template('score.html')

#歷年年度獎項讀主
@app.route('/winnerlist')
def winnerlist():
    return render_template('winnerList.html')

#插入頁面
@app.route('/insert')
def insert():
    return render_template('insert.html')

#球賽詳細資訊
@app.route('/getgamedetail')
def getgamedetail():
    return render_template('games_details.html')

#個別球員詳細資料
@app.route('/player')
def player():
    return render_template('player.html')

#預測功能
@app.route('/predict')
def predict():
    return render_template('predict.html')
    
#更新資料庫
@app.route('/update')
def update():
    return render_template('Update.html')

#刪除資料庫
@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/latest-games', methods=['GET'])
def get_latest_games():
    # 默認限制返回3場比賽
    limit = int(request.args.get('limit', 3))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 按日期降序排列並限制比賽數量
        query = "SELECT * FROM games ORDER BY game_date DESC LIMIT %s"
        cursor.execute(query, (limit,))
        games = cursor.fetchall()
        cursor.close()
        conn.close()

        if not games:
            return jsonify({"message": "No games found"}), 404

        # 將比賽數據轉為 JSON 格式返回
        results = []
        for game in games:
            results.append({
                "game_date": game["game_date"],
                "home_team": game["home_team"],
                "away_team": game["away_team"],
                "home_score": game["home_score"],
                "away_score": game["away_score"],
                "game_number": game["game_number"],
                "HP": game["HP"],
                "1B": game["1B"],
                "2B": game["2B"],
                "3B": game["3B"],
                "audience": game["audience"],
                "game_time": game["time"]
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/games', methods=['GET'])
def get_games_by_date():
    # 從請求中獲取 game_date 查詢參數
    game_date = request.args.get('game_date')

    # 驗證 game_date 是否存在
    if not game_date:
        return jsonify({"error": "game_date is required"}), 400

    try:
        print(game_date)
        # 建立資料庫連線
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # 使用 dictionary=True 返回字典格式的結果

        # 查詢資料庫中符合 game_date 的比賽
        query = "SELECT * FROM games WHERE game_date = %s"
        cursor.execute(query, (game_date,))
        games = cursor.fetchall()

        cursor.close()
        conn.close()

        # 如果沒有找到比賽，返回提示訊息
        if not games:
            return jsonify({"message": f"No games found for the date {game_date}"}), 404

        # 將比賽數據轉為 JSON 格式返回
        results = []
        for game in games:
            results.append({
                "game_date": game["game_date"],
                "home_team": game["home_team"],
                "away_team": game["away_team"],
                "home_score": game["home_score"],
                "away_score": game["away_score"],
                "game_number": game["game_number"],
                "HP": game["HP"],
                "1B": game["1B"],
                "2B": game["2B"],
                "3B": game["3B"],
                "audience": game["audience"],
                "game_time": game["time"],  # 修正為 time 對應的欄位名稱
                "mvp_player": game["mvp_player"]
            })

        return jsonify(results)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/game_details', methods=['GET'])
def game_details():
    # 提取 URL 参数
    game_id = request.args.get('id')
    game_date = request.args.get('data')

    # 确保参数存在
    if not game_id or not game_date:
        return "Game ID and Date are required!", 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM games WHERE game_number = %s AND game_date = %s"
        cursor.execute(query, (game_id, game_date))
        game = cursor.fetchone()
        cursor.close()
        conn.close()

        print(game)
        if not game:
            return "No game found with the given ID and date.", 404

        # 直接傳 html
        return render_template('game_details.html', game=game)

    except mysql.connector.Error as e:
        return f"Database error: {str(e)}", 500
    
@app.route('/check-pitcher', methods=['GET'])
def check_pitcher():
    # 從 URL 參數中獲取投手名字
    pitcher_name = request.args.get('name')

    # 檢查是否有輸入投手名字
    if not pitcher_name:
        return jsonify({'exists': False, 'pitchers': []})

    try:
        # 連接資料庫並查詢匹配的投手
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM players WHERE name = %s"
        cursor.execute(query, (pitcher_name,))
        pitchers = cursor.fetchall()  # 查詢結果返回列表
        cursor.close()
        conn.close()

        # 如果找到匹配的投手，返回 exists = True，否則返回 False
        if pitchers:
            return jsonify({'exists': True, 'pitchers': pitchers})
        else:
            return jsonify({'exists': False, 'pitchers': []})

    except mysql.connector.Error as e:
        # 捕捉資料庫錯誤並返回
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/check-batter', methods=['GET'])
def check_batter():
    batter_name = request.args.get('name')

    # 檢查是否有輸入投手名字
    if not batter_name:
        return jsonify({'exists': False, 'batters': []})
    
    try:
        # 連接資料庫並查詢匹配的投手
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM players WHERE name = %s"
        cursor.execute(query, (batter_name,))
        batters = cursor.fetchall()  # 查詢結果返回列表
        cursor.close()
        conn.close()
    # 如果找到匹配的投手，返回 exists = True，否則返回 False
        if batters:
            return jsonify({'exists': True, 'batters': batters})
        else:
            return jsonify({'exists': False, 'batters': []})

    except mysql.connector.Error as e:
        # 捕捉資料庫錯誤並返回
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/show-outcome', methods=['GET'])
def show_outcome():
    pitcher_id = request.args.get('pitcher_id')
    batter_id = request.args.get('batter_id')
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM match_results WHERE pitcher_id = %s and batter_id = %s and year between %s and %s"; 
        cursor.execute(query, (pitcher_id, batter_id, year1, year2))
        battles = cursor.fetchall()  # 查詢結果返回列表
        cursor.close()
        conn.close()
        print(battles)
        # 返回查詢結果
        if battles:
           return jsonify({'success': True, 'battles': battles})
        else: 
            return jsonify({'success': True, 'battles': []})

    except mysql.connector.Error as e:
        # 捕捉資料庫錯誤並返回
        return jsonify({'error': f'Database error: {str(e)}'}), 500
 
@app.route('/predict-outcome', methods=['GET'])
def predict_outcome():
    pitcher_id = request.args.get('pitcher_id')
    batter_id = request.args.get('batter_id')
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')

    try:
        # 先確認有沒有這場比賽 沒有的話直接回傳
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query1 = "SELECT * FROM match_results WHERE pitcher_id = %s and batter_id = %s and year between %s and %s"; 
        cursor.execute(query1, (pitcher_id, batter_id, year1, year2))
        the_result = cursor.fetchall()
        if not the_result:
            print("No")
            # 如果没有比赛结果，返回错误消息
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '查無比賽結果 故無法預測'})
        
        ## 我預期你會傳給我的.json的格式
        query = "SELECT * FROM output WHERE pitcher_id = %s and batter_id = %s"; 
        cursor.execute(query, (pitcher_id, batter_id))
        the_result = cursor.fetchall()  # 查詢結果返回列表
        cursor.close()
        conn.close()

        
        # 返回查詢結果
        if the_result:
           return jsonify({'success': True, 'the_result': the_result})
        else: 
            return jsonify({'success': True, 'the_result': []})

    except mysql.connector.Error as e:
        # 捕捉資料庫錯誤並返回
        return jsonify({'error': f'Database error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)