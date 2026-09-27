from app.repositories.in_memory import db

if __name__ == "__main__":
    db.reset_and_seed()
    print("Reset StatSaksham AI demo state back to baseline (Score: 67/100).")
