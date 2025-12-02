import multer from 'multer';

// Store uploaded file in memory (no files on disk)
const storage = multer.memoryStorage();

const upload = multer({ storage });

// This is *middleware*, not a controller.
// It parses a single file with field name "image".
export const imageUploadMiddleware = upload.single('image');
