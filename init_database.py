import random

from requests import post, patch

url_post_beers = "http://127.0.0.1:8000/api/v1/beers/"
url_post_categories = "http://127.0.0.1:8000/api/v1/categories/"
url_post_reviews = "http://127.0.0.1:8000/api/v1/reviews/"
url_post_comments = "http://127.0.0.1:8000/api/v1/comments/"
url_login = "http://127.0.0.1:8000/api/v1/auth/login"
url_register = "http://127.0.0.1:8000/api/v1/auth/register"

admin_login_data = {"username": "admin",
                    "password": "admin"}

users = [
    {'username': 'user1', 'password': 'pass1', 'email': 'user1@example.com', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': 'user2', 'password': 'pass2', 'email': 'user2@example.com', 'first_name': 'Jane',
     'last_name': 'Smith'},
    {'username': 'user3', 'password': 'pass3', 'email': 'user3@example.com', 'first_name': 'Bob',
     'last_name': 'Johnson'},
    {'username': 'user4', 'password': 'pass4', 'email': 'user4@example.com', 'first_name': 'Alice',
     'last_name': 'Williams'},
    {'username': 'user5', 'password': 'pass5', 'email': 'user5@example.com', 'first_name': 'Charlie',
     'last_name': 'Brown'}
]

categories = [{"name": "IPA"},
              {"name": "APA"},
              {"name": "Lager"},
              {"name": "Porter"},
              {"name": "Weizen"},
              {"name": "Bock"},
              {"name": "Barley wine"},
              {"name": "Stout"},
              {"name": "Pilzner"},
              {"name": "Oktoberfestbier"},
              {"name": "Vienna Red Lager"},
              {"name": "Dunkel"},
              ]
images = ['perla.jfif', 'warka.jfif', 'zywiec_porter.jfif', 'zywiec_biale.jfif', 'zywiec_apa.jpeg', 'zywiec_ipa.jpg']
beers = [{'name': 'Perła Export',
          'description': 'Perła w butelce to jasne pełne piwo o 5,6% zawartości '
                         'alkoholu, które znakomicie orzeźwia, dzięki czemu cieszy '
                         'się swoim zainteresowaniem przede wszystkim podczas cieplejszych '
                         'dni, lecz nie tylko – jej miłośnicy doceniają jej walory smakowe '
                         'także podczas przeróżnych spotkań w gronie znajomych. '
                         'Charakteryzuje się ona dość wyrazistym aromatem chmielu oraz '
                         'złocistym kolorem, atrakcyjnie prezentującym się na tle '
                         'pozostałych piw w sklepach. Oferujemy Państwu prawdziwą Perłę, '
                         'która zyskuje uznanie coraz większego grona odbiorców, już nie '
                         'tylko w Polsce, lecz także w licznych krajach na całym świecie.',
          'category': 3},
         {'name': 'Warka',
          'description': 'Warka to jasne piwo dolnej fermentacji typu lager, '
                         'o przyjemnym i łagodnym smaku oraz delikatnej goryczce. '
                         'Produkowane jest w browarze w Warce od 1975 r. oraz w '
                         'browarze w Żywcu. Nazwa piwa wywodzi się zarówno od miasta, '
                         'w którym powstało jak i od określenia piwowarskiej miary, '
                         'oznaczającej porcję piwa uzyskanego z jednego warzenia.',
          'category': 3},
         {'name': 'Żywiec Porter',
          'description': 'Żywiec Porter jest bardzo mocnym i treściwym piwem charakteryzującym '
                         'się posmakiem palonego słodu z nutami kawowo-karmelowymi. Produkowany '
                         'jest ze słodu monachijskiego oraz kombinacji słodów jasnych i specjalnych, '
                         'fermentowany w otwartych kadziach i poddawany długiemu okresowi leżakowania, '
                         'który może trwać do 6 miesięcy.',
          'category': 4},
         {'name': 'Żywiec Białe',
          'description': 'Żywiec Białe to wariacja na temat interesującego piwnego stylu jakim jest '
                         'witbier - znajdziemy w nim to, co najciekawsze i najbardziej charakterystyczne '
                         'dla piw pszenicznych, czyli jasną barwę, łagodny smak, ziołowym zapach kolendry '
                         'i bananowy aromat. Doskonale orzeźwia i odświeża w gorące dni. Mariaż przypraw i '
                         'słodu pszenicznego skutkuje nieprzeciętnym piwem sesyjnym, które umili letnie '
                         'wieczory i spotkania z przyjaciółmi. Delikatny i lekki trunek o zawartości alkoholu '
                         '4,9% obj. intryguje i zaskakuje intensywnym orzeźwieniem.',
          'category': 5},
         {'name': 'Żywiec APA',
          'description': 'Intensywnie chmielowe piwo typu Pale Ale z nutą cytrynową. Warzone z użyciem '
                         'pięciu odmian chmielu, przy zastosowaniu górnej fermentacji w otwartych kadziach. '
                         'Chmielone na zimno. Receptura piwa APA jest dziełem mistrzów Żywieckiej Szkoły '
                         'Piwowarskiej, którzy od pokoleń pracują w warzelniach arcyksiążęcych w Żywcu i Cieszynie.',
          'category': 2},
         {'name': 'Żywiec Sesyjne IPA',
          'description': 'Session India Pale Ale to stosunkowo młody styl, będący lżejszą wersją klasycznego '
                         'stylu IPA, czyli mocno chmielonego trunku, którego historia sięga brytyjskich czasów '
                         'kolonialnych. Żywiec Sesyjne IPA charakteryzuje się przyjemną chmielową goryczką '
                         'oraz wyraźnie wyczuwalnymi nutami owoców egzotycznych i cytrusów. Jest chmielone na '
                         'zimno wyjątkową kompozycją amerykańskich chmieli.',
          'category': 1},
         ]

