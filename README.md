# Target Sum / 目标求和

A bilingual console number puzzle game written with the Python standard library.

一个使用 Python 标准库编写的双语控制台数字求和小游戏。

## Features / 功能

- Pick numbered values that add up to a target.
- Multiple difficulties with more numbers and harder ranges.
- Hint command reveals one useful index once per round.
- Bilingual UI: English and Chinese.
- Persistent JSON settings and top scores.
- Optional terminal bell sound with adjustable volume.
- Automated tests for core logic, persistence modules, sound, and menu gameplay.

## Requirements / 环境要求

- Python 3.9+
- No third-party dependencies.

## Run / 启动

```bash
python3 game.py
```

## Test / 测试

```bash
python3 -m py_compile game.py target_sum.py i18n.py settings.py score.py sound.py
python3 tests/run_tests.py
```

## How to Play / 玩法

1. Choose Play from the main menu.
2. Read the numbered list and target value.
3. Enter the required number of indices, separated by spaces or commas.
4. The chosen values must sum to the target.
5. Type `hint` once per round to reveal one useful index.
6. Type `q` to quit the current round.

## Difficulty / 难度

| Difficulty | Numbers | Pick | Rounds | Range | Score bonus |
| --- | ---: | ---: | ---: | --- | ---: |
| easy | 5 | 2 | 6 | 1..12 | 1x |
| normal | 6 | 3 | 7 | 1..20 | 2x |
| hard | 7 | 3 | 8 | -5..30 | 3x |

## Files / 文件

- `game.py` — console UI and menus.
- `target_sum.py` — core puzzle, parsing, scoring, and rating logic.
- `i18n.py` — bilingual strings.
- `settings.py` — JSON settings persistence.
- `score.py` — JSON score persistence.
- `sound.py` — terminal bell sound helper.
- `tests/` — automated unit tests.
