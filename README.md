# miscritsbotv2 👾  
Automation bot for **Miscrits (PC)** using computer vision + OCR

This project automates repetitive Miscrits gameplay loops (fighting/training/capturing, etc.) using:
- **Template matching** via screenshot images.
- **OCR (Tesseract)** to detect crit name, capture chance%, HP, and tier.
- Human-like mouse movement + configurable logic.
- **Telegram notifications** and **IST timestamped logs**.

---

## Features

### Fight/Training Bot
- Automatically searches for Miscrits and fights repeatedly.
- Reads fight info using OCR:
  - Crit name
  - Capture chance
  - HP
  - Tier (A+, A, S+, etc.)
- Auto-captures based on tier + thresholds.
- Optional **Magical Heal** usage when HP is low.
- Auto-training loop when crits are ready.
- Tracks stats: captured crits, tier stats, tries, level-ups.

### Extras
- **Battle Arena auto-runner** (attack + loop + heal)
- **Breeding helper** (filters miscrits, drags breeders, keeps/releases based on results)
- **Rename helper** (renames crits based on detected stat)

---

## Project Structure
```
miscritsbotv2/
├── photos/    # all template images for UI detection 
│ ├── fight/   # per-miscrit + common fight UI images 
│ ├── tiers/   # tier templates (A+, S+, etc.) 
│ ├── ba/      # battle arena templates
│ ├── breed/   # breeding templates
│ └── rename/  # rename/stat detection templates
├── templates/
│ └── environment/ # tree/grass encounter-object templates
└── scripts/
  ├── run.py            # main fight/training bot runner
  ├── fight.py          # core bot logic + capture rules
  ├── fight_info.py     # OCR + tier detection
  ├── human_mouse.py    # mouse movement + locate helpers
  ├── notifier.py       # Telegram notifications
  ├── logger.py         # IST timestamped log files
  ├── battle_arena.py   # arena automation script
  ├── breed_helper.py   # breeding helper
  └── rename.py         # rename helper
```
---

## Requirements

### OS
- **Windows 10/11**, or **MacOS**

### Python packages
Install dependencies:
```bash
pip install pyautogui pillow pytesseract pytz requests opencv-python numpy
```
## Install Tesseract OCR
Install **Tesseract OCR**.
Default expected path:
```
C:\Program Files\Tesseract-OCR\tesseract.exe
```
If your path differs, update it in:
`scripts/fight_info.py → FightInfo(tesseract_cmd=...)`

---

## Setup before running

Open Miscrits and set:
- Windowed mode or full-screen.
- Keep the whole window visible on screen.

Windows settings:
- Set Display Scale = 100% (important for template matching)
- This bot controls the cursor.

You will get a few seconds in between clicks where you are able to work on something else.

## Running the main bot
### Configuration
Edit `scripts/run.py` to configure behavior:
```bash
bot = MiscritsBot(
  search_crit="geneseed",       # crit to search for (must exist in photos/fight/<crit>/)
  trainer_crit="papa",          # which crit attack button template to use
  heal=False,                   # use Magical Heal if low HP
  plat_training=False,          # enable platinum training clicks
  capture_tiers=["S+", "A+", "A", "B+"],  # tiers to capture
  move_page=1,                  # moves to page 2 if required
  plat_capture_attempts=0       # extra plat capture attempts
)
```
The search_crit must match a folder in:
`photos/fight/<search_crit>/` Example: `photos/fight/geneseed/`

### Environment scanning mode
The current runner enables environment scanning instead of searching for one specific Miscrit. It scans the visible map for the supplied tree/grass templates, interacts with an unchecked object, waits for an encounter, and then hands the encounter to the existing fight/training logic.

Environment templates are stored in `templates/environment/`:
- `tree_01.jpg`
- `tree_02.jpg`
- `grass_01.jpg`
- `grass_02.jpg`

The scan area defaults to the 1366x670 map viewport shown by the supplied game screenshot, leaving the bottom social controls outside the scan. If your game window uses a different resolution, update `scan_region` in `scripts/environment_scanner.py`.

S+ encounters use an HP-first capture rule: the bot attacks while HP is above the configured threshold, then attempts capture. The runner currently uses `s_plus_capture_hp=25` and up to 3 capture attempts.

### Run
From the project root:
```bash
cd scripts
python run.py
```

---

## Telegram notifications
The bot supports Telegram notifications when rare or desired encounters happen.
In `scripts/notifier.py`, set:
- `telegram_token`
- `telegram_chat_id`

Security note: Do not commit your token publicly! Keep a local config.

---

## Logs
Logs are automatically written to:
```bash
logs/run_<IST timestamp>.log
```

---

## Troubleshooting
### Bot can’t detect buttons / clicks wrong areas
- Set Windows display scaling to 100%
- Make sure full Miscrits window is in-view
- Ensure templates in `photos/` match your current game UI
### OCR gives incorrect crit name / capture chance
- Confirm Tesseract installation
- The OCR region may need adjustment in:
`FightInfo.get_capture_chance_crit_name_tier`
