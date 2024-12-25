# 改動

##### CSS:

新代碼 fChoosePlayer.css, newForm.css
改動 navigationBar.css
可刪除 Form.css

##### html:

新代碼 insertGame.html, insertPlayer.html, updatePlayer.html updateWinnerList.html
可刪除 temp.html, test.html, update.html, insert.html

##### javascript:

新代碼 editModeNavigation.js, insertPlayer.js, insertGame.js, updatePlayer.js, updateWinnerList.js, playerSearch.js
可刪除 insertNavigation.js, updateNavigation.js, submitPlayer.js,

# 後端(可能)需更改

### editModeNavigation.js:

11, 12, 47, 48: html 連結

---

### insertGame.js:

83: post game 傳的 jason 跟之前一樣

---

### insertPlayer.js:

151: post player 傳的 jason 跟之前一樣

---

### updatePlayer.js:

1: import
174: update players/{要更改的 unique_id}

##### JSON:

```jason
transferData = {
"player_name": name,
"number": number,
"t_b": tb,
"height": height,
"weight": weight,
"born": birthday,
"debut": debut,
"nationality": nationality,
"draft_order": draftOrder,
"position": position
}
```

---

### updateWinnerList.js:

1: `import`
11: Fetch player ID by year (跟之前一樣)
19: Fetch playerData by unique ID (跟之前一樣)
101: Update `winnerlist/{年}`

##### JSON:

```json
const transferData = {
  "most_hits_player_id": hitKing,
  "highest_batting_average_player_id": highest_batting_average,
  "most_RBI_player_id": RBI_player,
  "most_stolen_bases_player_id": most_stolen_bases_player,
  "homerun_leader_player_id": homerun_leader_player,
  "most_wins_player_id": most_wins_player,
  "strikeout_leader_player_id": strikeout_leader_player,
  "lowest_ERA_player_id": lowest_ERA_player,
  "most_saves_player_id": most_saves_player,
  "most_holds_player_id": most_holds_player
}
```

---

### playerSearch.js:

29: 用前綴名子搜球員名子和 id (要鎖傳過來的數量)
101: fetch playerData by unique id 跟之前一樣
