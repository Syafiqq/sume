from spellchecker import SpellChecker

spell = SpellChecker()

# find those words that may be misspelled
misspelled = spell.unknown(['something', 'tdak', 'hapenning', 'bsa'])

for word in misspelled:
    # Get the one `most likely` answer
    print(spell.correction(word))

    # Get a list of `likely` options
    print(spell.candidates(word))


spell.word_frequency.load_words(['microsoft', 'apple', 'google'])
print(spell.known(['microsoft', 'bagaimana']))  # will return both now!
