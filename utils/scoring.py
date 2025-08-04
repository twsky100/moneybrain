def score_method(result):
    if result['revenue'] > 0:
        return round(result['revenue'] / (1 + result['visits'] / 100), 2)
    return -1
