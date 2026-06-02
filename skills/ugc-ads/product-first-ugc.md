# Product-First UGC Ad

> Loaded by the `ugc-ads` skill when the user wants a **Product-First** ad.
> The `ugc-ads` CORE RULE still applies: **ask before you create.**

## What this is
The ad is **100% about the product**. Product-First has several **production formats** that share the same brand voice, output format, and approval gate — they differ only in how they're shot/edited:

| Format | Name | What it is | Engine |
|--------|------|-----------|--------|
| **A.1** | Talking Head | Creator talks straight to camera about the product | Talking-head avatar tool (e.g. Higgsfield Marketing Studio: avatar + product + TTS lip-sync) |
| **A.2** | Split-Screen Edit | Music-driven product-flex montage in stacked split panels (no talking) | Reference-driven video model (e.g. Seedance 2.0), image refs |
| **A.3** | Product Modelling | Product worn/used on a model, motion/showcase emphasis | TBD |

Confirm which format before generating.

---

# A.1 — Talking Head

## Output format (always)
Numbered segments. Each segment = one generation (≤15s on most tools). For each:
```
### Segment N — (0–15s)
SPOKEN (VO): "<spoken line, ≤~38 words for 15s, natural pace>"
ON-SCREEN VISUAL (SLCT):
  • Subject — who/what is in frame, action, expression
  • Lighting/Look — natural/phone-quality, "not studio-perfect"
  • Camera — selfie / handheld / medium shot
  • Technical — 9:16 vertical, authentic UGC not polished commercial
ON-SCREEN CAPTION (optional)
```

## Default = 15s (single segment)
- **0–3s Hook** · **3–11s product + ONE benefit** · **11–15s CTA**
- **Word budget ≈ 38 words / 15s** or text-to-speech speeds the audio up.

## Scaling to 30s / 60s
Most tools cap a clip at ~15s → **segment & stitch** (keep the same avatar + product across segments; optionally hide joins with product B-roll).

## Generic creative rules (adapt to your brand)
1. **One core benefit** — don't list five features.
2. **Specific > generic** — concrete claims beat vague ones.
3. **Show the product in use**, not just held up.
4. **Talk like a person**, first-person.
5. **Authentic look** — real room, phone light, handheld. The moment it looks like a TVC, it dies.
6. **Compliance** — only claims the brand approved.

## Voice / language tips (learned, brand-agnostic)
- **Match the audience's language** (e.g. a Hindi+English "Hinglish" mix). For mixed-language VO, the foreign-language words are usually fine; **the OTHER language's words + your brand name are the pronunciation risk** in text-to-speech.
- **Spell the brand name the way it should sound** (e.g. split a compound brand into two words) so the TTS says it correctly. Phonetically respell any word that mis-renders; drop words that won't.
- **Positioning words matter** — pick the framing the brand wants (e.g. "premium / affordable / value"), avoid framings it doesn't (e.g. "cheap").
- **Don't recite the full SKU / spec dump** — keep it short, casual, Gen-Z.
- **Add a relatable, believable use-case** (weather, commute, a daily annoyance the product fixes).
- Keep a strong hook + a clear CTA (app / link / store).

---

# A.2 — Split-Screen Edit

A **music-driven product-flex montage** in a stacked split-screen layout. **No talking / no VO / no lip-sync** — visual flex cut to music, with an optional CTA text card at the end. Two common variants:
- **2-split (studio beauty):** TOP = a model wearing the product, flex poses in a clean studio; BOTTOM = the product rotating in-hand on a neutral background.
- **3-split (outdoor lifestyle):** TOP = model walking outdoors wearing it; MIDDLE = POV hand holding the product; BOTTOM = wide tracking shot of the model.

## A.2 engine & recipe (reference-driven model, e.g. Seedance 2.0)
- **Image references ONLY**: `image` = a model still (a bare-faced fashion model so the product can be placed on them) + `image` = a clean product shot.
- **Describe the split IN THE PROMPT** — *not* via a video reference. Template: *"Vertical 9:16 video split into TWO/THREE equal stacked horizontal panels with thin dividing lines, all panels visible the entire time. TOP PANEL: … MIDDLE/BOTTOM PANEL: … Keep the face identical to the reference and the product identical to the product image."*
- **Clean-start fix for 3-split:** add *"the panels are SEPARATE shots locked from the VERY FIRST FRAME; no person/object ever spans/crosses between panels"* — else the opening frame bleeds one subject across bands.
- Params: 9:16, 720p, 15s, standard mode.

## A.2 hard-won gotchas (model-agnostic, learned the hard way)
- Some reference-driven models, **via an MCP/tool integration, accept IMAGE references only** — a **`video` reference** (to copy a reference edit) and an **`audio` reference** (to bake in music) may silently **fail**. Test image-only first.
- ⇒ **Treat music as a POST step.** Generate silent, stitch the track in post. Many gen models won't synthesize/attach licensed music anyway.
- The tool may pop a **preset recommendation** — decline it and generate literally.
- Busy queues: renders can sit for minutes; **failed jobs usually aren't charged** (verify with a balance check).

## A.2 models (new fashion identities)
- Mint with an **image model** (e.g. Nano Banana Pro), **bare-faced** portraits so the gen model places the real product on them — NOT your talking-head avatars.
- You can seed new models from face/body **reference images** (upload → pass as an `image` ref; prompt "a NEW distinct individual inspired by the reference aesthetic"). Be deliberate about skin tone / styling — models often default to a narrow look without strong prompting + a reference. **Do not replicate real, identifiable people.** Keep a reusable model library.

## A.2 brand rules
Same brand-voice rules apply to **any on-screen text / CTA card** (added in post).

---

# A.3 — Product Modelling

Cinematic **beauty/fashion showcase of the product worn on a model** — direct-to-camera, the signature "hands adjusting the product" gesture + subtle head turns. No talking; music + caption in post. Useful sub-formats (mirror whatever references you're replicating):
- **Indoor multi-frame** — model in a store/home trying on variants, head turns to show angles (try-on feel).
- **Outdoor cinematic jump-cuts** — single model outdoors flexing one variant, hard jump-cuts between distinct poses.
- **Studio portrait** — premium studio, tight head-and-shoulders, elegant poses.

## A.3 engine & recipe (reference-driven model, image refs — FULL-FRAME)
- Same image-refs approach as A.2 but **full-frame, no split panels**: `image` = model still + `image` = product image. Describe the sub-format + motion in the prompt.
- ⚠️ If your video tool was given a product through a separate "product entity" step, still pass the **product IMAGE id**, not the entity id, as the reference — entity ids can fail with "media input not found".
- Params: 9:16, 720p, 15s.

## A.3 gotcha — safety-filter false positives
Some models' NSFW filters false-positive on **full-body "studio shoot / standing / posing model"** framing (especially youthful-looking models) — the job returns a safety-block status. **Fix:** use **tight close-up / head-and-shoulders framing** + modest, product-led wording (e.g. "eyewear product-campaign portrait, fully-clothed, elegant"); avoid words like "shoot / full-body / posing". Tight close-ups generally pass first try.

*Replicating a reference (e.g. a Pinterest clip)? Match its framing and motion, but generate brand-new model identities — don't reproduce real, identifiable people.*

---

## Process — SCRIPT/STORYBOARD APPROVAL GATE
Show the script (A.1) or the shot plan (A.2/A.3) to the user and get approval before generating any video.

*Living file — update with the hooks, angles, formats, and voice rules that convert for your brand.*
