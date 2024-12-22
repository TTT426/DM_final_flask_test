 // 按鈕功能設定
 document.getElementById("winlist").addEventListener("click", function () {
    // 彈出提示框讓使用者輸入年份
    const year = prompt("請輸入年份（西元年）：");
    if (!year || isNaN(year) || year.length !== 4) {
        alert("請輸入正確的四位數年份！");
        return;
    }

    // 將年份發送到後端
    fetch('http://127.0.0.1:5000/winlist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ year: year }) // 將年份包裝成 JSON
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`錯誤: ${data.error}`);
        } else {
            alert(`${data.message}`);
        }
    })
    .catch(error => {
        console.error('錯誤:', error);
        alert('請求失敗，請檢查伺服器是否正在運行。');
    });
});

document.getElementById("game").addEventListener("click", function () {
    // 建立年份選單
    const yearSelect = document.createElement("select");
    yearSelect.id = "yearSelect";
    for (let i = 1990; i <= new Date().getFullYear(); i++) {
        const option = document.createElement("option");
        option.value = i;
        option.textContent = i;
        yearSelect.appendChild(option);
    }

    // 建立月份選單
    const monthSelect = document.createElement("select");
    monthSelect.id = "monthSelect";
    for (let i = 1; i <= 12; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.textContent = i;
        monthSelect.appendChild(option);
    }

    // 建立日期選單
    const daySelect = document.createElement("select");
    daySelect.id = "daySelect";

    // 動態更新日期選單
    function updateDays() {
        const year = parseInt(yearSelect.value, 10);
        const month = parseInt(monthSelect.value, 10);
        const daysInMonth = new Date(year, month, 0).getDate();

        daySelect.innerHTML = ""; // 清空原有的選項
        for (let i = 1; i <= daysInMonth; i++) {
            const option = document.createElement("option");
            option.value = i;
            option.textContent = i;
            daySelect.appendChild(option);
        }
    }

    yearSelect.addEventListener("change", updateDays);
    monthSelect.addEventListener("change", updateDays);

    // 初始化選單
    updateDays();

    // 彈出對話框
    const dialog = document.createElement("div");
    dialog.style.position = "fixed";
    dialog.style.left = "50%";
    dialog.style.top = "50%";
    dialog.style.transform = "translate(-50%, -50%)";
    dialog.style.background = "#fff";
    dialog.style.padding = "20px";
    dialog.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";
    dialog.style.zIndex = "1000";

    dialog.innerHTML = `<p>請選擇日期(西元年/月/日）</p>`;
    dialog.appendChild(yearSelect);
    dialog.appendChild(monthSelect);
    dialog.appendChild(daySelect);

    const submitButton = document.createElement("button");
    submitButton.textContent = "確定";
    submitButton.addEventListener("click", function () {
        const year = yearSelect.value;
        const month = monthSelect.value;
        const day = daySelect.value;

        // 發送日期到後端
        fetch('http://127.0.0.1:5000/game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            
            body: JSON.stringify({ year: year, month: month, day: day })
        })
        
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`錯誤: ${data.error}`);
            } else {
                const games = data.games;

                // 找到顯示結果的容器
                const resultContainer = document.getElementById("resultContainer");
                resultContainer.innerHTML = ""; // 清空之前的結果

                // 動態生成比賽資訊
                games.forEach(game => {
                    const gameCard = document.createElement("div");
                    gameCard.className = "game-card";
                    
                    // 確保 game.game_date 是 YYYY-MM-DD 格式
                    const formattedDate = new Date(game.game_date).toISOString().split('T')[0];
                    
                    gameCard.innerHTML = `
                        <p><strong>比賽日期:</strong> ${formattedDate}</p>
                        <p><strong>主場隊伍:</strong> ${game.home_team} (${game.home_score})</p>
                        <p><strong>客場隊伍:</strong> ${game.away_team} (${game.away_score})</p>
                        <p><strong>MVP:</strong> ${game.mvp_player || "無"}</p>
                        <p><strong>game_number:</strong> ${game.game_number}</p>
                    `;

                    // 添加刪除按鈕
                    const deleteButton = document.createElement("button");
                    deleteButton.textContent = "刪除比賽";
                    deleteButton.className = "delete-button";
                    deleteButton.dataset.gameDate = formattedDate; // 添加 game_date
                    deleteButton.dataset.gameNumber = game.game_number; // 添加 game_number

                    // 刪除按鈕事件
                    deleteButton.addEventListener("click", () => {
                        const gameDate = deleteButton.dataset.gameDate;
                        const gameNumber = deleteButton.dataset.gameNumber;

                        // 發送刪除請求到後端
                        fetch('http://127.0.0.1:5000/delete_game', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ game_date: gameDate, game_number: gameNumber }),
                        })

                        .then((response) => response.json())
                        .then((data) => {
                            if (data.error) {
                                alert(`錯誤: ${data.error}`);
                            } else {
                                alert(`刪除成功: ${data.message}`);
                                // 移除該比賽卡片
                                resultContainer.removeChild(gameCard);
                            }
                        })
                        .catch((error) => {
                            console.error('錯誤:', error);
                            alert('請求失敗，請檢查伺服器是否正在運行。');
                        });
                    });

                    // 將按鈕添加到卡片
                    gameCard.appendChild(deleteButton);

                    // 將卡片添加到結果容器
                    resultContainer.appendChild(gameCard);
                });
            }
        })
        .catch(error => {
            console.error('錯誤:', error);
            alert('請求失敗，請檢查伺服器是否正在運行。');
        });

        document.body.removeChild(dialog); // 關閉對話框
    });

    const cancelButton = document.createElement("button");
    cancelButton.textContent = "取消";
    cancelButton.addEventListener("click", function () {
        document.body.removeChild(dialog); // 關閉對話框
    });

    dialog.appendChild(submitButton);
    dialog.appendChild(cancelButton);

    document.body.appendChild(dialog);
});