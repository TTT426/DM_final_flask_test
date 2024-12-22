fetch('http://localhost:3000/games') // 傳遞 recent 參數
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // 解析 JSON
  })
  .then(data => {
    console.log(data); // 查看後端返回的數據是否正確
    const allGamesDiv = document.getElementById('allGames');

    // 清空現有的比賽內容（避免多次加載疊加）
    allGamesDiv.innerHTML = '';

    // 遍歷返回的比賽數據
    data.forEach(game => {
      const gameDiv = document.createElement('div');
      gameDiv.classList.add('game');
      gameDiv.setAttribute('data-id', game.id);

      gameDiv.innerHTML = `
        <p class="date">${new Date(game.game_date).toLocaleDateString()}</p>
        <h1 class="score">${game.home_score}</h1>
        <div class="team">
          <img class="logo" src="../picture_repository/team_logo_lions_500x500.png">
          <p class="teamName">${game.home_team}</p>
        </div>
        <h1 class="middle"> / </h1>
        <div class="team">
          <img class="logo" src="../picture_repository/team_logo_lions_500x500.png">
          <p class="teamName">${game.away_team}</p>
        </div>
        <h1 class="score">${game.away_score}</h1>
      `;

      gameDiv.addEventListener('click', () => {
        window.location.href = `../web_page/game_details.html?id=${game.id}`;
      });

      allGamesDiv.appendChild(gameDiv);
    });
  })
  .catch(error => {
    console.error('Error fetching data:', error); // 處理錯誤
  });
