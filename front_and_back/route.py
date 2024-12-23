from model import Player,Games,WinnerList
from datetime import datetime
from flask import Flask, render_template, jsonify, request


def register_routes(app,db):
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

    #取得特定年分的年度獎項名單
    @app.route('/winnerlist/searchyear', methods=['GET'])
    def get_winner_list():
        # 從查詢參數中獲取年份
        year = request.args.get('years')
        
        # 檢查是否提供年份
        if not year:
            return jsonify({"error": "Year parameter is required"}), 400
        try:
            # 查詢年份的資料
            
            winner = WinnerList.query.filter_by(years=int(year)).first()
            # 檢查是否找到資料
            if not winner:
                print("error1\n")
                return jsonify({"error": f"No winners found for the year {year}"}), 404

            # 將查詢結果轉為字典格式返回
            result =[{
                "years": winner.years,
                "most_hits_player_id": winner.most_hits_player_id,
                "highest_batting_average_player_id": winner.highest_batting_average_player_id,
                "most_RBI_player_id": winner.most_RBI_player_id,
                "most_stolen_bases_player_id": winner.most_stolen_bases_player_id,
                "homerun_leader_player_id": winner.homerun_leader_player_id,
                "most_wins_player_id": winner.most_wins_player_id,
                "strikeout_leader_player_id": winner.strikeout_leader_player_id,
                "lowest_ERA_player_id": winner.lowest_ERA_player_id,
                "most_saves_player_id": winner.most_saves_player_id,
                "most_holds_player_id": winner.most_holds_player_id
            }]
            print(jsonify(result))
            return jsonify(result)

        except Exception as e:
            print("ok\n")
            return jsonify({"error": str(e)}), 500

    # API：取得球員詳細資料
    @app.route('/players/searchplayer', methods=['GET'])
    def get_player():
        # 從請求中獲取 player_unique_id 參數
        player_unique_id = request.args.get('player_unique_id')

        # 檢查是否提供 player_unique_id
        if not player_unique_id:
            return jsonify({"error": "Player unique ID is required"}), 400

        try:
            # 查詢資料庫中的球員資訊
            print("ok\n")
            player = Player.query.filter_by(player_unique_id=int(player_unique_id)).first()

                # 如果未找到球員，返回錯誤訊息
            if not player:
                return jsonify({"message": "Player not found"}), 404

            # 將 ORM 對象轉換為字典格式返回
            result2 = [{
                    "player_name": player.player_name,
                    "player_unique_id": player.player_unique_id,
                    "t_b": player.t_b,
                    "height": player.height,
                    "weight": player.weight,
                    "born": player.born,
                    "debut": player.debut,
                    "nationality": player.nationality,
                    "draft_order": player.draft_order,
                    "position": player.position
            }]
            return jsonify(result2)

        except ValueError:
            return jsonify({"error": "Invalid player unique ID format"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    #回傳所有球員的id和名字
    @app.route('/player/getallplayer', methods=['GET'])
    def get_all_players():
        try:
            players = Player.query.all()
            if not players:
                return jsonify({"message": "No players found"}), 404

            # 將 ORM 對象轉換為 JSON
            result = [
                {
                    "player_name": player.player_name,
                    "player_unique_id": player.player_unique_id
                }
                for player in players
            ]
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    #用日期取得在該日期的所有球賽資訊
    @app.route('/games', methods=['GET'])
    def get_games_by_date():
        # 從請求中獲取 game_date 查詢參數
        game_date = request.args.get('game_date')

        # 驗證 game_date 是否存在
        if not game_date:
            return jsonify({"error": "game_date is required"}), 400

        try:
            print(game_date)
            # 查詢資料庫中符合 game_date 的比賽
            games = Games.query.filter_by(game_date=game_date).all()
            # 如果沒有找到比賽，返回提示訊息
            if not games:
                return jsonify({"message": f"No games found for the date {game_date}"}), 404

            # 將比賽數據轉為 JSON 格式返回
            results = []
            for game in games:
                results.append({
                    "game_date": game.game_date,
                    "home_team": game.home_team,
                    "away_team": game.away_team,
                    "home_score": game.home_score,
                    "away_score": game.away_score,
                    "game_number": game.game_number,
                    "HP": game.HP,
                    "1B": game.first_base,
                    "2B": game.second_base,
                    "3B": game.third_base,
                    "audience": game.audience,
                    "game_time": game.game_time,
                    "mvp_player": game.mvp_player,
                    "game_status": game.game_status
                })

            return jsonify(results)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    #回傳最近三場的比賽資料
    @app.route('/latest-games', methods=['GET'])
    def get_latest_games():
        # 默認限制返回3場比賽
        limit = int(request.args.get('limit', 3))
        
        try:
            # 按日期降序排列並限制比賽數量
            games = Games.query.order_by(Games.game_date.desc()).limit(limit).all()

            if not games:
                return jsonify({"message": "No games found"}), 404

            # 將比賽數據轉為 JSON 格式返回
            results = []
            for game in games:
                results.append({
                    "game_date": game.game_date,
                    "home_team": game.home_team,
                    "away_team": game.away_team,
                    "home_score": game.home_score,
                    "away_score": game.away_score,
                    "game_number": game.game_number,
                    "HP": game.HP,
                    "1B": game.first_base,
                    "2B": game.second_base,
                    "3B": game.third_base,
                    "audience": game.audience,
                    "game_time": game.game_time,
                    "mvp_player": game.mvp_player,
                    "game_status": game.game_status
                })

            return jsonify(results)

            

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    #刪除某一年的winnerlist
    @app.route('/winlist/delete', methods=['POST'])
    def delete_winlist_entry():
        data = request.get_json()
        year = data.get('year')

        # 檢查是否有提供年份
        if not year:
            return jsonify({"error": "Year is required"}), 400

        try:
            # 查詢資料庫中對應年份的資料
            winner = WinnerList.query.filter_by(years=year).first()

            if not winner:
                return jsonify({"message": f"No data found for year {year}"}), 404

            # 刪除資料
            db.session.delete(winner)
            db.session.commit()

            return jsonify({"message": f"Data for year {year} deleted successfully"}), 200

        except Exception as e:
            db.session.rollback()  # 回滾資料庫變更
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        

    # 刪除比賽資料
    @app.route('/delete_game', methods=['POST'])
    def delete_game():
        data = request.get_json()
        game_date = data.get('game_date')
        game_number = data.get('game_number')

        # 驗證請求參數
        if not game_date or not game_number:
            return jsonify({"error": "Both 'game_date' and 'game_number' are required."}), 400

        try:
            # 確認日期格式
            game_date = datetime.strptime(game_date, "%Y-%m-%d").date()

            # 查詢資料庫中的比賽
            game = Games.query.filter_by(game_date=game_date, game_number=game_number).first()
            if not game:
                return jsonify({"error": "Game not found for the specified date and number."}), 404

            # 刪除比賽
            db.session.delete(game)
            db.session.commit()

            return jsonify({"message": "Game deleted successfully."}), 200

        except Exception as e:
            db.session.rollback()  # 發生異常時回滾變更
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500