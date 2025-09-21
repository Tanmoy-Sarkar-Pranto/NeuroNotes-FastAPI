import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const NoteForm = ({ note, topics, tags, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    topic_id: '',
    urls: [],
    tag_ids: []
  });
  const [urlInput, setUrlInput] = useState('');
  const [newTag, setNewTag] = useState({ name: '', color: '#3b82f6' });
  const [showNewTagForm, setShowNewTagForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (note) {
      setFormData({
        title: note.title || '',
        content: note.content || '',
        topic_id: note.topic_id || '',
        urls: note.urls || [],
        tag_ids: (note.tags || []).map(tag => tag.id)
      });
    }
  }, [note]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleTagToggle = (tagId) => {
    setFormData(prev => ({
      ...prev,
      tag_ids: prev.tag_ids.includes(tagId)
        ? prev.tag_ids.filter(id => id !== tagId)
        : [...prev.tag_ids, tagId]
    }));
  };

  const handleAddUrl = () => {
    if (urlInput.trim() && !formData.urls.includes(urlInput.trim())) {
      setFormData(prev => ({
        ...prev,
        urls: [...prev.urls, urlInput.trim()]
      }));
      setUrlInput('');
    }
  };

  const handleRemoveUrl = (urlToRemove) => {
    setFormData(prev => ({
      ...prev,
      urls: prev.urls.filter(url => url !== urlToRemove)
    }));
  };

  const handleCreateTag = async () => {
    if (!newTag.name.trim()) return;

    try {
      const createdTag = await apiService.createTag(newTag);
      // Add the new tag to the list and select it
      setFormData(prev => ({
        ...prev,
        tag_ids: [...prev.tag_ids, createdTag.id]
      }));
      setNewTag({ name: '', color: '#3b82f6' });
      setShowNewTagForm(false);
      // Trigger parent component to refresh tags list
      window.location.reload(); // Simple way to refresh - in production you'd pass a callback
    } catch (err) {
      console.error('Failed to create tag:', err);
      setError('Failed to create tag. Please try again.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validation
    if (!formData.content.trim()) {
      setError('Content is required.');
      setLoading(false);
      return;
    }
    if (!formData.topic_id) {
      setError('Please select a topic.');
      setLoading(false);
      return;
    }

    try {
      const noteData = {
        title: formData.title.trim() || null,
        content: formData.content.trim(),
        topic_id: formData.topic_id,
        urls: formData.urls.length > 0 ? formData.urls : null,
        tag_ids: formData.tag_ids.length > 0 ? formData.tag_ids : null
      };

      if (note) {
        await apiService.updateNote(note.id, noteData);
      } else {
        await apiService.createNote(noteData);
      }

      onSuccess();
    } catch (err) {
      console.error('Failed to save note:', err);
      setError('Failed to save note. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const isFormValid = formData.content.trim() && formData.topic_id;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              {note ? 'Edit Note' : 'Create Note'}
            </h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600 cursor-pointer"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Title (Optional)
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                placeholder="Enter note title..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>

            {/* Topic Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Topic <span className="text-red-500">*</span>
              </label>
              <select
                name="topic_id"
                value={formData.topic_id}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
                <option value="">Select a topic...</option>
                {topics.map(topic => (
                  <option key={topic.id} value={topic.id}>
                    {topic.title}
                  </option>
                ))}
              </select>
            </div>

            {/* Content */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content <span className="text-red-500">*</span>
              </label>
              <textarea
                name="content"
                value={formData.content}
                onChange={handleInputChange}
                required
                rows={8}
                placeholder="Enter your note content..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm resize-vertical"
              />
            </div>

            {/* URLs */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                URLs
              </label>
              <div className="flex gap-2 mb-2">
                <input
                  type="url"
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                  placeholder="Add a URL..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      handleAddUrl();
                    }
                  }}
                />
                <button
                  type="button"
                  onClick={handleAddUrl}
                  className="px-3 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 text-sm cursor-pointer"
                >
                  Add
                </button>
              </div>
              {formData.urls.length > 0 && (
                <div className="space-y-1">
                  {formData.urls.map((url, index) => (
                    <div key={index} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                      <a
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex-1 text-blue-600 hover:text-blue-800 text-sm truncate"
                      >
                        {url}
                      </a>
                      <button
                        type="button"
                        onClick={() => handleRemoveUrl(url)}
                        className="text-red-500 hover:text-red-700 p-1 cursor-pointer"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Tags */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium text-gray-700">
                  Tags
                </label>
                <button
                  type="button"
                  onClick={() => setShowNewTagForm(!showNewTagForm)}
                  className="text-blue-600 hover:text-blue-800 text-sm cursor-pointer"
                >
                  {showNewTagForm ? 'Cancel' : 'Create New Tag'}
                </button>
              </div>

              {/* New Tag Form */}
              {showNewTagForm && (
                <div className="mb-4 p-3 bg-gray-50 rounded-md">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Tag name"
                      value={newTag.name}
                      onChange={(e) => setNewTag(prev => ({ ...prev, name: e.target.value }))}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
                    />
                    <input
                      type="color"
                      value={newTag.color}
                      onChange={(e) => setNewTag(prev => ({ ...prev, color: e.target.value }))}
                      className="w-12 h-10 border border-gray-300 rounded-md cursor-pointer"
                      title="Choose tag color"
                    />
                    <button
                      type="button"
                      onClick={handleCreateTag}
                      disabled={!newTag.name.trim()}
                      className="px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm cursor-pointer"
                    >
                      Create
                    </button>
                  </div>
                </div>
              )}

              {/* Existing Tags */}
              {tags.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {tags.map(tag => (
                    <button
                      key={tag.id}
                      type="button"
                      onClick={() => handleTagToggle(tag.id)}
                      className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium transition-colors cursor-pointer ${
                        formData.tag_ids.includes(tag.id)
                          ? 'ring-2 ring-blue-500 ring-offset-1'
                          : 'hover:opacity-80'
                      }`}
                      style={{
                        backgroundColor: tag.color ? `${tag.color}20` : '#f3f4f6',
                        color: tag.color || '#6b7280',
                        border: formData.tag_ids.includes(tag.id) ? `2px solid ${tag.color || '#6b7280'}` : '1px solid transparent'
                      }}
                    >
                      {tag.name}
                      {formData.tag_ids.includes(tag.id) && (
                        <svg className="w-4 h-4 ml-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      )}
                    </button>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">No tags available. Create your first tag above.</p>
              )}
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
                {error}
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-3 pt-4">
              <button
                type="submit"
                disabled={!isFormValid || loading}
                className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-4 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer"
              >
                {loading ? 'Saving...' : (note ? 'Update Note' : 'Create Note')}
              </button>
              <button
                type="button"
                onClick={onCancel}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default NoteForm;