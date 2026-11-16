# logicanimated — production settings (Ryan-tuned, Nov 15, 2026)

The standing recipe for every video unless Ryan changes it. Copy of this file lives in the repo root.

## Format
- 1080×1920 portrait Short (9:16), Manim `-qm --resolution 1080,1920`
- Manim frame: `config.frame_width = 4.5`, `config.frame_height = 8.0`
- Palette: ink #e8eef5, mute #9fb4c8, gold #e8b64c, hole fill #22354d, hole edge #7fa6c9, soft red #e08a8a, black background

## Safe zones (Ryan's phone rule — see SAFE_ZONES.md)
- Critical content ONLY inside x ±1.7, y −2.3…+3.2 of the Manim frame
- Wide visuals ≤3.4 units wide, centered; nothing essential in the bottom ~410px or top ~190px
- Verify one frame per scene against the safe box before upload

## Narration
- Kokoro TTS, voice `am_michael`, speed 1.0 (local model, ~/workspace/binary-search-animation/)
- One Manim scene per narration segment, each scene padded to its measured segment length (segment-locked); 0.4s pauses between segments
- Narration normalized to −1.5 dB peak

## Audio mix (mix_audio.py) — FINAL TUNED SETTINGS
- **Music bed: "Vibing Over Venus" by Kevin MacLeod** (music/bed-vibing-over-venus.mp3, CC BY 4.0)
- **Bed gain: −10 dB** (Ryan-tuned Nov 15, 2026: −24 dB was inaudible — measured −43 dB in pauses; −13 audible; −10 is the pick → bed ≈ −29 dB in narration pauses, ~7 dB under the voice)
- Bed fades: 1.5s in, 2.5s out; trimmed to video length
- **NO sound effects** (standing rule, Ryan, Nov 15, 2026 — cues were built and aligned, then removed at his direction; Kenney core set stays in sfx/ unused)
- Limiter 0.89 on the sum; output AAC 192k, 48 kHz
- ALWAYS verify a narration-pause window with volumedetect before delivering a mix

## Upload checklist
- Title, description, tags from the video's script.md
- **Description MUST include the CC BY credit line for the current bed** (see music/LICENSE.md):
  "Vibing Over Venus" Kevin MacLeod (incompetech.com) / Licensed under Creative Commons: By Attribution 4.0 License / http://creativecommons.org/licenses/by/4.0/
- Audience: Not made for kids; visibility: Public; no custom thumbnail (no phone verification on the account)

## Repo
- github.com/Ryansmuse/logicanimated — one folder per video under videos/NNN-slug/ (script.md, src/, audio/, final MP4)
- Files >~1 MB go in via GitHub web upload (git push dies on the proxy); small files push normally
