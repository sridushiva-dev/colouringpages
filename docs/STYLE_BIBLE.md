# ColourPages Style Bible

Visual and tonal standards for all product lines. Agents must reference this document before generating art or copy.

## Global Rules

1. **Print-safe line art only** — no shading, gradients, halftones, or gray fills
2. **Colorable regions** — enclosed shapes with clear boundaries
3. **Consistent line weight** within each book (±15% tolerance)
4. **Safe zone** — all art and text inside margins defined in `docs/DECISIONS.md`
5. **Original compositions** — landmarks and scenes drawn as original line art

---

## Adult: Serenity

**Mood:** Calm, restorative, spacious  
**Line weight:** 1.5–2.5 pt at print size  
**Detail:** Medium–high; generous negative space  
**Subjects:** Botanicals, ocean, cozy interiors, celestial scenes, slow-living activities  

**Prompt tone:** Gentle, open-ended  
**Example:** *"Color this ocean as if the tide is breathing slowly."*

**Avoid:** Busy clutter, horror motifs, aggressive geometry

---

## Adult: Psychedelia

**Mood:** Trippy, funky, playful surrealism  
**Line weight:** 1.5–3 pt; can vary for emphasis  
**Detail:** Medium–high; flowing organic + geometric fusion  
**Subjects:** Cosmic gardens, melting patterns, neon flora, impossible architecture, funky creatures  

**Prompt tone:** Imaginative, constraint-based  
**Example:** *"Make every petal a different decade of fashion."*

**Avoid:** Explicit drug imagery, offensive symbols, copyrighted characters

---

## Adult: Landmark Remix

**Mood:** Wonder + creative reinterpretation  
**Line weight:** 2–2.5 pt  
**Detail:** Medium; landmark recognizable but stylized  
**Subjects:** Taj Mahal, Eiffel Tower, Colosseum, Petra, Great Wall, etc. (original art)  

**Prompt tone:** "What if…" reimagination  
**Examples:**
- *"Paint the Taj Mahal as if carved from ice."*
- *"Imagine the Colosseum overgrown with jungle vines."*
- *"Show the Eiffel Tower underwater at twilight."*

**Every page includes a printed prompt** in the top banner.

---

## Kids: Sprout (ages 2–4)

**Trim:** 8.5" × 8.5"  
**Line weight:** 4–6 pt (very bold)  
**Objects per page:** 1–3 large simple shapes  
**Prompt tone:** Simple, sensory  
**Example:** *"Name three colors you see."*

---

## Kids: Explorer (ages 4–7)

**Trim:** 8.5" × 8.5"  
**Line weight:** 3–4 pt  
**Objects per page:** Small scenes, 3–6 elements  
**Prompt tone:** Playful, curious  
**Example:** *"What sound does this animal make?"*

---

## Kids: Creator (ages 7–10)

**Trim:** 8.5" × 11"  
**Line weight:** 2–3 pt  
**Objects per page:** Detailed scenes, narratives  
**Prompt tone:** Story-building  
**Example:** *"Invent a backstory for this character."*

---

## Cover Standards

- Title: large, readable, line-friendly typography
- Subtitle: product line + theme
- Back cover: QR code (bottom-right safe zone), imprint name, optional blurb
- No bleed unless explicitly enabled for a title

---

## Reference Lock Process

1. Creative Director generates 3 style candidates for a book
2. Human approves one in Control Center
3. Approved reference saved as `art/reference.png`
4. All page generation uses that reference for consistency
