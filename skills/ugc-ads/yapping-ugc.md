# Yapping UGC Ad

> Loaded by the `ugc-ads` skill when the user wants a **Yapping** ad.
> The `ugc-ads` CORE RULE still applies: **ask before you create.** Do not produce a script/visual until the brief questions are answered.

## What this is

The creator is **storytelling / rambling about something relatable and random** — a day, a thought, a hot take, a mini-story — and then **pivots to the product out of nowhere**. The yap earns attention; the product lands as a casual aside, not a pitch. The unexpected pivot is the whole signature.

**Primary model: Seedance 2.0** (reference-driven, consistent identity, start/end frames).

---

## Output format (always)

Delivered as **numbered segments**. Each segment = one Seedance 2.0 generation (≤15s). For each, output **both**:

```
### Segment N — (0–15s)
SPOKEN (VO): "<spoken line, ≤38 words, natural pace, conversational>"

ON-SCREEN VISUAL (SLCT):
  • Subject — creator mid-yap, natural gestures, real expression
  • Lighting/Look — natural/phone-quality, warm, "not studio-perfect"
  • Camera — selfie / handheld, slight shake, talking to camera
  • Technical — 9:16 vertical, 15s, authentic UGC not polished commercial

ON-SCREEN CAPTION (optional): "<short text overlay>"

SEEDANCE 2.0: reference image [same creator]; start_image / end_image [for chaining]; audio ref [optional]
```

---

## Default = 15s (single segment)

Structure the one 15s block as:
- **0–8s — The yap:** relatable story/topic that makes them go "that's me." No product yet. This is the hook and the body.
- **8–12s — The pivot:** swing to the product *out of nowhere* — "anyway, this is the only thing that…" Feels offhand, not salesy.
- **12–15s — Soft CTA:** low-pressure ("you'll thank me", "it's linked").

**Word budget: ≤38 words total** for a 15s segment, or speech gets sped up. Count the words.

## Scaling to 30s / 60s

Seedance caps every clip at 15s. **Segment and stitch**:
- 30s = 2 segments · 60s = ~4 segments (~150 words total). Longer yaps can afford a slower-burn pivot.
- Keep the **same creator** by passing the **same reference image** to every segment (Seedance "consistent identity").
- Chain for seamless joins: **end_image of segment N = start_image of segment N+1**.
- Stitch in CapCut / Premiere / ffmpeg.

---

## Rules for Yapping

1. **The yap must be genuinely watchable on its own** — relatable, funny, or intriguing. If the story is boring, the ad fails before the pivot.
2. **The pivot is abrupt on purpose.** Don't telegraph it. The charm is the swerve.
3. **Product mention stays casual** — one natural line, not a feature dump. The yap is 70%, the product is 30%.
4. **First-person, unscripted feel.** Filler words and tangents are fine — that's what makes it real.
5. **Authentic look** — real setting, phone-quality light, handheld, talking to camera.
6. **Compliance** — only approved claims, even in an offhand line.

## Seedance 2.0 production notes

- Feed a **reference image** of the creator for identity consistency across segments.
- Use **start_image/end_image** roles to chain segments seamlessly.
- Optional **audio reference** to drive natural delivery.
- 9:16 vertical, sound-on, captions burned in.

*Living file — update with yap formats, pivot lines, and hooks that perform.*
