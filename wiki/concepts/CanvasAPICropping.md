---
title: "Canvas API Cropping"
type: concept
tags: [api, image-processing, canvas]
sources: ["avatar-crop-js-drag-to-reposition-avatar-upload.md"]
last_updated: 2026-04-08
---

## Definition
Using the HTML5 Canvas API to extract a rectangular sub-region from an image based on coordinates. The `drawImage()` method accepts source coordinates and dimensions to crop during the draw operation.

## Implementation in Avatar Crop
```javascript
function _doCrop(img, offsetX, offsetY, zoneSize, drawW, drawH) {
    const canvas = document.createElement('canvas');
    canvas.width = zoneSize;
    canvas.height = zoneSize;
    const ctx = canvas.getContext('2d');
    // Draw cropped region: source image at (-offsetX, -offsetY) scaled to zoneSize
    ctx.drawImage(img, offsetX, offsetY, drawW, drawH, 0, 0, zoneSize, zoneSize);
    // Export as blob/file
}
```

## Key Parameters
- **Source coords**: (offsetX, offsetY) — where in source image to start
- **Source dimensions**: (drawW, drawH) — how much of source to use
- **Dest coords**: (0, 0) — canvas origin
- **Dest dimensions**: (zoneSize, zoneSize) — output size

## Related Concepts
- [[Image Processing]] — broader category
- [[Blob Conversion]] — canvas.toBlob for file export
