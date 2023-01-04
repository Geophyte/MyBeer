# Struktura projektu

Aplikacja serwerowa znajduje się w branchu *backend*.
Aplikacja okienkowa znajduje się w branchu *desktop*.

# Instalacja aplikacji serwerowej

Stworzenie obrazu Dockera:

    cd backend    
    docker-compose up

Uruchomienie terminala django:

    docker ps
    docker exec -it [id_kontenera] bash

Dostęp do aplikacji jest możliwy na localhost

    http://127.0.0.1:8000/

lub poprzez dowolne narzędzie umożliwiające wykonywanie requestów. Podczas testów API korzystaliśmy z Pythona i
biblioteki requests.

Aplikacja administratora:

    http://127.0.0.1:8000/admin/

API:

    http://127.0.0.1:8000/api/v1/

# Przykłady zapytań do API

## Rejestracja

    register = "http://127.0.0.1:8000/api/v1/auth/register"
    post(register, {'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.com',
                    'first_name': 'foo',
                    'last_name': 'bar'})

## Logowanie

    login = "http://127.0.0.1:8000/api/v1/auth/login"
    token = post(login, {"username": "foo",
                        "password": "bar"}).json()['token']

## Dane użytkownika

    user_data = "http://127.0.0.1:8000/api/v1/auth/user"
    get(user_data, headers={"Authorization": f"Token {token}"})

## Wylogowanie

    logout = "http://127.0.0.1:8000/api/v1/auth/logout"
    post(logout, headers={"Authorization": f"Token {token}"})

## Lista piw

    url = "http://127.0.0.1:8000/api/v1/beers/"
    get(url, headers={"Authorization": f"Token {token}"})

## Dane piwo

    url = "http://127.0.0.1:8000/api/v1/beers/1/"
    get(url, headers={"Authorization": f"Token {token}"})

## Piwa z danej kategorii

    url = "http://127.0.0.1:8000/api/v1/beers/?category=IPA"
    get(url, headers={"Authorization": f"Token {token}"})

## Dodaj piwo
    url = "http://127.0.0.1:8000/api/v1/beers/"
    new_beer = {
        "name": "Heineken",
        "description": "Very interesting and long description.",
        "category": 5}
    post(url, new_beer, headers={"Authorization": f"Token {token}"})

Podobnie dla endpointów */categories*, */reviews*, */comments*.

## Instalacja aplikacji okienkowej
    
