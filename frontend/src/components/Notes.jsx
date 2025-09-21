import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import NoteForm from './NoteForm';
import TagManagementModal from './TagManagementModal';

const Notes = () => {
  const { user, logout } = useAuth();
  const [notes, setNotes] = useState([]);
  const [topics, setTopics] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal states
  const [showNoteForm, setShowNoteForm] = useState(false);
  const [editingNote, setEditingNote] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [noteToDelete, setNoteToDelete] = useState(null);

  // Tag management states
  const [showTagManagement, setShowTagManagement] = useState(false);
  const [editingTag, setEditingTag] = useState(null);
  const [showTagDeleteModal, setShowTagDeleteModal] = useState(false);
  const [tagToDelete, setTagToDelete] = useState(null);

  // Filter states
  const [selectedTopic, setSelectedTopic] = useState('');
  const [selectedTag, setSelectedTag] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const handleLogout = () => {
    logout();
  };

  const fetchTopics = async () => {
    try {
      const topicsData = await apiService.getTopics();
      setTopics(Array.isArray(topicsData) ? topicsData : []);
    } catch (err) {
      console.error('Failed to fetch topics:', err);
      setTopics([]);
    }
  };

  const fetchTags = async () => {
    try {
      const tagsData = await apiService.getTags();
      setTags(Array.isArray(tagsData) ? tagsData : []);
    } catch (err) {
      console.error('Failed to fetch tags:', err);
      setTags([]);
    }
  };

  const fetchAllNotes = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch notes for all topics
      let allNotes = [];
      for (const topic of topics) {
        try {
          const topicNotes = await apiService.getNotesByTopic(topic.id);
          // Add topic info to each note
          const notesWithTopic = (Array.isArray(topicNotes) ? topicNotes : []).map(note => ({
            ...note,
            topic: topic
          }));
          allNotes = [...allNotes, ...notesWithTopic];
        } catch (err) {
          console.warn(`Failed to fetch notes for topic ${topic.title}:`, err);
        }
      }

      setNotes(allNotes);
    } catch (err) {
      console.error('Failed to fetch notes:', err);
      setError('Failed to load notes. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      await Promise.all([fetchTopics(), fetchTags()]);
    };
    loadData();
  }, []);

  useEffect(() => {
    if (topics.length > 0) {
      fetchAllNotes();
    }
  }, [topics]);

  const handleCreateNote = () => {
    setEditingNote(null);
    setShowNoteForm(true);
  };

  const handleEditNote = (note) => {
    setEditingNote(note);
    setShowNoteForm(true);
  };

  const handleDeleteNote = (note) => {
    setNoteToDelete(note);
    setShowDeleteModal(true);
  };

  const confirmDeleteNote = async () => {
    if (!noteToDelete) return;

    try {
      await apiService.deleteNote(noteToDelete.id);
      setNotes(notes.filter(note => note.id !== noteToDelete.id));
      setShowDeleteModal(false);
      setNoteToDelete(null);
    } catch (err) {
      console.error('Failed to delete note:', err);
      setError('Failed to delete note. Please try again.');
    }
  };

  const handleNoteFormSuccess = () => {
    setShowNoteForm(false);
    setEditingNote(null);
    fetchAllNotes(); // Refresh notes list
  };

  // Tag management functions
  const handleEditTag = (tag) => {
    setEditingTag(tag);
    setShowTagManagement(true);
  };

  const handleDeleteTag = (tag) => {
    setTagToDelete(tag);
    setShowTagDeleteModal(true);
  };

  const confirmDeleteTag = async () => {
    if (!tagToDelete) return;

    try {
      await apiService.deleteTag(tagToDelete.id);
      await fetchTags(); // Refresh tags list
      await fetchAllNotes(); // Refresh notes to update tag associations
      setShowTagDeleteModal(false);
      setTagToDelete(null);
    } catch (err) {
      console.error('Failed to delete tag:', err);
      setError('Failed to delete tag');
    }
  };

  const handleTagFormSuccess = () => {
    setShowTagManagement(false);
    setEditingTag(null);
    fetchTags(); // Refresh tags list
  };

  // Filter notes based on selected filters and search term
  const filteredNotes = notes.filter(note => {
    const matchesTopic = !selectedTopic || note.topic_id === selectedTopic;
    const matchesTag = !selectedTag || (note.tags && note.tags.some(tag => tag.id === selectedTag));
    const matchesSearch = !searchTerm ||
      note.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      note.content?.toLowerCase().includes(searchTerm.toLowerCase());

    return matchesTopic && matchesTag && matchesSearch;
  });

  const getTopicTitle = (topicId) => {
    const topic = topics.find(t => t.id === topicId);
    return topic ? topic.title : 'Unknown Topic';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const truncateContent = (content, maxLength = 150) => {
    if (!content) return '';
    return content.length > maxLength ? content.substring(0, maxLength) + '...' : content;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center space-x-8">
                <h1 className="text-xl font-semibold text-gray-900">NeuroNotes</h1>
                <nav className="flex space-x-4">
                  <Link to="/dashboard" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    Dashboard
                  </Link>
                  <Link to="/topics" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    Topics
                  </Link>
                  <Link to="/notes" className="bg-blue-100 text-blue-700 px-3 py-2 rounded-md text-sm font-medium">
                    Notes
                  </Link>
                  <Link to="/graph" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    Graph
                  </Link>
                </nav>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">Welcome, {user?.username}</span>
                <button
                  onClick={handleLogout}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer"
                >
                  Sign out
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Loading */}
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading notes...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-8">
              <h1 className="text-xl font-semibold text-gray-900">NeuroNotes</h1>
              <nav className="flex space-x-4">
                <Link to="/dashboard" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                  Dashboard
                </Link>
                <Link to="/topics" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                  Topics
                </Link>
                <Link to="/notes" className="bg-blue-100 text-blue-700 px-3 py-2 rounded-md text-sm font-medium">
                  Notes
                </Link>
                <Link to="/graph" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                  Graph
                </Link>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">Welcome, {user?.username}</span>
              <button
                onClick={handleLogout}
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Header */}
          <div className="mb-8">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Notes</h2>
                <p className="mt-1 text-gray-600">Manage your knowledge notes and their tags</p>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => setShowTagManagement(true)}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer"
                >
                  Manage Tags
                </button>
                <button
                  onClick={handleCreateNote}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer"
                >
                  Create Note
                </button>
              </div>
            </div>
          </div>

          {/* Filters */}
          <div className="mb-6 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Search */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
                <input
                  type="text"
                  placeholder="Search notes..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>

              {/* Topic Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Topic</label>
                <select
                  value={selectedTopic}
                  onChange={(e) => setSelectedTopic(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="">All Topics</option>
                  {topics.map(topic => (
                    <option key={topic.id} value={topic.id}>{topic.title}</option>
                  ))}
                </select>
              </div>

              {/* Tag Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tag</label>
                <select
                  value={selectedTag}
                  onChange={(e) => setSelectedTag(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="">All Tags</option>
                  {tags.map(tag => (
                    <option key={tag.id} value={tag.id}>{tag.name}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Tags Quick View */}
          {tags.length > 0 && (
            <div className="mb-6 p-4 bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-sm font-medium text-gray-900">Quick Tag Actions</h3>
                <span className="text-xs text-gray-500">{tags.length} tags total</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {tags.map(tag => (
                  <div
                    key={tag.id}
                    className="inline-flex items-center space-x-1 px-3 py-1 rounded-full text-sm"
                    style={{
                      backgroundColor: tag.color ? `${tag.color}20` : '#f3f4f6',
                      border: `1px solid ${tag.color || '#d1d5db'}`
                    }}
                  >
                    <span
                      className="font-medium"
                      style={{ color: tag.color || '#6b7280' }}
                    >
                      {tag.name}
                    </span>
                    <button
                      onClick={() => handleEditTag(tag)}
                      className="text-gray-400 hover:text-blue-600 ml-1 cursor-pointer"
                      title="Edit tag"
                    >
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      onClick={() => handleDeleteTag(tag)}
                      className="text-gray-400 hover:text-red-600 ml-1 cursor-pointer"
                      title="Delete tag"
                    >
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
              {error}
            </div>
          )}

          {/* Notes Grid */}
          {filteredNotes.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-500">
                {notes.length === 0 ? (
                  <div>
                    <h3 className="text-lg font-medium mb-2">No notes yet</h3>
                    <p className="mb-4">Create your first note to get started.</p>
                    <button
                      onClick={handleCreateNote}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer"
                    >
                      Create Note
                    </button>
                  </div>
                ) : (
                  <div>
                    <h3 className="text-lg font-medium mb-2">No notes match your filters</h3>
                    <p>Try adjusting your search criteria.</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredNotes.map((note) => (
                <div key={note.id} className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                  <div className="p-6">
                    {/* Note Header */}
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-lg font-semibold text-gray-900 truncate">
                        {note.title || 'Untitled Note'}
                      </h3>
                      <div className="flex space-x-1 ml-2">
                        <button
                          onClick={() => handleEditNote(note)}
                          className="text-gray-400 hover:text-blue-600 p-1 rounded cursor-pointer"
                          title="Edit note"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button
                          onClick={() => handleDeleteNote(note)}
                          className="text-gray-400 hover:text-red-600 p-1 rounded cursor-pointer"
                          title="Delete note"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </div>

                    {/* Note Content */}
                    <p className="text-gray-600 text-sm mb-4 leading-relaxed">
                      {truncateContent(note.content)}
                    </p>

                    {/* Topic Badge */}
                    <div className="mb-3">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {getTopicTitle(note.topic_id)}
                      </span>
                    </div>

                    {/* Tags */}
                    {note.tags && note.tags.length > 0 && (
                      <div className="flex flex-wrap gap-1 mb-4">
                        {note.tags.map((tag) => (
                          <span
                            key={tag.id}
                            className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                            style={{
                              backgroundColor: tag.color ? `${tag.color}20` : '#f3f4f6',
                              color: tag.color || '#6b7280'
                            }}
                          >
                            {tag.name}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* URLs */}
                    {note.urls && note.urls.length > 0 && (
                      <div className="mb-4">
                        {note.urls.map((url, index) => (
                          <a
                            key={index}
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 text-xs block truncate"
                          >
                            {url}
                          </a>
                        ))}
                      </div>
                    )}

                    {/* Timestamp */}
                    <div className="text-xs text-gray-500">
                      {note.updated_at !== note.created_at ? 'Updated' : 'Created'}: {formatDate(note.updated_at || note.created_at)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Note Form Modal */}
      {showNoteForm && (
        <NoteForm
          note={editingNote}
          topics={topics}
          tags={tags}
          onSuccess={handleNoteFormSuccess}
          onCancel={() => {
            setShowNoteForm(false);
            setEditingNote(null);
          }}
        />
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && noteToDelete && (
        <div className="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Delete Note</h3>
                <p className="text-sm text-gray-600">This action cannot be undone</p>
              </div>
            </div>

            <p className="text-gray-700 mb-6">
              Are you sure you want to delete <strong>"{noteToDelete.title || 'this note'}"</strong>? This will permanently remove the note and all associated content.
            </p>

            <div className="flex justify-end space-x-3">
              <button
                onClick={() => {
                  setShowDeleteModal(false);
                  setNoteToDelete(null);
                }}
                className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md text-sm font-medium cursor-pointer transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDeleteNote}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md text-sm font-medium cursor-pointer transition-colors"
              >
                Delete Note
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Tag Management Modal */}
      {showTagManagement && (
        <TagManagementModal
          tag={editingTag}
          onSuccess={handleTagFormSuccess}
          onCancel={() => {
            setShowTagManagement(false);
            setEditingTag(null);
          }}
        />
      )}

      {/* Tag Delete Confirmation Modal */}
      {showTagDeleteModal && tagToDelete && (
        <div className="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Delete Tag</h3>
                <p className="text-sm text-gray-600">This action cannot be undone</p>
              </div>
            </div>

            <p className="text-gray-700 mb-6">
              Are you sure you want to delete the tag <strong>"{tagToDelete.name}"</strong>? This will remove the tag from all associated notes.
            </p>

            <div className="flex justify-end space-x-3">
              <button
                onClick={() => {
                  setShowTagDeleteModal(false);
                  setTagToDelete(null);
                }}
                className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md text-sm font-medium cursor-pointer transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDeleteTag}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md text-sm font-medium cursor-pointer transition-colors"
              >
                Delete Tag
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Notes;