reviews = [{
    "title": "Najlepsze piwo na świecie",
    "content": "Perła Export to piwo, które przypadło mi do gustu. Jasne, pełne i z ładnym, średnią goryczką. "
               "Aromat jest lekko słodowy, a smak delikatny i przyjemny. Piwo jest dobrze wyważone i łatwo się "
               "je pije. Moim zdaniem, Perła Export jest świetnym piwem na codzienne picie, ponieważ jest "
               "orzeźwiające i nie jest zbyt intensywne. Polecam je zarówno miłośnikom piw jasnych, jak i tym, "
               "którzy dopiero zaczynają swoją przygodę z piwem.",
    "beer": 1,
    'rating': 10},

    {"title": "Nie smakuje mi.",
     "content": "Perła to piwo, który niestety nie przypadło mi do gustu. Ma ono silnie metaliczny posmak i "
                "intensywny, nieprzyjemny zapach. Goryczka jest zbyt mocna i pozostaje długo w ustach. Smak "
                "jest bardzo niezrównoważony, z dominującymi nuty gorzkie i kwaśne. Trudno mi to polecić "
                "komukolwiek, niezależnie od preferencji smakowych.",
     "beer": 1,
     'rating': 2},

]

comments = [{'content': 'Zgadzam się z autorem.',
             'review': 1},
            {'content': 'Nie zgadzam się z autorem.',
             'review': 1},
            {'content': 'Zgadzam się z autorem.',
             'review': 2},
            {'content': 'Nie zgadzam się z autorem.',
             'review': 2},
            {'content': 'Zgadzam się z autorem.',
             'review': 3},
            {'content': 'Nie zgadzam się z autorem.',
             'review': 3},
            ]

if __name__ == "__main__":
    token = post(url_login, admin_login_data).json().get('token')
    authorization = {"Authorization": f"Token {token}"}

    # REGISTER USERS
    for user in users:
        response = post(url_register, user)
        if response.status_code == 200:
            print(f"Pomyślnie zarejestrowano użytkownika {user.get('username')}")
        else:
            print(f"Błąd podczas rejestracji użytkownika {user.get('username')}")

    # POST CATEGORIES
    for category in categories:
        response = post(url_post_categories, category, headers=authorization)
        if response.status_code == 201:
            print(f"Pomyślnie dodano kategorię {category.get('name')}.")
        else:
            print(f"Błąd podczas dodawania kategorii {category.get('name')}.")

    # POST BEERS
    for image, beer in zip(images, beers):
        files = {
            "image_url": open(f"beer_images/{image}", 'rb')
        }
        response = post(url_post_beers, beer, files=files, headers=authorization)
        if response.status_code == 201:
            print(f"Pomyślnie dodano piwo {beer.get('name')}.")
        else:
            print(f"Błąd podczas dodawania piwa {beer.get('name')}.")

    # ACTIVATE BEERS
    for i in range(1, 7):
        response = patch(url_post_beers + f"{i}/", {'active': True}, headers=authorization)
        if response.status_code == 200:
            print(f"Pomyślnie aktywowano piwo o id={i}.")
        else:
            print(f"Błąd podczas aktywacji piwa o id={i}.")

    # POST REVIEWS
    for review in reviews:
        user = random.choice(users)
        token = post(url_login, {'username': user.get('username'),
                                 'password': user.get('password')}).json().get('token')
        authorization = {"Authorization": f"Token {token}"}

        response = post(url_post_reviews, review, headers=authorization)
        if response.status_code == 201:
            print(f"Pomyślnie dodano recenzję: {review.get('title')}.")
        else:
            print(f"Błąd podczas dodawania recenzji: {review.get('title')}.")

    # POST COMMENTS
    for comment in comments:
        user = random.choice(users)
        token = post(url_login, {'username': user.get('username'),
                                 'password': user.get('password')}).json().get('token')
        authorization = {"Authorization": f"Token {token}"}

        response = post(url_post_comments, comment, headers=authorization)
        if response.status_code == 201:
            print(f"Pomyślnie dodano komentarz.")
        else:
            print(f"Błąd podczas dodawania komentarza.")
