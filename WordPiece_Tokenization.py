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


#Output

WORD FREQUENCIES
robot : 4
robots : 2
robotic : 2
code : 3
coder : 2
coding : 2
computer : 3
compute : 1

 INITIAL SPLITS
robot -> ['r', '##o', '##b', '##o', '##t']
robots -> ['r', '##o', '##b', '##o', '##t', '##s']
robotic -> ['r', '##o', '##b', '##o', '##t', '##i', '##c']
code -> ['c', '##o', '##d', '##e']
coder -> ['c', '##o', '##d', '##e', '##r']
coding -> ['c', '##o', '##d', '##i', '##n', '##g']
computer -> ['c', '##o', '##m', '##p', '##u', '##t', '##e', '##r']
compute -> ['c', '##o', '##m', '##p', '##u', '##t', '##e']

 INITIAL VOCABULARY 
##b
##c
##d
##e
##g
##i
##m
##n
##o
##p
##r
##s
##t
##u
c
r

 WORDPIECE TRAINING

Merge 1
Best Pair : ('##n', '##g')
Pair Frequency : 2
Score : 0.5
New Token : ##ng

Merge 2
Best Pair : ('##i', '##c')
Pair Frequency : 2
Score : 0.25
New Token : ##ic

Merge 3
Best Pair : ('##i', '##ng')
Pair Frequency : 2
Score : 0.5
New Token : ##ing

Merge 4
Best Pair : ('##m', '##p')
Pair Frequency : 4
Score : 0.25
New Token : ##mp

Merge 5
Best Pair : ('##mp', '##u')
Pair Frequency : 4
Score : 0.25
New Token : ##mpu

Merge 6
Best Pair : ('##d', '##ing')
Pair Frequency : 2
Score : 0.142857
New Token : ##ding

Merge 7
Best Pair : ('##d', '##e')
Pair Frequency : 5
Score : 0.111111
New Token : ##de

Merge 8
Best Pair : ('##e', '##r')
Pair Frequency : 3
Score : 0.15
New Token : ##er

Merge 9
Best Pair : ('##de', '##r')
Pair Frequency : 2
Score : 0.2
New Token : ##der

Merge 10
Best Pair : ('##t', '##s')
Pair Frequency : 2
Score : 0.083333
New Token : ##ts

 FINAL WORD SPLITS 
robot -> ['r', '##o', '##b', '##o', '##t']
robots -> ['r', '##o', '##b', '##o', '##ts']
robotic -> ['r', '##o', '##b', '##o', '##t', '##ic']
code -> ['c', '##o', '##de']
coder -> ['c', '##o', '##der']
coding -> ['c', '##o', '##ding']
computer -> ['c', '##o', '##mpu', '##t', '##er']
compute -> ['c', '##o', '##mpu', '##t', '##e']

 FINAL VOCABULARY 
##b
##c
##d
##de
##der
##ding
##e
##er
##g
##i
##ic
##ing
##m
##mp
##mpu
##n
##ng
##o
##p
##r
##s
##t
##ts
##u
c
r

Vocabulary Size : 26

 TEST TOKENIZATION 
Test Word : robotic
Tokens : ['r', '##o', '##b', '##o', '##t', '##ic']

 TOKEN ID MAPPING 
##b : 0
##c : 1
##d : 2
##de : 3
##der : 4
##ding : 5
##e : 6
##er : 7
##g : 8
##i : 9
##ic : 10
##ing : 11
##m : 12
##mp : 13
##mpu : 14
##n : 15
##ng : 16
##o : 17
##p : 18
##r : 19
##s : 20
##t : 21
##ts : 22
##u : 23
[UNK] : 24
c : 25
r : 26

Input Tokens : ['r', '##o', '##b', '##o', '##t', '##ic']
Token IDs : [26, 17, 0, 17, 21, 10]



