from collections import Counter

word_freq = {
    "robot": 4,
    "robots": 2,
    "robotic": 2,
    "code": 3,
    "coder": 2,
    "coding": 2,
    "computer": 3,
    "compute": 1
}

print("WORD FREQUENCIES")

for word, freq in word_freq.items():
    print(word, ":", freq)

splits = {}

for word in word_freq:

    tokens = []

    for i, char in enumerate(word):

        if i == 0:
            tokens.append(char)
        else:
            tokens.append("##" + char)

    splits[word] = tokens


print("\n INITIAL SPLITS")

for word, tokens in splits.items():
    print(word, "->", tokens)


vocab = set()

for tokens in splits.values():
    vocab.update(tokens)


print("\n INITIAL VOCABULARY ")

for token in sorted(vocab):
    print(token)



def get_token_frequency(splits, word_freq):

    token_freq = Counter()

    for word, tokens in splits.items():

        frequency = word_freq[word]

        for token in tokens:
            token_freq[token] += frequency

    return token_freq


def get_pair_frequency(splits, word_freq):

    pair_freq = Counter()

    for word, tokens in splits.items():

        frequency = word_freq[word]

        for i in range(len(tokens) - 1):

            pair = (
                tokens[i],
                tokens[i + 1]
            )

            pair_freq[pair] += frequency

    return pair_freq



def calculate_scores(pair_freq, token_freq):

    scores = {}

    for pair, frequency in pair_freq.items():

        first = pair[0]
        second = pair[1]

        score = frequency / (
            token_freq[first] *
            token_freq[second]
        )

        scores[pair] = score

    return scores



def merge_pair(splits, pair):

    new_token = (
        pair[0] +
        pair[1].replace("##", "")
    )

    for word in splits:

        tokens = splits[word]

        new_tokens = []

        i = 0

        while i < len(tokens):

            if i < len(tokens) - 1:

                current_pair = (
                    tokens[i],
                    tokens[i + 1]
                )

                if current_pair == pair:

                    new_tokens.append(new_token)

                    i += 2

                    continue

            new_tokens.append(tokens[i])

            i += 1

        splits[word] = new_tokens

    return new_token


number_of_merges = 10

print("\n WORDPIECE TRAINING")

for step in range(number_of_merges):

    pair_freq = get_pair_frequency(
        splits,
        word_freq
    )

    if not pair_freq:
        break

    token_freq = get_token_frequency(
        splits,
        word_freq
    )

    scores = calculate_scores(
        pair_freq,
        token_freq
    )

    best_pair = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_pair]

    new_token = merge_pair(
        splits,
        best_pair
    )

    vocab.add(new_token)

    print("\nMerge", step + 1)
    print("Best Pair :", best_pair)
    print("Pair Frequency :", pair_freq[best_pair])
    print("Score :", round(best_score, 6))
    print("New Token :", new_token)




print("\n FINAL WORD SPLITS ")

for word, tokens in splits.items():
    print(word, "->", tokens)



print("\n FINAL VOCABULARY ")

for token in sorted(vocab):
    print(token)

print("\nVocabulary Size :", len(vocab))


def tokenize_word(word, vocab):

    tokens = []

    while len(word) > 0:

        found = False

        for i in range(len(word), 0, -1):

            part = word[:i]

            if len(tokens) > 0:
                part = "##" + part

            if part in vocab:

                tokens.append(part)

                word = word[i:]

                found = True

                break

        if not found:

            return ["[UNK]"]

    return tokens



vocab.add("[UNK]")



test_word = "robotic"

encoded_tokens = tokenize_word(
    test_word,
    vocab
)

print("\n TEST TOKENIZATION ")

print("Test Word :", test_word)
print("Tokens :", encoded_tokens)


token_to_id = {}

for index, token in enumerate(sorted(vocab)):

    token_to_id[token] = index


token_ids = []

for token in encoded_tokens:

    token_ids.append(
        token_to_id[token]
    )


print("\n TOKEN ID MAPPING ")

for token, token_id in token_to_id.items():
    print(token, ":", token_id)


print("\nInput Tokens :", encoded_tokens)
print("Token IDs :", token_ids)



