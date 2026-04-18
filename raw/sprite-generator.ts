/**
 * Sprite Generator Service for WorldAI Claw
 *
 * Generates Chrono Trigger-level 16-bit pixel art sprites using Grok image generation API.
 * Follows worldai_claw CLAUDE.md: must use real LLM API calls, NOT direct OpenAI keys.
 * Uses Grok API (via AI_UNIV_GROK_KEY) through the gateway pattern.
 *
 * Key features:
 * - Character sprite sheets with consistent art style
 * - Animation frames (idle, walk, attack, magic, hurt, death)
 * - Direction variants (4 directions or 8)
 * - Environment tiles and backgrounds
 * - Consistent color palettes
 */

// Environment: Grok API for image generation (via worldai_claw CLAUDE.md pattern)
// Use x.ai API (not api.grok.com) - model is grok-imagine-image
const GROK_API_KEY = process.env.AI_UNIV_GROK_KEY || process.env.GROK_API_KEY;
const GROK_IMAGE_MODEL = process.env.GROK_IMAGE_MODEL || 'grok-imagine-image';

export interface SpriteConfig {
  width: number;           // Sprite width in pixels (e.g., 16, 32, 48)
  height: number;          // Sprite height in pixels (e.g., 16, 32, 48)
  pixelScale: number;      // Scale factor for generation (1x, 2x, 4x)
  frameCount: number;      // Frames per animation
  directions: number;      // 4 or 8 directional sprites
}

export interface CharacterSpriteRequest {
  characterType: 'knight' | 'mage' | 'rogue' | 'beast' | 'boss' | 'npc';
  gender?: 'male' | 'female' | 'neutral';
  colorScheme: string;     // Primary armor/outfit color
  secondaryColor?: string;
  animation: 'idle' | 'walk' | 'attack' | 'magic' | 'hurt' | 'death';
  direction?: 'north' | 'south' | 'east' | 'west';
}

export interface SpriteSheetResult {
  imageData: string;       // Base64 encoded PNG
  styleGuide: SpriteStyleGuide;
  metadata: SpriteMetadata;
}

export interface SpriteStyleGuide {
  palette: string[];       // 16-32 color palette used
  pixelDensity: number;    // Actual pixels per "game pixel"
  borderStyle: string;     // Outline style
  shadingStyle: string;    // Light/shadow approach
}

export interface SpriteMetadata {
  characterType: string;
  animation: string;
  frameCount: number;
  dimensions: { width: number; height: number };
  generatedAt: string;
  styleVersion: string;
}

// Chrono Trigger inspired palettes
export const CHRONO_TRIGGER_PALETTES = {
  knight: {
    primary: ['#1a1a2e', '#16213e', '#0f3460', '#e94560', '#f0f0f0'],
    skin: ['#ffdbac', '#e8b88a', '#c68642', '#8d5524'],
    metal: ['#c0c0c0', '#808080', '#404040', '#ffd700'],
  },
  mage: {
    primary: ['#1a1a2e', '#4a148c', '#7b1fa2', '#e040fb', '#f3e5f5'],
    skin: ['#ffdbac', '#e8b88a', '#c68642', '#8d5524'],
    magic: ['#00bcd4', '#03a9f4', '#2196f3', '#9c27b0'],
  },
  rogue: {
    primary: ['#1a1a2e', '#2d3436', '#636e72', '#b2bec3', '#dfe6e9'],
    skin: ['#ffdbac', '#e8b88a', '#c68642', '#8d5524'],
    accent: ['#00ff00', '#ff6600', '#ffff00'],
  },
  beast: {
    primary: ['#2d3436', '#6c5ce7', '#a29bfe', '#f0f0f0'],
    fur: ['#8b4513', '#a0522d', '#cd853f', '#deb887'],
    eyes: ['#ff0000', '#ffff00', '#00ff00'],
  },
};

// Default sprite configurations
export const SPRITE_CONFIGS: Record<string, SpriteConfig> = {
  tiny: { width: 16, height: 16, pixelScale: 4, frameCount: 4, directions: 4 },
  small: { width: 24, height: 32, pixelScale: 4, frameCount: 4, directions: 4 },
  medium: { width: 32, height: 48, pixelScale: 4, frameCount: 6, directions: 4 },
  large: { width: 48, height: 64, pixelScale: 4, frameCount: 8, directions: 4 },
};

