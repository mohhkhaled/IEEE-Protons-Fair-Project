// FastAPI Backend Endpoint Configuration
const API_BASE_URL = ''; // Direct server endpoints as declared in main.py
const CURRENT_SCHOOL_ID = 1; // Set to user's logged-in school_id

// State variables for filter and search
let currentCategory = 'all';
let searchQuery = '';

// Mobile Menu Toggle
function toggleMenu() {
    document.getElementById('navLinks').classList.toggle('show');
}

// Modal Handlers
function openModal() { document.getElementById('postModal').classList.add('active'); }
function closeModal() { document.getElementById('postModal').classList.remove('active'); }

// Fetch announcements from FastAPI REST endpoint
async function fetchAnnouncements() {
    const feed = document.getElementById('announcementsFeed');

    try {
        // Fetch announcements by school ID from FastAPI
        const response = await fetch(`${API_BASE_URL}/announcements/school/${CURRENT_SCHOOL_ID}`);
        if (!response.ok) throw new Error('API server unavailable');
        
        const data = await response.json();

        // Map Backend schema fields (content) to Frontend fields (body) & filter locally
        const mappedData = data.map(item => ({
            id: item.id,
            title: item.title,
            body: item.content, // Maps SQLAlchemy 'content' to UI 'body'
            category: item.category, // Default visual category tag
            author_name: `School #${item.school_id} Admin`,
            author_initials: 'AD',
            school: `School ${item.school_id}`,
            created_at: new Date(item.created_at).toLocaleString(),
            likes: 0
        }));
        const filteredData = mappedData.filter(item => {

            const matchesSearch = 
                post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                post.body.toLowerCase().includes(searchQuery.toLowerCase());

            const matchesCategory = currentCategory === 'all' || item.category === currentCategory;

            return matchesSearch && matchesCategory;
        });
        renderAnnouncements(filteredData);
    } catch (err) {
        console.warn('Backend offline or error occurred. Falling back to local mock state:', err);
        const mockData = getMockData().filter(item => {
            const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                                 item.body.toLowerCase().includes(searchQuery.toLowerCase());
            return matchesSearch;
        });
        renderAnnouncements(mockData);
    }
}

// Render Cards dynamically into HTML
function renderAnnouncements(items) {
    const feed = document.getElementById('announcementsFeed');
    
    if (items.length === 0) {
        feed.innerHTML = `
            <div style="text-align: center; padding: 40px; background: #fff; border-radius: 12px; color: #7f8c8d;">
                <i class="fa-solid fa-folder-open" style="font-size: 32px; margin-bottom: 10px;"></i>
                <p>No announcements found.</p>
            </div>`;
        return;
    }

    feed.innerHTML = items.map(post => `
        <article class="announcement-card category-${post.category}" data-announcement-id="${post.id}">
            <div class="card-top">
                <div class="author-meta">
                    <div class="author-avatar">${post.author_initials || 'AD'}</div>
                    <div class="author-details">
                        <h3>${post.author_name}</h3>
                        <p>${post.created_at} &bull; ${post.school || 'Daresny'}</p>
                    </div>
                </div>
                <span class="category-chip">${post.category}</span>
            </div>
            <h3 class="announcement-title">${post.title}</h3>
            <p class="announcement-body">${post.body}</p>
            <div class="card-actions">
                <div class="action-group">
                    <button class="action-btn" onclick="toggleLike(this, ${post.id})">
                        <i class="fa-regular fa-heart"></i> <span>${post.likes || 0}</span>
                    </button>
                </div>
            </div>
        </article>
    `).join('');
}

// Post a new announcement to FastAPI (POST /announcements/)
async function handleCreatePost(event) {
    event.preventDefault();

    // Align schema with Pydantic AnnouncementCreate in backend
    const payload = {
        title: document.getElementById('postTitle').value,
        content: document.getElementById('postBody').value, // 'content' required by FastAPI
        category: document.getElementById('postCategory').value,
        school_id: CURRENT_SCHOOL_ID
    };

    try {
        const response = await fetch(`${API_BASE_URL}/announcements/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorDetail = await response.json();
            throw new Error(errorDetail.detail || 'Failed to create announcement');
        }

        closeModal();
        document.getElementById('createPostForm').reset();
        fetchAnnouncements(); // Refresh feed automatically after publishing
    } catch (err) {
        alert('Error publishing announcement: ' + err.message);
    }
}

// Filter and Search Helpers
function filterCategory(category, btn) {
    document.querySelectorAll('.tag-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentCategory = category;
    fetchAnnouncements();
}

function handleSearch() {
    searchQuery = document.getElementById('searchInput').value;
    fetchAnnouncements();
}

function toggleLike(btn, id) {
    const countSpan = btn.querySelector('span');
    let count = parseInt(countSpan.innerText);
    btn.classList.toggle('liked');
    if (btn.classList.contains('liked')) {
        btn.querySelector('i').className = 'fa-solid fa-heart';
        countSpan.innerText = count + 1;
    } else {
        btn.querySelector('i').className = 'fa-regular fa-heart';
        countSpan.innerText = count - 1;
    }
}

// Initial Fallback Mock Data
function getMockData() {
    return [
        {
            id: 1,
            title: "Mid-Semester Exam Schedule Revision & Room Allocations",
            body: "Please be advised that the Mid-Semester examination schedule has been updated.",
            category: "urgent",
            author_name: "Administration Office",
            author_initials: "AD",
            school: "School 1",
            created_at: new Date().toLocaleDateString(),
            likes: 24
        }
    ];
}

// Load data on page load
window.addEventListener('DOMContentLoaded', fetchAnnouncements);