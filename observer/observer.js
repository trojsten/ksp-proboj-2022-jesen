
function renderPlayers(f) {
    document.getElementById("players").innerHTML = ''
    const frame = OBSLINES[f]
    for (const player of frame.players) {
        document.getElementById("players").innerHTML += `
            <div class="player ${player.alive ? '' : 'player-dead'}">
                <div class="player-color" style="background: #${player.color}"></div>
                <div class="player-name">${player.display_name}</div>
                <div class="player-score">${frame.scores[player.name]}</div>
            </div>`
    }
}

const TileColors = [
    "#4d4d4d",
    "#a8a8a8",
    "#d29b75",
    "#298c22",
    "#0eb0cc",
    "#9a9a9a",
]

function square(x, y, color) {
    CTX.beginPath()
    CTX.fillStyle = color
    CTX.lineWidth = 1;
    CTX.fillRect(x * GRID, y * GRID, GRID, GRID)
}

function renderFrame(f) {
    const frame = OBSLINES[f]
    CTX.clearRect(-GRID, -GRID, CANVAS.width+GRID, CANVAS.height+GRID);
    CTX.fillStyle = "#000000"
    CTX.fillRect(-GRID, -GRID, CANVAS.width+GRID, CANVAS.height+GRID);

    for (let y = 0; y < frame.world.height; y++) {
        for (let x = 0; x < frame.world.width; x++) {
            const tile = frame.world.tiles[y][x]
            const type = tile[0]
            square(x, y, TileColors[type])
        }
    }

    for (let y = 0; y < frame.world.height; y++) {
        for (let x = 0; x < frame.world.width; x++) {
            const minT = 0.9
            const transparency = minT - (minT / 15) * frame.world.oxygen[y][x]
            square(x, y, "rgba(0,0,0,"+transparency+")")
        }
    }

    for (const player of frame.players) {
        if (!player.alive) {
            continue
        }

        for (const lemur of player.lemurs) {
            if (!lemur.alive) {
                continue
            }

            square(lemur.position.x, lemur.position.y, "#" + player.color)
        }
    }


    renderPlayers(f)
}
