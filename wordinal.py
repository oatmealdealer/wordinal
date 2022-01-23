from random import choice
from typing import List, Optional

from nltk.corpus import words
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit import prompt as prompt_unformatted


def five_letter_words():
    for word in words.words("en"):
        if len(word) == 5 and word.lower() == word:
            yield word


def green_bg(text: str):
    return ansi("black", text, bg="green")


def yellow_bg(text: str):
    return ansi("black", text, bg="yellow")


def fprint(text: str):
    print_formatted_text(HTML(text))


def prompt(text: str):
    return prompt_unformatted(HTML(text))


def ansi(color: str, text: str, *, bg: Optional[str] = None):
    if bg is None:
        attrs = ""
    else:
        attrs = f'bg="ansi{bg}"'
    return f"<ansi{color} {attrs}>{text}</ansi{color}>"


class Game:
    LETTERS = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, valid_words: List[str], *, hard_mode=False) -> None:
        self.valid_words = set(valid_words)
        self.word = choice(valid_words)
        self.remaining_letters = set(self.LETTERS)
        self.guessed_letters = set()
        self.misplaced_letters = set()
        self.guesses = 0
        self.hard_mode = hard_mode

    def format_guess(self, guess: str):
        output = ""
        for guess_letter, word_letter in zip(guess, self.word):
            if guess_letter == word_letter:
                output += green_bg(guess_letter)
                self.guessed_letters.add(guess_letter)
            elif guess_letter in self.word:
                output += yellow_bg(guess_letter)
                self.misplaced_letters.add(guess_letter)
            else:
                output += guess_letter
                if guess_letter in self.remaining_letters:
                    self.remaining_letters.remove(guess_letter)
        return output

    def letters(self):
        output = ""
        for letter in self.LETTERS:
            if letter in self.guessed_letters:
                output += green_bg(letter)
            elif letter in self.misplaced_letters:
                output += yellow_bg(letter)
            elif letter in self.remaining_letters:
                output += letter
            else:
                output += " "
        return output

    def get_guess(self):
        return prompt(ansi("cyan", "Enter a word: "))

    def guess_is_valid(self, guess: str):
        if len(guess) != 5:
            fprint(f"{ansi('red', guess)} is not 5 letters.")
            return False
        elif self.hard_mode and any(guessed_letters := [char for char in guess if char not in self.remaining_letters]):
            fprint(
                f"{ansi('cyan', 'Letters: ')}{ansi('red', ', '.join(guessed_letters))}{ansi('cyan', ' have already been guessed!')}"
            )
            return False
        return True

    def play(self):
        while self.guesses < 6:
            while not self.guess_is_valid(guess := self.get_guess()):
                pass
            fprint(ansi("cyan", "You said: ") + self.format_guess(guess))
            fprint(ansi("cyan", "Remaining letters: ") + self.letters())
            if guess == self.word:
                fprint(ansi("cyan", "You win!"))
                return
            self.guesses += 1
        fprint(f"{ansi('cyan', 'Word was:')} {ansi('red', self.word)}")


if __name__ == "__main__":
    hard_mode = "y" in prompt(ansi("cyan", "Play in hard mode? y/n: "))
    words = list(five_letter_words())
    while True:
        Game(words, hard_mode=hard_mode).play()