/**
 * System prompt for generating Chrono Trigger style sprites via xAPI
 */
function buildSpritePrompt(request: CharacterSpriteRequest, config: SpriteConfig): string {
  const scale = config.pixelScale;
  const genWidth = config.width * scale;
  const genHeight = config.height * scale;

  const styleInstructions = `
CHRONO TRIGGER PIXEL ART STYLE (SNES 16-bit era):
- Sharp pixel edges, NO anti-aliasing or smoothing
- Limited palette: 16-32 colors max per sprite
- Bold outlines: 1-2 pixels, dark color (#1a1a2e or similar)
- Character sprites: centered, facing viewer for south direction
- Smooth animation frames with clear pose differences
- Expression: 2-3 pixel eyes, simple but expressive
- Shading: hard edge shadows, no gradients
- Magic effects: small particles, glowing cores
- Consistent with classic JRPG sprites (Chrono Trigger, Final Fantasy 6, Earthbound)

COLOR PALETTE: Use the provided color scheme as primary. Include skin tones.

ANIMATION ${request.animation.toUpperCase()}:
- Create ${config.frameCount} frames showing the motion
- Frame timing should be smooth at 200ms per frame
- Clear start and end poses that loop well
`.trim();

  const characterDesc = {
    knight: `Heroic warrior in ${request.colorScheme} armor. Plate armor with detailed helmet, sword at side or raised for attack. Noble bearing.`,
    mage: `Mystical spellcaster in flowing robes. Hood or pointed hat. Glowing ${request.colorScheme || 'purple'} magical aura. Staff in hand.`,
    rogue: `Swift shadow warrior. Light armor in ${request.colorScheme}. Mask or hood. Dual daggers or bow. Sneaky, agile poses.`,
    beast: `Fearsome creature or friendly animal companion. Fur patterns in ${request.colorScheme}. Expressive eyes. Standing on hind legs like bipedal Pokemon.`,
    boss: `Intimidating enemy with dramatic presence. Multiple color accents. Larger than party sprites. Throne or arena pose.`,
    npc: `Friendly village person. Simple ${request.colorScheme} clothing. Open stance. Approachable expression. No weapons.`,
  };

  return `
PIXEL ART GENERATION REQUEST

IMAGE SPECIFICATIONS:
- Format: PNG with transparency
- Size: ${genWidth}x${genHeight} pixels
- Style: ${scale}x scale (each game pixel = ${scale} real pixels)
- Total game sprite size: ${config.width}x${config.height} game pixels

${styleInstructions}

CHARACTER: ${request.characterType}
${characterDesc[request.characterType] || ''}
${request.gender ? `Gender presentation: ${request.gender}` : ''}
Primary Color: ${request.colorScheme}
${request.secondaryColor ? `Secondary Color: ${request.secondaryColor}` : ''}
Animation: ${request.animation}
Direction: ${request.direction || 'south'}

Generate the sprite as a sprite sheet with ${config.frameCount} frames arranged horizontally.
`.trim();
}

/**
 * Sprite Generator using OpenAI DALL-E for actual image generation
 */
export class SpriteGenerator {
  private cache: Map<string, SpriteSheetResult> = new Map();

  constructor() {
    // No client needed - using OpenAI API directly
  }

