from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from functools import wraps
from recommendation_engine import RecommendationEngine
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Needed for user sessions

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn

# Login required decorator (to protect pages)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page - shows all current shows"""
    conn = get_db()
    shows = conn.execute('SELECT * FROM shows ORDER BY theatre').fetchall()
    conn.close()
    
    # If user is logged in, we might want to show personalized info
    user_profile = None
    if 'user_id' in session:
        # We'll add user-specific data here later
        pass
        
    return render_template('index.html', shows=shows, user=session.get('user_id'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In real app, hash this!
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', 
                           (username,)).fetchone()
        conn.close()
        
        # Super simple auth for learning - DON'T do this in production!
        if user and password == 'password':  # Check properly in real app
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/rate_show', methods=['POST'])
@login_required
def rate_show():
    """Save a user's rating for a show"""
    data = request.get_json()
    show_id = data['show_id']
    rating = data['rating']
    user_id = session['user_id']
    
    conn = get_db()
    # Insert or replace if already exists
    conn.execute('''
        INSERT OR REPLACE INTO ratings (user_id, show_id, rating, timestamp)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (user_id, show_id, rating))
    conn.commit()
    conn.close()
    
    return {'status': 'success'}

@app.route('/mark_seen', methods=['POST'])
@login_required
def mark_seen():
    """Mark a show as seen by the user"""
    data = request.get_json()
    show_id = data['show_id']
    user_id = session['user_id']
    
    conn = get_db()
    conn.execute('''
        INSERT OR REPLACE INTO seen_shows (user_id, show_id, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (user_id, show_id))
    conn.commit()
    conn.close()
    
    return {'status': 'success'}

# Initialize the recommendation engine
rec_engine = RecommendationEngine()

@app.route('/recommendations')
@login_required
def show_recommendations():
    """Show personalized recommendations for the user"""
    user_id = session['user_id']
    
    # Get personalized recommendations
    recommendations = rec_engine.get_recommendations(user_id)
    
    # Also get collaborative hints
    # For this example, we'll use the first seen show as a seed
    conn = get_db()
    seen_show = conn.execute('''
        SELECT show_id FROM seen_shows WHERE user_id = ? 
        ORDER BY timestamp DESC LIMIT 1
    ''', (user_id,)).fetchone()
    conn.close()
    
    collaborative_recs = []
    if seen_show:
        collaborative_recs = rec_engine.get_collaborative_hint(
            user_id, seen_show['show_id']
        )
    
    return render_template('recommendations.html', 
                         recommendations=recommendations,
                         collaborative_recs=collaborative_recs)

# Update your rating route to also update user profile
@app.route('/rate_show', methods=['POST'])
@login_required
def rate_show():
    data = request.get_json()
    show_id = data['show_id']
    rating = data['rating']
    user_id = session['user_id']
    
    conn = get_db()
    conn.execute('''
        INSERT OR REPLACE INTO ratings (user_id, show_id, rating, timestamp)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (user_id, show_id, rating))
    conn.commit()
    conn.close()
    
    # THIS IS THE KEY: Update user profile based on rating
    rec_engine.update_user_profile(user_id, show_id, rating)
    
    return {'status': 'success'}

@app.route('/initial-mood', methods=['POST'])
@login_required
def set_initial_mood():
    """For new users: get recommendations based on mood"""
    data = request.get_json()
    mood = data['mood']
    
    recommendations = rec_engine.get_mood_based_recommendations(mood)
    
    # Convert to list of dicts for JSON response
    recs_list = []
    for rec in recommendations:
        recs_list.append({
            'id': rec['id'],
            'title': rec['title'],
            'theatre': rec['theatre'],
            'genre': rec['genre'],
            'mood': rec['mood']
        })
    
    return {'recommendations': recs_list}