// io (server side)

// Broadcast to everyone
// Send to a room
// Manage all connections
// Check who’s connected

const http = require('http');
const { Server } = require('socket.io');
const app = require('./app');
const registerHandlers = require("./socket-handlers")

const server = http.createServer(app);

const io = new Server(server, {
  cors: {
    origin: 'http://localhost:5173',
  },
});

io.on('connection', (socket) => {
  console.log('A user connected', socket.id);
  registerHandlers(io, socket);
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
