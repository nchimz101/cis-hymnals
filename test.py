import requests

BASE_URL = 'https://cis-hymnals-47632a642a1e.herokuapp.com'


def test_languages():
    response = requests.get(f'{BASE_URL}/languages')
    print("Languages:")
    print(response.json())


def test_hymnals(language):
    response = requests.get(f'{BASE_URL}/hymnals/{language}')
    print(f"\nHymnals for {language}:")
    print(f"Total hymns: {len(response.json())}")
    print("First hymn:", response.json()[0])


def test_specific_hymn(language, number):
    response = requests.get(f'{BASE_URL}/hymnals/{language}/{number}')
    print(f"\nHymn {number} in {language}:")
    print(response.json())


def test_search(language, query):
    response = requests.get(f'{BASE_URL}/search', params={'language': language, 'query': query})
    print(f"\nSearch results for '{query}' in {language}:")
    print(f"Total results: {len(response.json())}")
    for result in response.json():
        print(f"- Hymn {result['number']}: {result['title']}")


def main():
    test_languages()

    # Example usage (modify based on your actual data)
    language = 'en'  # change to your language key
    test_hymnals(language)
    test_specific_hymn(language, 1)
    test_search(language, 'love')


if __name__ == '__main__':
    main()
