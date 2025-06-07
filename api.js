// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// API Functions for Notes Management

/**
 * Get all notes from the API
 * @returns {Promise<Array>} Array of notes
 */
async function getNotes() {
    try {
        const response = await fetch(`${API_BASE_URL}/notes`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching notes:', error);
        throw error;
    }
}

/**
 * Search notes by query
 * @param {string} query - The search query
 * @returns {Promise<Array>} Array of matching notes
 */
async function searchNotes(query) {
    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error searching notes:', error);
        throw error;
    }
}

/**
 * Create a new note
 * @param {string} title - The note title
 * @param {string} content - The note content
 * @returns {Promise<Object>} Response from API
 */
async function createNote(title, content) {
    try {
        const response = await fetch(`${API_BASE_URL}/notes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                content: content
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error creating note:', error);
        throw error;
    }
}

/**
 * Update an existing note
 * @param {string} id - The note ID
 * @param {string} title - The updated note title
 * @param {string} content - The updated note content
 * @returns {Promise<Object>} Response from API
 */
async function updateNote(id, title, content) {
    try {
        const response = await fetch(`${API_BASE_URL}/notes`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
                title: title,
                content: content
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error updating note:', error);
        throw error;
    }
}

/**
 * Delete a note by ID
 * @param {string} id - The note ID to delete
 * @returns {Promise<Object>} Response from API
 */
async function deleteNoteById(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/notes`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error deleting note:', error);
        throw error;
    }
}

/**
 * Test API connection
 * @returns {Promise<boolean>} True if API is reachable
 */
async function testApiConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/notes`);
        return response.ok;
    } catch (error) {
        console.error('API connection test failed:', error);
        return false;
    }
}

// Export functions for use in other modules (if using ES6 modules)
// export { getNotes, searchNotes, createNote, updateNote, deleteNoteById, testApiConnection, API_BASE_URL }; 