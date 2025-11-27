import { generateRoomCode } from "./utils/roomCode.js";

// "MODEL" (rather than "Controller" - socket-handler)
export const rooms = {};

export function createRoom(roomCode, hostId) {
    rooms[roomCode] = {
        host: hostId,
        players: {},    //{socketId: {nickname}}
        submissions: []
    };
}

export function joinRoom(roomCode, socketId, nickname){
    if (!rooms[roomCode]) return false;

    rooms[roomCode].players[socketId] = {nickname};
    return true;
}

export function leaveRoom(roomCode, socketId){
    if (!rooms[roomCode]) return;
    
    delete rooms[roomCode].players[socketId];

    //remove room if empty
    if (Object.keys(rooms[roomCode].players).length === 0) {
        delete rooms[roomCode];
    }
}