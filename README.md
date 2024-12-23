# DM_final_flask_test
架構圖:
front_and_back/
│
├── static/                       # 靜態資源
│   ├── CSS/                      # CSS 檔案
│   │   ├── general.css
│   │   ├── game.css
│   │   ├── showMatch.css
│   │   └── ...
│   ├── js/                       # JavaScript 檔案
│   │   ├── score.js
│   │   ├── game_data.js
│   │   └── ...
│   ├── logo/                     # 圖片和Logo
│   │   ├── team_logo_lions_500x500.png
│   │   ├── team_logo_guardians_500x500.png
│   │   └── ...
│   └── ...
│
├── templates/                    # Flask HTML 模板
│   ├── index.html
│   ├── allPlayersWithoutTeam.html
│   ├── game_details.html
│   ├── score.html
│   ├── winnerList.html
│   └── ...
│
├── app.py                         
├── run.py                        
├── model.py                     
├── requirements.txt              
├── route.py                      # 主要的路由檔案 
├── route_test.py                 # 測試用的路由檔案或實驗功能 （曾子堤編輯 只有做部份功能）
└── README.md                     
