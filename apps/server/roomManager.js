import { generateRoomCode } from "./utils/roomCode.js";

// "MODEL" (rather than "Controller" - socket-handler)
export const rooms = {};

export function createRoom(roomCode, hostId, nickname) {
    rooms[roomCode] = {
        host: hostId,
        players: {},    //{socketId: {nickname}}
        submissions: []
    };
}

export function joinRoom(roomCode, socketId, nickname){
    const room = rooms[roomCode]
  if (!room) return;
  room.players[socketId] = { nickname };
}

export function leaveRoom(roomCode, socketId){
    const room = rooms[roomCode];
    if (!rooms) return;
    delete rooms.players[socketId];

    //remove room if empty
    if (Object.keys(rooms[roomCode].players).length === 0) {
        delete rooms[roomCode];
    }
}