function setupCanvas(canvas) {
    let rect = canvas.getBoundingClientRect()
    canvas.width = rect.width
    canvas.height = rect.height
    let ctx = canvas.getContext('2d')
    return ctx
}

const CANVAS = document.querySelector('.canvas')
const CTX = setupCanvas(CANVAS)
let GRID = 0
let OBSLINES = []
let FRAME = 0
const urlParams = new URLSearchParams(window.location.search)

async function showFile(f) {
    let file = f.files[0]
    let data = await file.arrayBuffer()
    observe(data)
}

function observe(log) {
    log = new Uint8Array(log)
    try {
        log = pako.inflate(log)
        log = new TextDecoder().decode(log)
    } catch (err) {
        alert("error while inflating: " + err)
        return
    }

    lines = log.split("\n")
    OBSLINES = []
    for (let i = 0; i < lines.length; i++) {
        if (!lines[i]) {
            continue
        }
        OBSLINES.push(JSON.parse(lines[i]))
    }

    FRAME = 0
    let frame = OBSLINES[0]
    GRID = Math.min(CANVAS.width / frame.world.width, CANVAS.height / frame.world.height)
    let mapW = frame.world.width * GRID
    let mapH = frame.world.height * GRID

    CTX.translate((CANVAS.width - mapW) / 2, (CANVAS.height - mapH) / 2)
    renderFrame(0)

    if (urlParams.get("autoplay") === "1") {
        PLAYBACK.playing = true
    }
}

let PLAYBACK = {
    playing: false,
    speed: 50
}

document.getElementById("js-frame-prev").addEventListener("click", () => {
    FRAME--
    FRAME = Math.max(FRAME, 0)
    renderFrame(FRAME)
})

document.getElementById("js-frame-next").addEventListener("click", () => {
    FRAME++
    FRAME = Math.min(FRAME, OBSLINES.length - 1)
    renderFrame(FRAME)
})

document.getElementById("js-speed-slower").addEventListener("click", () => {
    PLAYBACK.speed += 20
})

document.getElementById("js-speed-faster").addEventListener("click", () => {
    PLAYBACK.speed -= 20
    PLAYBACK.speed = Math.max(PLAYBACK.speed, 20)
})

document.getElementById("js-play").addEventListener("click", () => {
    PLAYBACK.playing = true
})

document.getElementById("js-pause").addEventListener("click", () => {
    PLAYBACK.playing = false
})

function playTick() {
    if (PLAYBACK.playing) {
        if (FRAME < OBSLINES.length - 1) {
            FRAME++
            renderFrame(FRAME)
        } else {
            PLAYBACK.playing = false

            if (urlParams.get("autoplay") === "1") {
                setTimeout(() => {window.location = "/autoplay/"}, 2500)
            }
        }
    }
    setTimeout(playTick, PLAYBACK.speed)
}

playTick()

if (urlParams.has("file")) {
    document.getElementById("js-file").style.display = "none"

    fetch(urlParams.get("file"))
        .then(res => res.blob())
        .then(blob => blob.arrayBuffer())
        .then(buffer => observe(buffer))
}
