function binaryToBase64(imageData) {
  // Node Buffer
  if (Buffer.isBuffer(imageData)) {
    return imageData.toString('base64');
  }

  if (imageData instanceof Uint8Array) {
    return Buffer.from(imageData).toString('base64');
  }

  if (Array.isArray(imageData)) {
    return Buffer.from(imageData).toString('base64');
  }

  if (typeof imageData === 'string') {
    return imageData;
  }

  throw new Error('Unsupported image data type for conversion to Base64');
}

export default binaryToBase64;
