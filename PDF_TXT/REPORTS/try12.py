import nltk
from nltk import pos_tag, word_tokenize

def extract_entities(text):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Perform part-of-speech tagging
    tagged_words = pos_tag(words)

    # Initialize variables
    entities = []
    current_entity = []

    # Iterate through tagged words
    for word, pos in tagged_words:
        if pos.startswith('NN') or pos.startswith('JJ'):
            # If the word is a noun or adjective, add it to the current entity
            current_entity.append(word)
        else:
            # If the word is not a noun or adjective, consider the current entity
            if current_entity:
                entities.append(' '.join(current_entity))
                current_entity = []

    # Consider the last entity if the text ends with a noun or adjective
    if current_entity:
        entities.append(' '.join(current_entity))

    return entities

# Example usage
text = "Located in central Croatia at the meeting point between the Croatian lowlands, Croatian highlands,  Pokupje and Kordun. Karlovac is framed by four rivers - Kupa, Korana, Dobra and Mrežnica."
entities = extract_entities(text)
print(entities)