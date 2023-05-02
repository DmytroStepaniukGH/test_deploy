"""
5. Write a script to remove values duplicates from dictionary. Feel free
   to hardcode your dictionary.
"""
if __name__ == "__main__":
    dict_1 = {'foo': 'bar', 'bar': 'buz', 'USD': '42', 'EUR': '42'}

    result = {}
    for key, value in dict_1.items():
        if value not in result.values():
            result[key] = value

    print(f'Result: {result}')