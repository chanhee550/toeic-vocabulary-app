import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

IPA_MAP = [
    # Diphthongs & long vowels (check first)
    ('eɪ', 'ay'), ('aɪ', 'eye'), ('ɔɪ', 'oy'), ('aʊ', 'ow'), ('oʊ', 'oh'),
    ('ɪr', 'eer'), ('ɛr', 'air'), ('ʊr', 'oor'), ('ɑr', 'ar'), ('ɔr', 'or'),
    # Affricates
    ('tʃ', 'ch'), ('ʧ', 'ch'), ('dʒ', 'j'), ('ʤ', 'j'),
    # Consonants
    ('ʃ', 'sh'), ('ʒ', 'zh'), ('θ', 'th'), ('ð', 'th'), ('ŋ', 'ng'),
    # Vowels
    ('iː', 'ee'), ('uː', 'oo'),
    ('ɪ', 'ih'), ('i', 'ee'), ('ɛ', 'eh'), ('æ', 'a'),
    ('ɑ', 'ah'), ('ɔ', 'aw'), ('ʌ', 'uh'), ('ʊ', 'oo'), ('u', 'oo'),
    ('ə', 'uh'), ('ɝ', 'er'), ('ɜ', 'er'), ('ɚ', 'er'),
    # Simple consonants
    ('j', 'y'), ('r', 'r'), ('l', 'l'), ('w', 'w'), ('h', 'h'),
    ('p', 'p'), ('b', 'b'), ('t', 't'), ('d', 'd'), ('k', 'k'), ('g', 'g'),
    ('f', 'f'), ('v', 'v'), ('s', 's'), ('z', 'z'), ('m', 'm'), ('n', 'n'),
]

VOWEL_SOUNDS = {'ay','eye','oy','ow','oh','eer','air','oor','ar','or','ee','oo','ih','eh','a','ah','aw','uh','er'}

def ipa_to_respelling(ipa):
    if not ipa:
        return ''

    # Parse IPA into tokens with stress info
    tokens = []  # list of (sound, is_stressed)
    i = 0
    stressed = False

    while i < len(ipa):
        c = ipa[i]
        if c == 'ˈ':
            stressed = True
            i += 1
            continue
        if c == 'ˌ':
            i += 1
            continue
        if c in (' ', '-'):
            i += 1
            continue

        matched = False
        for pat, repl in IPA_MAP:
            if ipa[i:i+len(pat)] == pat:
                tokens.append((repl, stressed))
                # Reset stress after first vowel sound in stressed syllable
                if repl in VOWEL_SOUNDS and stressed:
                    stressed = False
                i += len(pat)
                matched = True
                break
        if not matched:
            i += 1

    # Group tokens into syllables (each syllable has one vowel sound)
    syllables = []
    current = []
    current_stressed = False
    for sound, is_stressed in tokens:
        if is_stressed and current:
            # Check if current syllable has a vowel yet
            has_vowel = any(s in VOWEL_SOUNDS for s, _ in current)
            if has_vowel:
                syllables.append((current, current_stressed))
                current = []
                current_stressed = False
        if is_stressed:
            current_stressed = True
        current.append((sound, is_stressed))
        # If we just added a vowel and there are more tokens, check for syllable break
        if sound in VOWEL_SOUNDS and len(current) > 1:
            # Don't break yet, let consonants attach
            pass

    if current:
        syllables.append((current, current_stressed))

    # Simple approach: just join all sounds, insert - between syllable groups
    # Better: split by vowel sounds
    all_sounds = [s for s, _ in tokens]
    all_stress = [st for _, st in tokens]

    # Find vowel positions
    vowel_pos = [i for i, s in enumerate(all_sounds) if s in VOWEL_SOUNDS]

    if not vowel_pos:
        return '-'.join(all_sounds)

    # Build syllables by splitting around vowels
    syls = []
    for vi, vp in enumerate(vowel_pos):
        # Start: after previous vowel's consonants, or 0
        if vi == 0:
            start = 0
        else:
            prev_vp = vowel_pos[vi - 1]
            # Split consonants between vowels
            gap_start = prev_vp + 1
            gap_end = vp
            mid = gap_start + (gap_end - gap_start + 1) // 2
            start = mid

        # End: before next vowel's consonants, or end
        if vi == len(vowel_pos) - 1:
            end = len(all_sounds)
        else:
            next_vp = vowel_pos[vi + 1]
            gap_start = vp + 1
            gap_end = next_vp
            mid = gap_start + (gap_end - gap_start + 1) // 2
            end = mid

        syl_sounds = all_sounds[start:end]
        # Check if this syllable is stressed
        is_stressed = any(all_stress[j] for j in range(start, min(end, len(all_stress))))
        syl_text = ''.join(syl_sounds)
        if is_stressed:
            syl_text = syl_text.upper()
        syls.append(syl_text)

    return '-'.join(syls)


with open(r'C:\Users\chan7\toeic words\toeic_words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

for w in words:
    ipa = w.get('ipa', '')
    w['pronun'] = ipa_to_respelling(ipa)

for w in words[:20]:
    print(f"  {w['word']:20s} {w['pronun']:25s} /{w.get('ipa','')}/")

with open(r'C:\Users\chan7\toeic words\toeic_words.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)

count = sum(1 for w in words if w['pronun'])
print(f'\nGenerated: {count}/{len(words)}')
