import sys
from lib.text import normalize, tokenize, count_freq, top_n
deff_kr = True
if __name__ == '__main__':
    text = sys.stdin.read()
    
    if not text.strip():
        sys.exit(0)

    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top_words = top_n(freq, n=5)

    if not deff_kr:
        print(f"Всего слов: {len(tokens)}")
        print(f"Уникальных слов: {len(freq)}")
        print("Топ-5:")
        for word, count in top_words:
            print(f"{word}:{count}")
    else:
        if top_words:
            max_len = max(len(w) for w, _ in top_words)
            max_len = max(max_len, 5) 
            print(f"{'слово':<{max_len}} | частота")
            print("-" * (max_len + 10))
            for word, count in top_words:
                print(f"{word:<{max_len}} | {count}")