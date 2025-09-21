import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const TagManagementModal = ({ tag, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    color: '#3b82f6'
  });
  const [loading, setLoading] = useState(false);
  const [allTags, setAllTags] = useState([]);

  useEffect(() => {
    if (tag) {
      setFormData({
        name: tag.name || '',
        color: tag.color || '#3b82f6'
      });
    }
    fetchTags();
  }, [tag]);

  const fetchTags = async () => {
    try {
      const tagsData = await apiService.getTags();
      setAllTags(Array.isArray(tagsData) ? tagsData : []);
    } catch (err) {
      console.error('Failed to fetch tags:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim() || loading) return;

    setLoading(true);
    try {
      if (tag) {
        // Update existing tag
        await apiService.updateTag(tag.id, formData);
      } else {
        // Create new tag
        await apiService.createTag(formData);
      }
      onSuccess();
    } catch (err) {
      console.error('Failed to save tag:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTag = async (tagToDelete) => {
    if (!window.confirm(`Are you sure you want to delete "${tagToDelete.name}"?`)) {
      return;
    }

    try {
      await apiService.deleteTag(tagToDelete.id);
      await fetchTags(); // Refresh tags list
    } catch (err) {
      console.error('Failed to delete tag:', err);
    }
  };

  const isFormValid = formData.name.trim();

  return (
    <div className="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">
            {tag ? 'Edit Tag' : 'Manage Tags'}
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

        <div className="p-6">
          {/* Tag Creation/Edit Form */}
          <div className="mb-8">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              {tag ? 'Edit Tag' : 'Create New Tag'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="flex space-x-4">
                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tag Name
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="Enter tag name"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Color
                  </label>
                  <input
                    type="color"
                    value={formData.color}
                    onChange={(e) => setFormData(prev => ({ ...prev, color: e.target.value }))}
                    className="w-16 h-10 border border-gray-300 rounded-md cursor-pointer"
                    title="Choose tag color"
                  />
                </div>
                <div className="flex items-end">
                  <button
                    type="submit"
                    disabled={!isFormValid || loading}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium cursor-pointer transition-colors"
                  >
                    {loading ? 'Saving...' : (tag ? 'Update' : 'Create')}
                  </button>
                </div>
              </div>
            </form>
          </div>

          {/* Existing Tags List */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              All Tags ({allTags.length})
            </h3>
            {allTags.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No tags created yet</p>
            ) : (
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {allTags.map(existingTag => (
                  <div
                    key={existingTag.id}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
                  >
                    <div className="flex items-center space-x-3">
                      <div
                        className="w-4 h-4 rounded-full"
                        style={{ backgroundColor: existingTag.color || '#6b7280' }}
                      />
                      <span className="text-sm font-medium text-gray-900">
                        {existingTag.name}
                      </span>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => {
                          setFormData({
                            name: existingTag.name,
                            color: existingTag.color || '#3b82f6'
                          });
                          // Set as editing tag but don't close modal
                        }}
                        className="text-blue-600 hover:text-blue-800 text-sm cursor-pointer"
                        title="Edit tag"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteTag(existingTag)}
                        className="text-red-600 hover:text-red-800 text-sm cursor-pointer"
                        title="Delete tag"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end pt-6 border-t border-gray-200 mt-6">
            <button
              onClick={onCancel}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md text-sm font-medium transition-colors cursor-pointer"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TagManagementModal;