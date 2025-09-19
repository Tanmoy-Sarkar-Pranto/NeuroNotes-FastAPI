import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const TopicForm = ({ topic, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    node_type: '',
    position: { x: 0, y: 0 }
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});
  const [isFormValid, setIsFormValid] = useState(false);

  // Related topics state
  const [availableTopics, setAvailableTopics] = useState([]);
  const [selectedRelatedTopics, setSelectedRelatedTopics] = useState([]);
  const [loadingTopics, setLoadingTopics] = useState(false);

  useEffect(() => {
    if (topic) {
      setFormData({
        title: topic.title || '',
        description: topic.description || '',
        node_type: topic.node_type || topic.nodeType || '',
        position: topic.position || { x: 0, y: 0 }
      });
      // Load existing relationships when editing
      fetchExistingRelationships(topic.id);
    }
  }, [topic]);

  // Fetch available topics for relationships
  useEffect(() => {
    fetchAvailableTopics();
  }, []);

  const fetchAvailableTopics = async () => {
    try {
      setLoadingTopics(true);
      const topics = await apiService.getTopics();
      setAvailableTopics(Array.isArray(topics) ? topics : []);
    } catch (err) {
      console.error('Failed to fetch topics:', err);
      setAvailableTopics([]);
    } finally {
      setLoadingTopics(false);
    }
  };

  const fetchExistingRelationships = async (topicId) => {
    try {
      const edges = await apiService.getTopicEdges(topicId);
      const relationships = (Array.isArray(edges) ? edges : []).map(edge => ({
        topicId: edge.target_topic_id,
        relationshipType: edge.relation_type || 'related'
      }));
      setSelectedRelatedTopics(relationships);
    } catch (err) {
      console.error('Failed to fetch existing relationships:', err);
      setSelectedRelatedTopics([]);
    }
  };

  // Related topics management
  const addRelatedTopic = (topicId, relationshipType = 'related') => {
    if (!selectedRelatedTopics.find(rt => rt.topicId === topicId)) {
      setSelectedRelatedTopics([
        ...selectedRelatedTopics,
        { topicId, relationshipType }
      ]);
    }
  };

  const removeRelatedTopic = (topicId) => {
    setSelectedRelatedTopics(selectedRelatedTopics.filter(rt => rt.topicId !== topicId));
  };

  const updateRelationshipType = (topicId, relationshipType) => {
    setSelectedRelatedTopics(selectedRelatedTopics.map(rt =>
      rt.topicId === topicId ? { ...rt, relationshipType } : rt
    ));
  };

  const getTopicTitle = (topicId) => {
    const topic = availableTopics.find(t => t.id === topicId);
    return topic ? topic.title : 'Unknown Topic';
  };

  // Validation functions
  const validateTitle = (title) => {
    const errors = [];
    if (title.length < 3) {
      errors.push('Title must be at least 3 characters long');
    }
    if (title.length > 100) {
      errors.push('Title must be no more than 100 characters long');
    }
    return errors;
  };

  const validateDescription = (description) => {
    const errors = [];
    if (description && description.length > 500) {
      errors.push('Description must be no more than 500 characters long');
    }
    return errors;
  };

  const validatePosition = (position) => {
    const errors = [];
    if (position.x < -1000 || position.x > 1000) {
      errors.push('X position must be between -1000 and 1000');
    }
    if (position.y < -1000 || position.y > 1000) {
      errors.push('Y position must be between -1000 and 1000');
    }
    return errors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === 'positionX' || name === 'positionY') {
      const coord = name === 'positionX' ? 'x' : 'y';
      setFormData({
        ...formData,
        position: {
          ...formData.position,
          [coord]: parseInt(value) || 0
        }
      });
    } else if (name === 'node_type') {
      setFormData({
        ...formData,
        node_type: value,
      });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  // Real-time validation effect
  useEffect(() => {
    const errors = {};

    if (formData.title) {
      const titleErrors = validateTitle(formData.title);
      if (titleErrors.length > 0) {
        errors.title = titleErrors;
      }
    }

    if (formData.description) {
      const descriptionErrors = validateDescription(formData.description);
      if (descriptionErrors.length > 0) {
        errors.description = descriptionErrors;
      }
    }

    const positionErrors = validatePosition(formData.position);
    if (positionErrors.length > 0) {
      errors.position = positionErrors;
    }

    setFieldErrors(errors);

    // Check if form is valid
    const isValid = formData.title &&
                   Object.keys(errors).length === 0;

    setIsFormValid(isValid);
  }, [formData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!isFormValid) {
      setError('Please fix all form errors before submitting');
      return;
    }

    setLoading(true);

    try {
      const topicData = {
        title: formData.title,
        description: formData.description || null,
        node_type: formData.node_type || null,
        position: formData.position
      };

      // Add related topics data
      if (selectedRelatedTopics.length > 0) {
        topicData.related_topics = selectedRelatedTopics.map(rt => rt.topicId);
        topicData.relation_types = selectedRelatedTopics.map(rt => rt.relationshipType);
      } else if (topic) {
        // If editing and no related topics selected, send empty arrays to clear existing relationships
        topicData.related_topics = [];
        topicData.relation_types = [];
      }

      if (topic) {
        await apiService.updateTopic(topic.id, topicData);
      } else {
        await apiService.createTopic(topicData);
      }

      onSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-lg max-w-md w-full p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          {topic ? 'Edit Topic' : 'Create New Topic'}
        </h3>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Title Field */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              id="title"
              name="title"
              type="text"
              required
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
                fieldErrors.title ? 'border-red-300' : 'border-gray-300'
              }`}
              placeholder="Enter topic title"
              value={formData.title}
              onChange={handleChange}
            />
            {fieldErrors.title && (
              <div className="mt-1 space-y-1">
                {fieldErrors.title.map((error, index) => (
                  <p key={index} className="text-xs text-red-600">{error}</p>
                ))}
              </div>
            )}
          </div>

          {/* Node Type Field */}
          <div>
            <label htmlFor="node_type" className="block text-sm font-medium text-gray-700 mb-1">
              Node Type
            </label>
            <select
              id="node_type"
              name="node_type"
              value={formData.node_type}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">General</option>
              <option value="concept">Concept</option>
              <option value="skill">Skill</option>
              <option value="project">Project</option>
              <option value="resource">Resource</option>
              <option value="goal">Goal</option>
            </select>
          </div>

          {/* Description Field */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              rows={3}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
                fieldErrors.description ? 'border-red-300' : 'border-gray-300'
              }`}
              placeholder="Enter topic description (optional)"
              value={formData.description}
              onChange={handleChange}
            />
            {fieldErrors.description && (
              <div className="mt-1 space-y-1">
                {fieldErrors.description.map((error, index) => (
                  <p key={index} className="text-xs text-red-600">{error}</p>
                ))}
              </div>
            )}
          </div>

          {/* Position Fields */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Graph Position
            </label>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label htmlFor="positionX" className="block text-xs text-gray-600 mb-1">
                  X Position
                </label>
                <input
                  id="positionX"
                  name="positionX"
                  type="number"
                  min="-1000"
                  max="1000"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  value={formData.position.x}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="positionY" className="block text-xs text-gray-600 mb-1">
                  Y Position
                </label>
                <input
                  id="positionY"
                  name="positionY"
                  type="number"
                  min="-1000"
                  max="1000"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  value={formData.position.y}
                  onChange={handleChange}
                />
              </div>
            </div>
            {fieldErrors.position && (
              <div className="mt-1 space-y-1">
                {fieldErrors.position.map((error, index) => (
                  <p key={index} className="text-xs text-red-600">{error}</p>
                ))}
              </div>
            )}
            <p className="text-xs text-gray-500 mt-1">
              Coordinates for graph visualization (-1000 to 1000)
            </p>
          </div>

          {/* Related Topics Section */}
          <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Related Topics
              </label>

              {/* Topic Selection */}
              <div className="mb-3">
                <select
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  onChange={(e) => {
                    if (e.target.value) {
                      addRelatedTopic(e.target.value);
                      e.target.value = ''; // Reset selection
                    }
                  }}
                  disabled={loadingTopics}
                >
                  <option value="">
                    {loadingTopics ? 'Loading topics...' : 'Select a topic to relate'}
                  </option>
                  {availableTopics
                    .filter(t =>
                      !selectedRelatedTopics.find(rt => rt.topicId === t.id) &&
                      (!topic || t.id !== topic.id) // Exclude the topic being edited
                    )
                    .map(availableTopic => (
                      <option key={availableTopic.id} value={availableTopic.id}>
                        {availableTopic.title}
                      </option>
                    ))
                  }
                </select>
              </div>

              {/* Selected Related Topics */}
              {selectedRelatedTopics.length > 0 && (
                <div className="space-y-2">
                  <p className="text-xs text-gray-600 mb-2">Selected Related Topics:</p>
                  {selectedRelatedTopics.map(relatedTopic => (
                    <div key={relatedTopic.topicId} className="flex items-center gap-2 p-2 bg-gray-50 rounded-md">
                      <span className="flex-1 text-sm font-medium text-gray-700">
                        {getTopicTitle(relatedTopic.topicId)}
                      </span>

                      {/* Relationship Type Selector */}
                      <select
                        value={relatedTopic.relationshipType || 'related'}
                        onChange={(e) => updateRelationshipType(relatedTopic.topicId, e.target.value)}
                        className="px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="related">Related</option>
                        <option value="prerequisite">Prerequisite</option>
                        <option value="follows">Follows</option>
                        <option value="similar">Similar</option>
                        <option value="opposite">Opposite</option>
                        <option value="parent">Parent</option>
                        <option value="child">Child</option>
                      </select>

                      {/* Remove Button */}
                      <button
                        type="button"
                        onClick={() => removeRelatedTopic(relatedTopic.topicId)}
                        className="text-red-500 hover:text-red-700 p-1 rounded hover:bg-red-50"
                        title="Remove related topic"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  ))}
                </div>
              )}

              <p className="text-xs text-gray-500 mt-2">
                Related topics help organize knowledge connections in the graph view
              </p>
            </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
              {error}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm font-medium cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !isFormValid}
              className={`flex-1 px-4 py-2 rounded-md text-sm font-medium ${
                isFormValid && !loading
                  ? 'bg-blue-600 hover:bg-blue-700 text-white cursor-pointer'
                  : 'bg-gray-400 text-white cursor-not-allowed'
              }`}
            >
              {loading ? (topic ? 'Updating...' : 'Creating...') : (topic ? 'Update Topic' : 'Create Topic')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TopicForm;
