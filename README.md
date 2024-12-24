# DM_final_flask_test
## 更新：
1. 我在搞事 目前在github上的game_detail.html有問題 不要更新 有好心人有正常的話在幫我丟上來  
2. score.html 更新了（只動版面 功能不變）
3. predict 『大致』完成 （css 跟 html 都有變更)
4. route_test增加四個功能(皆for predict) (重點觀察 predict.js predict.html)
   (1) @app.route('/check-pitcher', methods=['GET']) -- 用來確認使用者輸入的人是不是在資料庫裡的球員 （前端傳 名子） 
   (2) @app.route('/check-batter', methods=['GET']) -- 用來確認使用者輸入的人是不是在資料庫裡的球員 ( (1) 跟 (2) 可能可以合併成一個 但我做完才想到 ）（前端傳 名子） 
   (3) @app.route('/show-outcome', methods=['GET']) -- 顯示投打對決的紀錄
       目前(3)的架構是 前端傳 : pitcher_id / batter_id / year1 / year2 (保證 year1 <= year2) 後端投打對決的所有資料
   (4) @app.route('/predict-outcome', methods=['GET']) -- 顯示出ops+
      (註）(4) 的參考價值極低 因為我不會算 ops+ 我在實做時事直接當作刪了 直接把計算的結果顯示出來
         目前(4)的架構是 前端傳 : pitcher_id / batter_id / year1 / year2 (保證 year1 <= year2)
         期望後端傳: 1. 球員上壘率 2. 聯盟上壘率 3. 球員長打率 4. 聯盟長打率 5. OPS+ 
### 已完成:
 Winlist / Delete / Score

### 等待對接: （ route_test.py 成功 但 route.py 還沒試）
predict

### 未完成:
Insert / Update /player顯示(預計根據隊伍顯示)

### 目前架構圖
![image](https://github.com/TTT426/DM_final_flask_test/blob/main/%E6%9E%B6%E6%A7%8B%E5%9C%96.png)

# 前端
.css .js放在 static 裡
.html (網頁）放在 templates

# 後端
route.py / app.py / model.py / run.py / requirements.txt 是最主要的後端程式
route_test是曾另外編輯的 是為了測試特定功能而架的後端 僅有特地功能
