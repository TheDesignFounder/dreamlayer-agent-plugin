---
name: sprite-sheet-from-reference
description: "Turn one character, object or effect reference into an animated sprite-sheet ZIP with transparent PNG frames using DreamLayer. Use for game sprites, walk cycles, idle animations or custom motion within a credit budget."
---

# sprite sheet from reference

Read [the workflow contract](references/workflow-contract.md) for setup, billing, recovery and output checks.

Read the workflow contract, then current sprite_pricing in capabilities. Exactly one reference and one of action (walk/run/idle) or animation_prompt (1–4000 chars) are required. Choose frame_count 7–100 and square frame_size 32,64,128,256,512,720,1080. action defaults to loop; custom animation defaults to once; explicitly set animation_mode when needed. Quote in integer cents: min(n,14)*14 + max(n-14,0)*7, divide by 17 cents per credit, round the WHOLE order upward once to 0.1 credit. Treat these as the current example values, and recompute from live capabilities. 7 frames currently cost 5.8 credits; 12 cost 9.9. Set max_credits within the user's authorized cap. Compare to available balance, not the separately rounded funding buckets. Sprites have no customer cancellation. Save execution and poll/resume; failed/expired work restores the hold. Download .zip, inspect its manifest and preview, and validate frame count/alpha/timing. Do not claim pixel-grid preservation, perfect anatomy, eight directions, editable Aseprite layers or production quality. For engine import use the matching engine skill. CLI: dreamlayer sprite reference.png --action walk --frames 7 --frame-size 128 --max-credits 5.8 --out walk.zip --json

