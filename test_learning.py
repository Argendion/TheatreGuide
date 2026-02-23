# test_learning.py
from recommendation_engine import RecommendationEngine
import sqlite3

# Create a test user
conn = sqlite3.connect('database.db')
conn.execute('INSERT OR IGNORE INTO users (id, username, password) VALUES (1, "testuser", "password")')
conn.commit()
conn.close()

# Test the engine
engine = RecommendationEngine()

# Simulate ratings
print("Updating profile for user 1 with rating for show 1...")
engine.update_user_profile(1, 1, 5)  # Liked show 1 a lot

print("Updating profile with rating for show 2...")
engine.update_user_profile(1, 2, 2)  # Didn't like show 2

# Get recommendations
print("\nGetting recommendations...")
recs = engine.get_recommendations(1)
for rec in recs:
    print(f"- {rec['title']} (Genre: {rec['genre']})")