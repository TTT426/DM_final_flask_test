from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 模擬數據：年份的獲獎者資料
winners_data = [
    {
        "year": "2015",
        "most_hits_player_id": "1",
        "highest_batting_average_player_id": "2",
        "most_stolen_bases_player_id": "3",
        "most_RBI_player_id": "4",
        "most_wins_player_id": "5",
        "most_saves_player_id": "6",
        "most_holds_player_id": "7",
        "strikeout_leader_player_id": "8",
        "homerun_leader_player_id": "9",
        "lowest_ERA_player_id": "10",
    },
    {
        "year": "2016",
        "most_hits_player_id": "11",
        "highest_batting_average_player_id": "12",
        "most_stolen_bases_player_id": "13",
        "most_RBI_player_id": "14",
        "most_wins_player_id": "15",
        "most_saves_player_id": "16",
        "most_holds_player_id": "17",
        "strikeout_leader_player_id": "18",
        "homerun_leader_player_id": "19",
        "lowest_ERA_player_id": "20",
    }
]

# 模擬球員資料
players_data = {
    "1": {"player_name": "John Doe"},
    "2": {"player_name": "Jane Smith"},
    "3": {"player_name": "Jim Brown"},
    "4": {"player_name": "Tom Green"},
    "5": {"player_name": "Alice White"},
    "6": {"player_name": "Bob Black"},
    "7": {"player_name": "Charlie Blue"},
    "8": {"player_name": "David Gray"},
    "9": {"player_name": "Eva Yellow"},
    "10": {"player_name": "Frank Red"}
}

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/allPlayersWithoutTeam')
def all_players():
    return render_template('allPlayersWithoutTeam.html')

@app.route('/score')
def score():
    return render_template('score.html')

@app.route('/winnerlist')
def winnerlist():
    return render_template('winnerList.html')

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/getgamedetail')
def getgamedetail():
    return render_template('games_deatails.html')

@app.route('/player')
def player():
    return render_template('player.html')

@app.route('/update')
def update():
    return render_template('Update.html')

@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/winnerlist/searchyear', methods=['GET'])
def get_winner_list():
    # Retrieve the 'years' query parameter
    year = request.args.get('years')
    
    # Validate the input parameter
    if not year:
        return jsonify({"error": "Year parameter is required"}), 400
    
    # Find winners for the given year
    winners_for_year = [winner for winner in winners_data if winner['year'] == year]
    
    # Check if any data was found for the specified year
    if not winners_for_year:
        return jsonify({"error": f"No winners found for the year {year}"}), 404

    # Return the winners data for the specified year
    return jsonify(winners_for_year)

# API：取得球員詳細資料
@app.route('/players/searchplayer', methods=['GET'])
def get_player():
    player_unique_id = request.args.get('player_unique_id')
    player = players_data.get(player_unique_id)
    if player:
        return jsonify([player])
    else:
        return jsonify({"message": "Player not found"}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
