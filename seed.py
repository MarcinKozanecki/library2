from app import app, db
from app.models import Book, Author
from faker import Faker
import random

fake = Faker()

with app.app_context():
    # Dodaj autorów (jeśli nie ma)
    if Author.query.count() == 0:
        for _ in range(5):
            author = Author(name=fake.name())
            db.session.add(author)
        db.session.commit()

    authors = Author.query.all()

    # Dodaj 5 książek
    for _ in range(5):
        book = Book(
            title=fake.sentence(nb_words=3),
            is_available=True
        )
        # Przypisz 1–2 losowych autorów
        book.authors = random.sample(authors, k=random.randint(1, 2))
        db.session.add(book)

    db.session.commit()
    print("Dodano 5 przykładowych książek.")
