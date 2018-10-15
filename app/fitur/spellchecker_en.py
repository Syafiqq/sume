from spellchecker import SpellChecker

spell = SpellChecker(distance=1)
spell.word_frequency.load_text_file('/home/daneswara/Django/app/fitur/id_full.txt')
spell.word_frequency.lo

# find those words that may be misspelled
misspelled = spell.unknown(['salahs', 'danes', 'apa', 'kok', 'iiya', 'bagaaimana'])

for word in misspelled:
    # Get the one `most likely` answer
    print(spell.correction(word))

    # Get a list of `likely` options
    print(spell.candidates(word))


spell.word_frequency.load_words(['microsoft', 'apple', 'google'])
print(spell.known(['microsoft', 'bagaimana']))  # will return both now!
