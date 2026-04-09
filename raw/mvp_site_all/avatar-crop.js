/**
 * avatar-crop.js — Shared drag-to-reposition crop UI for avatar uploads.
 *
 * Usage:
 *   // Show crop UI inside a container element:
 *   window.AvatarCrop.show(containerEl, imageSrc, { size: 280 });
 *
 *   // Get the cropped file:
 *   const file = window.AvatarCrop.getCroppedFile();
 *
 *   // Cleanup:
 *   window.AvatarCrop.destroy();
 */
(() => {
    'use strict';

    let _currentCleanup = null;
    let _currentCroppedFile = null;
    let _currentCroppedUrl = null;
    let _sessionId = 0; // Guard against stale img.onload callbacks

    /**
     * Show a drag-to-reposition crop UI inside a container element.
     * Auto-destroys any previous session first.
     * @param {HTMLElement} container - The element to render crop UI into.
     * @param {string} imageSrc - Data URL or URL of the image to crop.
     * @param {Object} [opts] - Options: { size: number (default 280) }
     */
    function show(container, imageSrc, opts = {}) {
        const zoneSize = opts.size || container.offsetWidth || 280;

        // Clean up any previous crop session
        destroy();

        // Increment session so stale img.onload callbacks are ignored
        const mySession = ++_sessionId;

        // Remove old crop container if any
        container.querySelector('.avatar-crop-container')?.remove();

        // Create crop container
        const cropEl = document.createElement('div');
        cropEl.className = 'avatar-crop-container';
        cropEl.style.cssText = `
      width:100%;height:100%;position:absolute;top:0;left:0;
      overflow:hidden;border-radius:50%;cursor:grab;touch-action:none;z-index:1;
    `;

        const img = new Image();
        img.onload = () => {
            // Guard: ignore if a newer show() was called while loading
            if (mySession !== _sessionId) return;

            const aspect = img.width / img.height;
            let drawW, drawH;
            if (aspect >= 1) {
                drawH = zoneSize;
                drawW = zoneSize * aspect;
            } else {
                drawW = zoneSize;
                drawH = zoneSize / aspect;
            }

            img.style.cssText = `width:${drawW}px;height:${drawH}px;position:absolute;user-select:none;pointer-events:none;`;
            let offsetX = -(drawW - zoneSize) / 2;
            let offsetY = -(drawH - zoneSize) / 2;
            img.style.left = `${offsetX}px`;
            img.style.top = `${offsetY}px`;
            cropEl.appendChild(img);

            // Drag to reposition
            let dragging = false, startX, startY, startOX, startOY;

            const onPointerDown = (e) => {
                e.preventDefault();
                e.stopPropagation();
                dragging = true;
                startX = e.clientX;
                startY = e.clientY;
                startOX = offsetX;
                startOY = offsetY;
                cropEl.style.cursor = 'grabbing';
            };
            const onPointerMove = (e) => {
                if (!dragging) return;
                e.preventDefault();
                const dx = e.clientX - startX;
                const dy = e.clientY - startY;
                offsetX = Math.min(0, Math.max(-(drawW - zoneSize), startOX + dx));
                offsetY = Math.min(0, Math.max(-(drawH - zoneSize), startOY + dy));
                img.style.left = `${offsetX}px`;
                img.style.top = `${offsetY}px`;
            };
            const onPointerUp = () => {
                if (!dragging) return;
                dragging = false;
                cropEl.style.cursor = 'grab';
                _doCrop(img, offsetX, offsetY, zoneSize, drawW, drawH);
            };

            cropEl.addEventListener('pointerdown', onPointerDown);
            document.addEventListener('pointermove', onPointerMove);
            document.addEventListener('pointerup', onPointerUp);

            _currentCleanup = () => {
                cropEl.removeEventListener('pointerdown', onPointerDown);
                document.removeEventListener('pointermove', onPointerMove);
                document.removeEventListener('pointerup', onPointerUp);
            };

            // Initial crop (center) — synchronous fallback for immediate availability
            _doCrop(img, offsetX, offsetY, zoneSize, drawW, drawH);
        };
        img.src = imageSrc;

        // Add hint text
        const hint = document.createElement('div');
        hint.className = 'avatar-crop-hint';
        hint.textContent = 'Drag to reposition';
        hint.style.cssText = `
      position:absolute;bottom:8px;left:50%;transform:translateX(-50%);
      font-size:0.75rem;color:rgba(255,255,255,0.7);background:rgba(0,0,0,0.5);
      padding:2px 10px;border-radius:12px;z-index:2;pointer-events:none;white-space:nowrap;
    `;
        cropEl.appendChild(hint);
        cropEl.addEventListener('pointerdown', () => { hint.style.display = 'none'; }, { once: true });

        container.appendChild(cropEl);
    }

    /**
     * Crop the visible area to a PNG file and cache it.
     * Uses both toBlob (async, higher quality) and toDataURL (sync, immediate availability).
     */
    function _doCrop(img, offsetX, offsetY, zoneSize, drawW, drawH) {
        const canvas = document.createElement('canvas');
        canvas.width = zoneSize;
        canvas.height = zoneSize;
        const ctx = canvas.getContext('2d');

        const scaleX = img.naturalWidth / drawW;
        const scaleY = img.naturalHeight / drawH;
        const sx = -offsetX * scaleX;
        const sy = -offsetY * scaleY;
        const sSize = zoneSize * scaleX;

        ctx.drawImage(img, sx, sy, sSize, sSize, 0, 0, zoneSize, zoneSize);

        // Synchronous fallback: always set URL immediately so getCroppedFile works
        _currentCroppedUrl = canvas.toDataURL('image/png');

        // Synchronous File from dataURL for immediate getCroppedFile() availability
        try {
            const dataUrl = _currentCroppedUrl;
            const byteString = atob(dataUrl.split(',')[1]);
            const ab = new ArrayBuffer(byteString.length);
            const ia = new Uint8Array(ab);
            for (let i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            _currentCroppedFile = new File([ab], 'avatar-cropped.png', { type: 'image/png' });
        } catch (_e) {
            // Fallback to async toBlob if sync fails
            canvas.toBlob((blob) => {
                if (blob) {
                    _currentCroppedFile = new File([blob], 'avatar-cropped.png', { type: 'image/png' });
                }
            }, 'image/png');
        }
    }

    /**
     * Get the last cropped file (or null).
     */
    function getCroppedFile() {
        return _currentCroppedFile;
    }

    /**
     * Get the last cropped data URL (or null).
     */
    function getCroppedUrl() {
        return _currentCroppedUrl;
    }

    /**
     * Clean up event listeners and state.
     */
    function destroy() {
        _sessionId++;
        if (_currentCleanup) {
            _currentCleanup();
            _currentCleanup = null;
        }
        _currentCroppedFile = null;
        _currentCroppedUrl = null;
    }

    // Expose globally
    window.AvatarCrop = { show, getCroppedFile, getCroppedUrl, destroy };
})();
