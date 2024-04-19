var { SerialPort } = require('serialport');
const express = require('express');
const cors = require('cors');
const morgan = require('morgan')
const app = express();
const PORT = 3000;
app.use(cors());
app.use(morgan('dev'))
app.use(express.json())


var serialPort = new SerialPort( {
    path: "COM8",
    baudRate: 9600
}) 

var ArduinoData = "";

function readSerialData() {
    serialPort.on("open", () => {
        console.log("Serial port is open");
        serialPort.on("data", (data) => {
            console.log("Received data: " + data);
        })
    })
}

app.get('/', (req, res) => {
    res.send("Hello World");
})

app.get('/data', (req, res) => {
    readSerialData()
    res.send("LEIDO")
})

app.listen(PORT, () => {
    console.log(`API Server Listening in http://localhost:${PORT}`)
})