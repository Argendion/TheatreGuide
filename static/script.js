// Wait for the page to load
document.addEventListener('DOMContentLoaded', function() {
    
    // Handle filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;
            filterShows(filter);
        });
    });
    
    // Handle rating stars
    const stars = document.querySelectorAll('.star');
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            const showId = this.parentElement.dataset.showId;
            const allStars = this.parentElement.querySelectorAll('.star');
            
            // Highlight stars up to the selected one
            allStars.forEach((s, index) => {
                if (index < rating) {
                    s.classList.add('selected');
                } else {
                    s.classList.remove('selected');
                }
            });
            
            // Send rating to server
            fetch('/rate_show', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    show_id: showId,
                    rating: rating
                })
            });
        });
    });
    
    // Handle "Seen It" button
    const seenButtons = document.querySelectorAll('.seen-btn');
    seenButtons.forEach(button => {
        button.addEventListener('click', function() {
            const showId = this.dataset.showId;
            
            fetch('/mark_seen', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    show_id: showId
                })
            });
            
            this.textContent = '✓ Seen!';
            this.disabled = true;
        });
    });
    
    // Handle "Liked" checkbox
    const likedCheckboxes = document.querySelectorAll('.liked-checkbox');
    likedCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const showId = this.dataset.showId;
            const liked = this.checked;
            
            fetch('/liked_show', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    show_id: showId,
                    liked: liked
                })
            });
        });
    });
});

// Function to filter shows by genre/mood
function filterShows(filter) {
    const shows = document.querySelectorAll('.show-card');
    
    shows.forEach(show => {
        if (filter === 'all') {
            show.style.display = 'block';
        } else {
            const genre = show.dataset.genre;
            const mood = show.dataset.mood;
            
            if (genre === filter || mood === filter) {
                show.style.display = 'block';
            } else {
                show.style.display = 'none';
            }
        }
    });
    
    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}