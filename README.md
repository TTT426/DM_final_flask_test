# DM_final_flask_test
## 更新：
1. games_deatails.html -> game_details.html (檔名改了）
2. score 的相關功能即和版面
3. Player、Game的insert完成
4. Player的update完成

### 已完成:
Player / Winlist / Delete / Score

### 等待對接: （ route_test.py 成功 但 route.py 還沒試）
Game的update須更新

### 未完成:
Predict(ops+計算測試) / Update(剩winnerlist) /player顯示(預計根據隊伍顯示)

### 目前架構圖
![image](https://github.com/TTT426/DM_final_flask_test/blob/main/%E6%9E%B6%E6%A7%8B%E5%9C%96.png)

# 前端
.css .js放在 static 裡
.html (網頁）放在 templates

# 後端
route.py / app.py / model.py / run.py / requirements.txt 是最主要的後端程式
route_test是曾另外編輯的 是為了測試特定功能而架的後端 僅有特地功能
