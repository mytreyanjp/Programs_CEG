def calculate_ic(text):
    from collections import Counter
    N = len(text)
    freq = Counter(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1)) if N > 1 else 0
    return ic

def estimate_key_length(ciphertext, max_key_length=20):
    ciphertext = ciphertext.upper()
    ciphertext = ''.join(filter(str.isalpha, ciphertext))
    results = {}
    for key_len in range(1, max_key_length + 1):
        ics = []
        for i in range(key_len):
            group = ciphertext[i::key_len]
            ic = calculate_ic(group)
            ics.append(ic)
        avg_ic = sum(ics) / len(ics)
        results[key_len] = avg_ic
    return results

ciphertext = "VSWMLFVCCXXUVZFSFGWCGYWSMPGSRMKYGCGWWSSQRJNOCZFQDPFMHUWCWNBQQFKCODNPOLQUAMSLWEFFCWQDLGCFKVZDLRLGNHSRMTASLVGPLZXLYKEOFOAHPOHGYCTBCQKKRVNPECNKWDTUAHKVDSWXJKEMWKSNWSHJWUNCGSSPTSMJGXPFHPWPEGUQVGOIWDLKZBOAPDHCWMVTCHVXCNSNRVCJ"

ic_results = estimate_key_length(ciphertext)

for key_len, ic_value in ic_results.items():
    print(f"Key Length: {key_len}, Avg IC: {ic_value:.4f}")
