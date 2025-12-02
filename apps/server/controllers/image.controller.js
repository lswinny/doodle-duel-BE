import { bufferToBase64 } from '../utils/imageUtils.js';
import { addSubmission } from '../roomManager.js';
// If later we want to emit to sockets from here, we can import `io`
// from a shared module, e.g. "../shared/io.js" or similar.

// This is the CONTROLLER, called after the middleware has run.
export async function uploadImageController(req, res) {
  try {
    const { socketId, roomCode } = req.body;
    const file = req.file; // set by imageUploadMiddleware

    //Validating the three parameters ----
    if (!socketId || !roomCode || !file) {
      return res.status(400).json({
        message: 'socketId, roomCode and image (file) are required',
      });
    }

    //Converting binary -> base64 using the util
    const base64Image = bufferToBase64(file.buffer);
    if (!base64Image) {
      return res.status(500).json({
        message: 'Could not convert image to base64',
      });
    }

    //Store submission via roomManager (re-use existing logic)
    const ok = addSubmission(roomCode, socketId, base64Image);

    if (!ok) {
      return res.status(404).json({
        message: 'Room not found when submitting drawing',
      });
    }

    //(Optional) Socket emit
    // Example pattern – depends how we choose to share `io`:
    //
    // import { io } from '../shared/io.js';
    // io.to(roomCode).emit('drawing-submitted', { socketId });
    //
    // Note: emitting here notifies other clients; it does NOT trigger
    // the server-side socket.on('submit-drawing') handler.

    //Responding to the HTTP client ----
    return res.status(200).json({
      message: 'Image uploaded and stored successfully',
      roomCode,
      socketId,
    });
  } catch (err) {
    console.error('Error in uploadImageController:', err);
    return res.status(500).json({
      message: 'Internal server error while uploading image',
    });
  }
}
