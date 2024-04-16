class Category:
    def __init__(self, name):
        self.name = name
        self.games = []

    def add_game(self, game):
        self.games.append(game)

    def __str__(self):
        return self.name

class Platform:
    def __init__(self):
        self.games = []

    def add_game(self, game):
        self.games.append(game)
        print(f"Гра '{game.title}' успішно додана.")

    def list_games(self):
        if self.games:
            for game in self.games:
                print(game)
        else:
            print("На цій платформі ще немає ігор")

    def search_game(self, **kwargs):
        found_games = []
        for game in self.games:
            match = True
            for key, value in kwargs.items():
                if getattr(game, key, None) != value:
                    match = False
                    break
            if match:
                found_games.append(game)
        return found_games

    def is_duplicate(self, title):
        for game in self.games:
            if game.title == title:
                return True
        return False

class Game:
    MAX_DESCRIPTION_LENGTH = 200

    def __init__(self, title, description, genre, rating, price, category):
        self.title = title
        self.description = self.validate_description(description)
        self.genre = genre
        self.rating = rating
        self.price = price
        self.reviews = []
        self.category = category

    def validate_description(self, description):
        if len(description) <= self.MAX_DESCRIPTION_LENGTH:
            return description
        else:
            return description[:self.MAX_DESCRIPTION_LENGTH]
    
    def __str__(self):
        return f"Категорія: {self.category}, Назва: {self.title}, Опис: {self.description}, Жанр: {self.genre}, Рейтинг: {self.rating}, Ціна: {self.price}"

class GameReview:
    MAX_COMMENT_LENGTH = 100

    def __init__(self, user, rating, comment):
        self.user = self.validate_user(user)
        self.rating = self.validate_rating(rating)
        self.comment = self.validate_comment(comment)

    def validate_user(self, user):
        if isinstance(user, str):
            return user
        else:
            raise ValueError("Ім'я користувача має бути рядком")

    def validate_comment(self, comment):
        if len(comment) <= self.MAX_COMMENT_LENGTH:
            return comment
        else:
            return comment[:self.MAX_COMMENT_LENGTH]

    def validate_rating(self, rating):
        if 1 <= rating <= 5:
            return rating
        else:
            raise ValueError("Рейтинг повинен бути від 1 до 5")
    
    def display(self):
        return f"Відгук від {self.user}: Рейтинг - {self.rating}, Коментар - {self.comment}"

class GamePlatformInterface:
    def __init__(self):
        self.platform = Platform()
        self.categories = []

    def run(self):
        print("Ласкаво просимо до нашої платформи для продажу відеоігор!")

        while True:
            print("\nОберіть опцію:")
            print("1. Додати категорію")
            print("2. Додати гру")
            print("3. Переглянути доступні ігри")
            print("4. Пошук ігор")
            print("5. Залишити відгук")
            print("6. Переглянути відгуки для гри")
            print("7. Вийти")

            choice = input("Ваш вибір: ")

            if choice == '1':
                self.add_category()
            elif choice == '2':
                self.add_game()
            elif choice == '3':
                self.platform.list_games()
            elif choice == '4':
                self.search_game()
            elif choice == '5':
                self.add_review()
            elif choice == '6':
                self.view_reviews()
            elif choice == '7':
                print("Дякую за використання нашої платформи!")
                break
            else:
                print("Невідома опція. Спробуйте ще раз.")

    def add_category(self):
        name = input("Введіть назву категорії: ")
        category = Category(name)
        self.categories.append(category)
        print(f"Категорія '{name}' успішно додана.")

    def add_game(self):
        title = input("Введіть назву гри: ")
        description = input("Введіть опис гри: ")
        genre = input("Введіть жанр гри: ")
        rating = float(input("Введіть рейтинг гри (від 1 до 5): "))
        price = float(input("Введіть ціну гри: "))
        
        print("Доступні категорії:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")
        category_choice = int(input("Оберіть категорію: "))
        category = self.categories[category_choice - 1] if 1 <= category_choice <= len(self.categories) else None

        if self.platform.is_duplicate(title):
            print(f"Гра з назвою '{title}' вже існує на цій платформі.")
        else:
            game = Game(title, description, genre, rating, price, category)
            self.platform.add_game(game)

    def search_game(self):
        print("\nОберіть критерій пошуку:")
        print("1. За назвою")
        print("2. За жанром")
        print("3. За рейтингом")
        print("4. За ціною")
        print("5. Назад")

        choice = input("Ваш вибір: ")

        if choice == '1':
            keyword = input("Введіть назву гри: ")
            found_games = self.platform.search_game(title=keyword)
        elif choice == '2':
            keyword = input("Введіть жанр гри: ")
            found_games = self.platform.search_game(genre=keyword)
        elif choice == '3':
            rating = float(input("Введіть мінімальний рейтинг: "))
            found_games = self.platform.search_game(rating=rating)
        elif choice == '4':
            price = float(input("Введіть максимальну ціну: "))
            found_games = self.platform.search_game(price=price)
        elif choice == '5':
            return
        else:
            print("Невідома опція.")
            return

        if found_games:
            print("Результати пошуку:")
            for game in found_games:
                print(game)
                if game.reviews:
                    print("Відгуки:")
                    for review in game.reviews:
                        print(review.display())
                else:
                    print("Відгуків поки немає.")
        else:
            print("Ігор за вашим запитом не знайдено.")

    def add_review(self):
        title = input("Введіть назву гри, для якої хочете залишити відгук: ")
        game = None
        for g in self.platform.games:
            if g.title == title:
                game = g
                break
        if game:
            user = input("Введіть ваше ім'я: ")
            rating = float(input("Введіть рейтинг гри (від 1 до 5): "))
            comment = input("Напишіть свій коментар: ")
            review = GameReview(user, rating, comment)
            game.reviews.append(review)  # Додаємо відгук до списку відгуків гри
            print(f"Відгук на гру '{title}' успішно додано.")
        else:
            print(f"Гру з назвою '{title}' не знайдено.")

    def view_reviews(self):
        title = input("Введіть назву гри, для якої хочете переглянути відгуки: ")
        game = None
        for g in self.platform.games:
            if g.title == title:
                game = g
                break
        if game:
            if game.reviews:
                print(f"Відгуки для гри '{title}':")
                for review in game.reviews:
                    print(review.display())
            else:
                print(f"Для гри '{title}' відгуки відсутні.")
        else:
            print(f"Гру з назвою '{title}' не знайдено.")

if __name__ == "__main__":
    interface = GamePlatformInterface()
    interface.run()