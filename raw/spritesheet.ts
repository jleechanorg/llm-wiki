/**
 * Sprite Sheet Renderer for WorldAI Claw
 *
 * Extends the existing Renderer to support sprite sheets with:
 * - Multiple animation frames
 * - Directional variants
 * - Sprite sheet loading from images or generated data
 */

import { TileMap } from '../tilemap/TileMap';

export type HTMLCanvasMockType = any;

export interface SpriteFrame {
  x: number;        // X position in sprite sheet
  y: number;        // Y position in sprite sheet
  width: number;    // Frame width
  height: number;   // Frame height
}

export interface SpriteAnimation {
  name: string;
  frames: SpriteFrame[];
  durationMs: number;     // Total animation duration
  loop: boolean;
}

export interface SpriteSheet {
  imageData: string | HTMLImageElement;  // Base64 or loaded image
  frameWidth: number;
  frameHeight: number;
  animations: Map<string, SpriteAnimation>;
}

export class SpriteSheetRenderer {
  private spriteSheets: Map<string, SpriteSheet> = new Map();
  private loadedImages: Map<string, HTMLImageElement> = new Map();
  private context: CanvasRenderingContext2D;
  private canvas: HTMLCanvasElement | HTMLCanvasMockType;

  constructor(canvas: HTMLCanvasElement | HTMLCanvasMockType) {
    this.canvas = canvas;
    const ctx = this.canvas.getContext('2d');
    if (!ctx) {
      throw new Error('Unable to obtain 2D canvas context');
    }
    this.context = ctx;
  }

  /**
   * Load a sprite sheet from a base64 or URL source
   */
  async loadSpriteSheet(
    id: string,
    source: string,
    frameWidth: number,
    frameHeight: number,
    animations: Array<{ name: string; row: number; frameCount: number; durationMs: number; loop?: boolean }>
  ): Promise<void> {
    const image = await this.loadImage(source);
    this.loadedImages.set(id, image);

    const spriteSheet: SpriteSheet = {
      imageData: image,
      frameWidth,
      frameHeight,
      animations: new Map(),
    };

    // Build animations from sprite sheet layout
    for (const anim of animations) {
      const frames: SpriteFrame[] = [];
      for (let i = 0; i < anim.frameCount; i++) {
        frames.push({
          x: i * frameWidth,
          y: anim.row * frameHeight,
          width: frameWidth,
          height: frameHeight,
        });
      }
      spriteSheet.animations.set(anim.name, {
        name: anim.name,
        frames,
        durationMs: anim.durationMs,
        loop: anim.loop ?? true,
      });
    }

    this.spriteSheets.set(id, spriteSheet);
  }

  /**
   * Register a procedurally generated sprite sheet
   */
  registerSpriteSheet(id: string, spriteSheet: SpriteSheet): void {
    this.spriteSheets.set(id, spriteSheet);
  }

  /**
   * Draw an animated sprite at the given position
   */
  drawAnimatedSprite(
    spriteId: string,
    animationName: string,
    x: number,
    y: number,
    elapsedTimeMs: number,
    flipX: boolean = false,
    scale: number = 1
  ): void {
    const spriteSheet = this.spriteSheets.get(spriteId);
    if (!spriteSheet) {
      console.warn(`[SpriteSheetRenderer] Sprite sheet not found: ${spriteId}`);
      return;
    }

    const animation = spriteSheet.animations.get(animationName);
    if (!animation) {
      console.warn(`[SpriteSheetRenderer] Animation not found: ${animationName}`);
      return;
    }

    // Calculate current frame
    const frameDuration = animation.durationMs / animation.frames.length;
    const frameIndex = Math.floor(elapsedTimeMs / frameDuration) % animation.frames.length;
    const frame = animation.frames[frameIndex];

    // Draw the frame
    this.context.save();

    if (flipX) {
      this.context.scale(-scale, scale);
      this.context.drawImage(
        spriteSheet.imageData as HTMLImageElement,
        frame.x, frame.y, frame.width, frame.height,
        -x * scale - frame.width * scale, y * scale,
        frame.width * scale, frame.height * scale
      );
    } else {
      this.context.drawImage(
        spriteSheet.imageData as HTMLImageElement,
        frame.x, frame.y, frame.width, frame.height,
        x * scale, y * scale,
        frame.width * scale, frame.height * scale
      );
    }

    this.context.restore();
  }

  /**
   * Draw a static sprite frame
   */
  drawSprite(
    spriteId: string,
    frameX: number,
    frameY: number,
    x: number,
    y: number,
    scale: number = 1
  ): void {
    const spriteSheet = this.spriteSheets.get(spriteId);
    if (!spriteSheet || !spriteSheet.imageData) {
      return;
    }

    const frameWidth = spriteSheet.frameWidth;
    const frameHeight = spriteSheet.frameHeight;

    this.context.drawImage(
      spriteSheet.imageData as HTMLImageElement,
      frameX * frameWidth, frameY * frameHeight,
      frameWidth, frameHeight,
      x, y,
      frameWidth * scale, frameHeight * scale
    );
  }

  private loadImage(source: string): Promise<HTMLImageElement> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;

