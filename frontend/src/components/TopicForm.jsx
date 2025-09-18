import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const TopicForm = ({ topic, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    position: { x: 0, y: 0 }
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});
  const [isFormValid, setIsFormValid] = useState(false);

  useEffect(() => {
    if (topic) {
      setFormData({
        title: topic.title || '',
        description: topic.description || '',
        position: topic.position || { x: 0, y: 0 }
      });
    }
  }, [topic]);

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
        position: formData.position
      };

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