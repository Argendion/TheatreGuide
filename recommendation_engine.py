import sqlite3
from collections import defaultdict

class RecommendationEngine:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def update_user_profile(self, user_id, show_id, rating):
        """
        This is the LEARNING function!
        When a user rates a show highly, we update their keyword preferences.
        """
        conn = self.get_connection()
        
        # Get the show's keywords
        show = conn.execute('SELECT keywords FROM shows WHERE id = ?', 
                           (show_id,)).fetchone()
        
        if show and show['keywords']:
            # Split keywords and clean them
            keywords = [k.strip() for k in show['keywords'].split(',')]
            
            # If rating is good (4 or 5 stars), increase keyword scores
            # If rating is bad (1 or 2 stars), decrease keyword scores
            score_change = 0
            if rating >= 4:
                score_change = 1
            elif rating <= 2:
                score_change = -1
            
            if score_change != 0:
                for keyword in keywords:
                    # Check if user already has this keyword
                    existing = conn.execute('''
                        SELECT score FROM user_keywords 
                        WHERE user_id = ? AND keyword = ?
                    ''', (user_id, keyword)).fetchone()
                    
                    if existing:
                        # Update existing keyword
                        conn.execute('''
                            UPDATE user_keywords 
                            SET score = score + ?, last_updated = CURRENT_TIMESTAMP
                            WHERE user_id = ? AND keyword = ?
                        ''', (score_change, user_id, keyword))
                    else:
                        # Insert new keyword preference
                        conn.execute('''
                            INSERT INTO user_keywords (user_id, keyword, score)
                            VALUES (?, ?, ?)
                        ''', (user_id, keyword, score_change))
                    
                    conn.commit()
        
        conn.close()
    
    def get_recommendations(self, user_id, limit=5):
        """
        Get personalized recommendations for a user based on their keyword scores.
        """
        conn = self.get_connection()
        
        # Get user's keyword preferences (only positive ones)
        user_keywords = conn.execute('''
            SELECT keyword, score FROM user_keywords 
            WHERE user_id = ? AND score > 0
            ORDER BY score DESC
        ''', (user_id,)).fetchall()
        
        # If user has no preferences yet, return popular or random shows
        if not user_keywords:
            recommendations = conn.execute('''
                SELECT * FROM shows 
                WHERE id NOT IN (
                    SELECT show_id FROM seen_shows WHERE user_id = ?
                )
                ORDER BY RANDOM()
                LIMIT ?
            ''', (user_id, limit)).fetchall()
            conn.close()
            return recommendations
        
        # Get all shows the user hasn't seen
        unseen_shows = conn.execute('''
            SELECT * FROM shows 
            WHERE id NOT IN (
                SELECT show_id FROM seen_shows WHERE user_id = ?
            )
        ''', (user_id,)).fetchall()
        
        # Score each show based on keyword matches
        scored_shows = []
        for show in unseen_shows:
            if show['keywords']:
                show_keywords = [k.strip() for k in show['keywords'].split(',')]
                score = 0
                
                # Add up scores from matching keywords
                for uk in user_keywords:
                    if uk['keyword'] in show_keywords:
                        score += uk['score']
                
                scored_shows.append((score, show))
        
        # Sort by score (highest first) and take top 'limit'
        scored_shows.sort(reverse=True, key=lambda x: x[0])
        recommendations = [show for score, show in scored_shows[:limit]]
        
        conn.close()
        return recommendations
    
    def get_mood_based_recommendations(self, mood, limit=5):
        """
        Simple recommendations based on mood (for new users)
        """
        conn = self.get_connection()
        recommendations = conn.execute('''
            SELECT * FROM shows 
            WHERE mood = ? OR genre = ?
            ORDER BY RANDOM()
            LIMIT ?
        ''', (mood, mood, limit)).fetchall()
        conn.close()
        return recommendations

    def get_collaborative_hint(self, user_id, show_id):
        """
        Advanced: Find similar users and what they liked
        This is a simple version of collaborative filtering
        """
        conn = self.get_connection()
        
        # Find users who liked this show (rated it 4 or 5)
        similar_users = conn.execute('''
            SELECT DISTINCT user_id FROM ratings 
            WHERE show_id = ? AND rating >= 4 AND user_id != ?
        ''', (show_id, user_id)).fetchall()
        
        if not similar_users:
            conn.close()
            return []
        
        # Get shows those similar users liked that this user hasn't seen
        similar_user_ids = [u['user_id'] for u in similar_users]
        placeholders = ','.join(['?'] * len(similar_user_ids))
        
        recommendations = conn.execute(f'''
            SELECT s.*, COUNT(*) as similarity_score
            FROM shows s
            JOIN ratings r ON s.id = r.show_id
            WHERE r.user_id IN ({placeholders})
            AND r.rating >= 4
            AND s.id NOT IN (
                SELECT show_id FROM seen_shows WHERE user_id = ?
            )
            AND s.id NOT IN (
                SELECT show_id FROM ratings WHERE user_id = ?
            )
            GROUP BY s.id
            ORDER BY similarity_score DESC
            LIMIT 5
        ''', (*similar_user_ids, user_id, user_id)).fetchall()
        
        conn.close()
        return recommendations