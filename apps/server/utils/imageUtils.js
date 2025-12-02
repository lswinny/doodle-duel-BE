export function bufferToBase64(buffer) {
  if (!buffer) return null;
  return buffer.toString('base64');
}
