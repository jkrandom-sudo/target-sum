"""Console game for Target Sum."""
import score as score_mod
import settings as settings_mod
import target_sum as core
from i18n import t
from sound import Sound


class QuitGame(Exception):
    pass


def _print(text=""):
    print(text)


def show_header(settings):
    _print("=" * 32)
    _print(t(settings["lang"], "title"))
    _print("=" * 32)


def show_help(settings):
    show_header(settings)
    _print(t(settings["lang"], "help_title"))
    _print(t(settings["lang"], "help_text"))
    input(t(settings["lang"], "press_enter"))


def show_scores(settings):
    show_header(settings)
    _print(t(settings["lang"], "scores"))
    scores = score_mod.load()
    if not scores:
        _print(t(settings["lang"], "no_scores"))
    for idx, item in enumerate(scores, 1):
        _print(f"{idx}. {item.get('name', '?')} {item.get('score', 0)} ({item.get('difficulty', '?')})")
    input(t(settings["lang"], "press_enter"))


def settings_menu(settings):
    while True:
        show_header(settings)
        _print(t(settings["lang"], "settings"))
        _print(f"{t(settings['lang'], 'lang')}: {settings['lang']}")
        _print(f"{t(settings['lang'], 'sound')}: {t(settings['lang'], 'on' if settings['sound'] else 'off')}")
        _print(f"{t(settings['lang'], 'volume')}: {settings['volume']}")
        _print(f"{t(settings['lang'], 'difficulty')}: {settings['difficulty']}")
        choice = input(t(settings["lang"], "settings_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "1":
            settings_mod.cycle_lang(settings)
        elif choice == "2":
            settings_mod.toggle_sound(settings)
        elif choice == "3":
            settings_mod.cycle_volume(settings)
        elif choice == "4":
            settings_mod.cycle_difficulty(settings)
        elif choice == "b":
            settings_mod.save(settings)
            return
        else:
            _print(t(settings["lang"], "unknown"))


def play_round(settings):
    lang = settings["lang"]
    difficulty = settings["difficulty"]
    cfg = core.config(difficulty)
    snd = Sound(settings["sound"], settings["volume"])
    total_score = 0
    correct_count = 0

    show_header(settings)
    for round_index in range(1, cfg["rounds"] + 1):
        puzzle = core.make_puzzle(difficulty)
        tries_left = 2
        used_hint = False
        _print(t(lang, "round", round=round_index, total=cfg["rounds"]))
        _print(t(lang, "puzzle", numbers=core.numbers_text(puzzle["numbers"]), pick=puzzle["pick"], target=puzzle["target"]))
        while tries_left > 0:
            answer = input(t(lang, "guess_prompt")).strip().lower()
            if answer == "q":
                raise QuitGame()
            if answer == "hint":
                if used_hint:
                    _print(t(lang, "no_hint"))
                    snd.incorrect()
                else:
                    used_hint = True
                    _print(t(lang, "hint", hint=core.hint_text(puzzle)))
                    snd.correct()
                continue
            indices = core.parse_indices(answer, len(puzzle["numbers"]))
            if indices is None or len(indices) != puzzle["pick"]:
                _print(t(lang, "invalid"))
                snd.incorrect()
                continue
            if core.is_correct(puzzle, indices):
                points = core.score_for(difficulty, tries_left - 1, used_hint)
                total_score += points
                correct_count += 1
                _print(t(lang, "correct", points=points))
                snd.correct()
                break
            tries_left -= 1
            if tries_left == 0:
                solution = " ".join(str(i + 1) for i in puzzle["solution"])
                _print(t(lang, "wrong", solution=solution))
                snd.incorrect()
            else:
                _print(t(lang, "invalid"))
                snd.incorrect()

    rating_key = core.final_rating(correct_count, cfg["rounds"])
    _print(t(lang, "finished", correct=correct_count, total=cfg["rounds"], rating=t(lang, rating_key), score=total_score))
    if correct_count:
        snd.win()
    else:
        snd.lose()
    return total_score


def main_menu():
    settings = settings_mod.load()
    while True:
        show_header(settings)
        choice = input(t(settings["lang"], "main_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "p":
            try:
                result = play_round(settings)
            except QuitGame:
                result = 0
            if result > 0:
                name = input(t(settings["lang"], "name_prompt")).strip()
                if name:
                    score_mod.add(name, result, settings["difficulty"])
                    _print(t(settings["lang"], "saved"))
                else:
                    _print(t(settings["lang"], "not_saved"))
            input(t(settings["lang"], "press_enter"))
        elif choice == "h":
            show_help(settings)
        elif choice == "s":
            settings_menu(settings)
        elif choice == "c":
            show_scores(settings)
        elif choice == "q":
            _print(t(settings["lang"], "bye"))
            return
        else:
            _print(t(settings["lang"], "unknown"))


if __name__ == "__main__":
    main_menu()
