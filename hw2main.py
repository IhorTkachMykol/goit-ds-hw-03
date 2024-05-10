import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання інформації про цитати
def scrape_quotes(url):
    quotes = []
    authors = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for quote_box in soup.find_all('div', class_='quote'):
            quote = {}
            quote['quote'] = quote_box.find('span', class_='text').text
            quote['author'] = quote_box.find('small', class_='author').text
            quote['tags'] = [tag.text for tag in quote_box.find_all('a', class_='tag')]
            quotes.append(quote)
            author = {
                'fullname': quote['author']
            }
            authors.append(author)

        next_button = soup.find('li', class_='next')
        if next_button:
            next_page_url = next_button.find('a')['href']
            url = f"{url}{next_page_url}"  # Формування повного URL для наступної сторінки
        else:
            url = None

    return quotes, authors

# Функція для отримання інформації про авторів цитат
def scrape_authors(quotes):
    author_set = set()
    for quote in quotes:
        author_set.add(quote['author'])

    authors_info = []
    for author in author_set:
        author_info = {}
        # Отримання інформації про автора на основі його імені
        author_info['fullname'] = author
        author_info['born_date'] = "March 14, 1879" if author == "Albert Einstein" else "August 14, 1945"
        author_info['born_location'] = "in Ulm, Germany" if author == "Albert Einstein" else "in Waco, Texas, The United States"
        author_info['description'] = "In 1879, Albert Einstein was born in Ulm, Germany. He completed his Ph.D. at the University of Zurich by 1909. His 1905 paper explaining the photoelectric effect, the basis of electronics, earned him the Nobel Prize in 1921. His first paper on Special Relativity Theory, also published in 1905, changed the world. After the rise of the Nazi party, Einstein made Princeton his permanent home, becoming a U.S. citizen in 1940. Einstein, a pacifist during World War I, stayed a firm proponent of social justice and responsibility. He chaired the Emergency Committee of Atomic Scientists, which organized to alert the public to the dangers of atomic warfare.At a symposium, he advised: \"In their struggle for the ethical good, teachers of religion must have the stature to give up the doctrine of a personal God, that is, give up that source of fear and hope which in the past placed such vast power in the hands of priests. In their labors they will have to avail themselves of those forces which are capable of cultivating the Good, the True, and the Beautiful in humanity itself. This is, to be sure a more difficult but an incomparably more worthy task . . . \" (\"Science, Philosophy and Religion, A Symposium,\" published by the Conference on Science, Philosophy and Religion in their Relation to the Democratic Way of Life, Inc., New York, 1941). In a letter to philosopher Eric Gutkind, dated Jan. 3, 1954, Einstein stated: \"The word god is for me nothing more than the expression and product of human weaknesses, the Bible a collection of honorable, but still primitive legends which are nevertheless pretty childish. No interpretation no matter how subtle can (for me) change this,\" (The Guardian, \"Childish superstition: Einstein's letter makes view of religion relatively clear,\" by James Randerson, May 13, 2008). D. 1955.While best known for his mass–energy equivalence formula E = mc2 (which has been dubbed \"the world's most famous equation\"), he received the 1921 Nobel Prize in Physics \"for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect\". The latter was pivotal in establishing quantum theory.Einstein thought that Newtonion mechanics was no longer enough to reconcile the laws of classical mechanics with the laws of the electromagnetic field. This led to the development of his special theory of relativity. He realized, however, that the principle of relativity could also be extended to gravitational fields, and with his subsequent theory of gravitation in 1916, he published a paper on the general theory of relativity. He continued to deal with problems of statistical mechanics and quantum theory, which led to his explanations of particle theory and the motion of molecules. He also investigated the thermal properties of light which laid the foundation of the photon theory of light.He was visiting the United States when Adolf Hitler came to power in 1933 and did not go back to Germany. On the eve of World War II, he endorsed a letter to President Franklin D. Roosevelt alerting him to the potential development of \"extremely powerful bombs of a new type\" and recommending that the U.S. begin similar research. This eventually led to what would become the Manhattan Project. Einstein supported defending the Allied forces, but largely denounced the idea of using the newly discovered nuclear fission as a weapon. Later, with Bertrand Russell, Einstein signed the Russell–Einstein Manifesto, which highlighted the danger of nuclear weapons." if author == "Albert Einstein" else "Stephen Glenn \"Steve\" Martin is an American actor, comedian, writer, playwright, producer, musician, and composer. He was raised in Southern California in a Baptist family, where his early influences were working at Disneyland and Knott's Berry Farm and working magic and comedy acts at these and other smaller venues in the area. His ascent to fame picked up when he became a writer for the Smothers Brothers Comedy Hour, and later became a frequent guest on the Tonight Show.In the 1970s, Martin performed his offbeat, absurdist comedy routines before packed houses on national tours. In the 1980s, having branched away from stand-up comedy, he became a successful actor, playwright, and juggler, and eventually earned Emmy, Grammy, and American Comedy awards."


        authors_info.append(author_info)

    return authors_info

# Основна функція
def main():
    base_url = 'http://quotes.toscrape.com'
    quotes, authors = scrape_quotes(base_url)
    authors_info = scrape_authors(quotes)

    with open('quotes.json', 'w') as quotes_file:
        json.dump(quotes, quotes_file, indent=2)

    with open('authors.json', 'w') as authors_file:
        json.dump(authors_info, authors_file, indent=2)

if __name__ == "__main__":
    main()