  /**
   * Generate a character sprite sheet
   */
  async generateCharacterSprite(
    request: CharacterSpriteRequest,
    config: SpriteConfig = SPRITE_CONFIGS.small
  ): Promise<SpriteSheetResult> {
    const cacheKey = this.getCacheKey(request, config);

    // Check cache first
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)!;
    }

    const prompt = buildSpritePrompt(request, config);

    try {
      // Call OpenClaw gateway with image generation request
      // Note: This requires xAPI or image generation model support
      const result = await this.generateWithModel(prompt, config);

      // Cache the result
      this.cache.set(cacheKey, result);

      return result;
    } catch (error) {
      console.error('[SpriteGenerator] Failed to generate sprite:', error);
      throw new Error(`Sprite generation failed: ${error}`);
    }
  }

  /**
   * Generate environment tiles
   */
  async generateTile(
    tileType: 'floor' | 'wall' | 'door' | 'chest' | 'npc' | 'decoration',
    theme: 'dungeon' | 'forest' | 'town' | 'castle' | 'cave',
    palette: string[]
  ): Promise<string> {
    const prompt = `
CHRONO TRIGGER TILE GENERATION

Tile Type: ${tileType}
Theme: ${theme}
Palette: ${palette.join(', ')}

Generate a ${theme} ${tileType} tile at 16x16 game pixels, scaled 4x to 64x64 pixels.
Sharp pixel edges, limited palette, classic SNES style.
Include variations in the tile design.
`.trim();

    const result = await this.generateWithModel(prompt, { width: 16, height: 16, pixelScale: 4, frameCount: 1, directions: 1 });
    return result.imageData;
  }

  /**
   * Generate a full character portrait
   */
  async generatePortrait(
    characterType: string,
    expression: 'neutral' | 'happy' | 'angry' | 'sad' | 'surprised',
    colorScheme: string
  ): Promise<string> {
    const prompt = `
CHRONO TRIGGER PORTRAIT GENERATION

Character: ${characterType}
Expression: ${expression}
Color Scheme: ${colorScheme}

Generate a character portrait at 64x64 game pixels (256x256 scaled 4x).
Classic SNES JRPG portrait style - bust/head and shoulders.
Bold, clean pixel art with the specified expression.
Limited palette of 16-24 colors.
`.trim();

    const result = await this.generateWithModel(prompt, { width: 64, height: 64, pixelScale: 4, frameCount: 1, directions: 1 });
    return result.imageData;
  }

  private async generateWithModel(
    prompt: string,
    config: SpriteConfig
  ): Promise<SpriteSheetResult> {
    // Use Grok API for image generation (following worldai_claw CLAUDE.md pattern)
    if (!GROK_API_KEY) {
      throw new Error('AI_UNIV_GROK_KEY not configured - cannot generate sprites');
    }

    console.log(`[SpriteGenerator] Generating sprite with Grok API`);

    // Grok images API endpoint - note: doesn't support size parameter, returns URL not base64
    const response = await fetch('https://api.x.ai/v1/images/generations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GROK_API_KEY}`,
      },
      body: JSON.stringify({
        model: GROK_IMAGE_MODEL,
        prompt: prompt,
        n: 1,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Grok API error: ${response.status} - ${error}`);
    }

    const data = await response.json() as { data: Array<{ url: string }> };
    const imageUrl = data.data[0]?.url;

    if (!imageUrl) {
      throw new Error('No image URL returned from Grok API');
    }

    // Download the image and convert to base64
    const imageResponse = await fetch(imageUrl);
    const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
    const imageData = imageBuffer.toString('base64');

    // Build style guide based on config
    const styleGuide: SpriteStyleGuide = {
      palette: CHRONO_TRIGGER_PALETTES.knight.primary,
      pixelDensity: config.pixelScale,
      borderStyle: '1-2px dark outline (#1a1a2e)',
      shadingStyle: 'hard edge shadows, no gradients',
    };

    const metadata: SpriteMetadata = {
      characterType: 'generated',
      animation: config.frameCount > 1 ? 'animated' : 'static',
      frameCount: config.frameCount,
      dimensions: { width: config.width * config.pixelScale, height: config.height * config.pixelScale },
      generatedAt: new Date().toISOString(),
      styleVersion: '1.0-grok',
    };

    return {
      imageData: imageData,
      styleGuide,
      metadata,
    };
  }

  private getCacheKey(request: CharacterSpriteRequest, config: SpriteConfig): string {
    return JSON.stringify({ request, config });
  }

  /**
   * Clear the sprite cache
   */
  clearCache(): void {
    this.cache.clear();
  }

  /**
   * Get sprite config by size name
   */
  getConfig(name: keyof typeof SPRITE_CONFIGS): SpriteConfig {
    return SPRITE_CONFIGS[name];
  }
}

// Singleton instance
let spriteGeneratorInstance: SpriteGenerator | null = null;

export function getSpriteGenerator(): SpriteGenerator {
  if (!spriteGeneratorInstance) {
    spriteGeneratorInstance = new SpriteGenerator();
  }
  return spriteGeneratorInstance;
}