      if (source.startsWith('data:')) {
        img.src = source;
      } else {
        img.src = source;
      }
    });
  }

  /**
   * Get a sprite sheet by ID
   */
  getSpriteSheet(id: string): SpriteSheet | undefined {
    return this.spriteSheets.get(id);
  }
}

/**
 * Procedural sprite generation for when AI generation is not available
 * Creates pixel art sprites programmatically
 */
export class ProceduralSpriteGenerator {
  private canvas: OffscreenCanvas;
  private ctx: OffscreenCanvasRenderingContext2D;

  constructor(width: number, height: number) {
    this.canvas = new OffscreenCanvas(width, height);
    this.ctx = this.canvas.getContext('2d')!;
  }

  /**
   * Generate a simple character sprite
   */
  generateCharacterSprite(options: {
    bodyColor: string;
    accentColor: string;
    skinColor: string;
    hasHelmet: boolean;
    hasSword: boolean;
    direction: 'north' | 'south' | 'east' | 'west';
  }): ImageData {
    const { width, height } = this.canvas;
    const imageData = this.ctx.createImageData(width, height);
    const data = imageData.data;

    const clearPixel = (x: number, y: number) => {
      const idx = (y * width + x) * 4;
      data[idx] = 0; data[idx + 1] = 0; data[idx + 2] = 0; data[idx + 3] = 0;
    };

    const setPixel = (x: number, y: number, color: string) => {
      if (x < 0 || x >= width || y < 0 || y >= height) return;
      const idx = (y * width + x) * 4;
      const rgb = this.hexToRgb(color);
      data[idx] = rgb.r; data[idx + 1] = rgb.g; data[idx + 2] = rgb.b; data[idx + 3] = 255;
    };

    const drawRect = (x: number, y: number, w: number, h: number, color: string) => {
      for (let dy = 0; dy < h; dy++) {
        for (let dx = 0; dx < w; dx++) {
          setPixel(x + dx, y + dy, color);
        }
      }
    };

    // Center position
    const cx = Math.floor(width / 2);
    const cy = Math.floor(height / 2);

    // Draw based on direction
    if (options.direction === 'south') {
      // Head
      drawRect(cx - 4, cy - 12, 8, 8, options.skinColor);
      // Eyes
      setPixel(cx - 2, cy - 10, '#000000');
      setPixel(cx + 2, cy - 10, '#000000');
      // Body
      drawRect(cx - 5, cy - 4, 10, 10, options.bodyColor);
      // Arms
      drawRect(cx - 8, cy - 4, 3, 8, options.skinColor);
      drawRect(cx + 5, cy - 4, 3, 8, options.skinColor);
      // Legs
      drawRect(cx - 4, cy + 6, 3, 6, options.accentColor);
      drawRect(cx + 1, cy + 6, 3, 6, options.accentColor);
      // Helmet
      if (options.hasHelmet) {
        drawRect(cx - 5, cy - 14, 10, 4, options.accentColor);
      }
      // Sword
      if (options.hasSword) {
        drawRect(cx + 9, cy - 8, 2, 10, '#c0c0c0');
        drawRect(cx + 8, cy - 2, 4, 2, '#ffd700');
      }
    }

    return imageData;
  }

  /**
   * Generate walk cycle frames
   */
  generateWalkCycle(frameCount: number, options: {
    bodyColor: string;
    accentColor: string;
    skinColor: string;
  }): ImageData[] {
    const frames: ImageData[] = [];
    const gen = new ProceduralSpriteGenerator(32, 48);

    for (let i = 0; i < frameCount; i++) {
      const frame = gen.generateCharacterSprite({
        ...options,
        hasHelmet: true,
        hasSword: true,
        direction: 'south',
      });
      frames.push(frame);
    }

    return frames;
  }

  /**
   * Convert sprite frames to a sprite sheet image
   */
  framesToSpriteSheet(frames: ImageData[], frameWidth: number, frameHeight: number): ImageData {
    const sheetWidth = frameWidth * frames.length;
    const sheetHeight = frameHeight;
    const sheet = new ImageData(sheetWidth, sheetHeight);

    for (let i = 0; i < frames.length; i++) {
      const frame = frames[i];
      for (let y = 0; y < frameHeight && y < frame.height; y++) {
        for (let x = 0; x < frameWidth && x < frame.width; x++) {
          const srcIdx = (y * frame.width + x) * 4;
          const dstIdx = (y * sheetWidth + i * frameWidth + x) * 4;
          sheet.data[dstIdx] = frame.data[srcIdx];
          sheet.data[dstIdx + 1] = frame.data[srcIdx + 1];
          sheet.data[dstIdx + 2] = frame.data[srcIdx + 2];
          sheet.data[dstIdx + 3] = frame.data[srcIdx + 3];
        }
      }
    }

    return sheet;
  }

  private hexToRgb(hex: string): { r: number; g: number; b: number } {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16),
    } : { r: 0, g: 0, b: 0 };
  }

  /**
   * Get the generated image as a data URL
   */
  toDataURL(): string {
    return this.canvas.convertToBlob().then(blob => {
      return new Promise<string>((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result as string);
        reader.readAsDataURL(blob);
      });
    }) as unknown as string;
  }
}
