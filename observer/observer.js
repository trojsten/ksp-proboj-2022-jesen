
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
    "#000000",
    "#a8a8a8",
    "#e3e3e3",
    "#298c22",
    "#0eb0cc",
    "#9a9a9a",
]

function renderFrame(f) {
    const frame = OBSLINES[f]
    CTX.clearRect(-GRID, -GRID, CANVAS.width+GRID, CANVAS.height+GRID);

    for (let y = 0; y < frame.world.height; y++) {
        for (let x = 0; x < frame.world.width; x++) {
            const tile = frame.world.tiles[y][x]
            const type = tile[0]
            if (type === 0) {
                continue
            }
            CTX.beginPath()
            CTX.fillStyle = TileColors[type]
            CTX.rect(x * GRID, y * GRID, GRID, GRID)
            CTX.fill()
        }
    }

    for (let y = 0; y < frame.world.height; y++) {
        for (let x = 0; x < frame.world.width; x++) {
            CTX.beginPath()
            const transparency = 255 - (255 / 15) * frame.world.oxygen[y][x]
            let hex = transparency.toString(16)
            hex = hex.length === 1 ? '0' + hex : hex
            CTX.fillStyle = "#000000" + hex
            CTX.rect(x * GRID, y * GRID, GRID, GRID)
            CTX.fill()
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

            CTX.beginPath()
            CTX.fillStyle = "#" + player.color
            CTX.rect(lemur.position.x * GRID, lemur.position.y * GRID, GRID, GRID)
            CTX.fill()
        }
    }


    renderPlayers(f)
}
