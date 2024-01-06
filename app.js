const express = require('express');
const { WebSocketServer } = require('ws');
const mockObjDet = require('./mockObjDet.js');

const PORT = 3000

const app = express();

const server = app.listen(PORT, () => {
    console.log(`Listening on ${PORT}`);
})

const wss = new WebSocketServer({
    server,
    clientTracking: true,
});

wss.on('connection', (ws, req) => {
    const path = req.url;

    if (path === "/object-detection") {
        setInterval(async () => {
            ws.send(JSON.stringify(mockObjDet()))
        }, 66)
    } else {
        console.log(path)
        ws.close();
    }
});