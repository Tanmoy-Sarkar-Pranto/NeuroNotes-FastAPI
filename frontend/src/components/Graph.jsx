import { useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { apiService } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

// Get node color based on type
const getNodeColor = (nodeType) => {
  switch (nodeType) {
    case 'concept': return '#3b82f6'; // blue
    case 'skill': return '#10b981'; // green
    case 'project': return '#f59e0b'; // amber
    case 'resource': return '#8b5cf6'; // purple
    case 'goal': return '#ef4444'; // red
    default: return '#6b7280'; // gray
  }
};

// Get edge color based on relationship type
const getEdgeColor = (relationType) => {
  switch (relationType) {
    case 'prerequisite': return '#ef4444'; // red
    case 'follows': return '#3b82f6'; // blue
    case 'similar': return '#10b981'; // green
    case 'opposite': return '#f59e0b'; // amber
    case 'parent': return '#8b5cf6'; // purple
    case 'child': return '#ec4899'; // pink
    default: return '#6b7280'; // gray
  }
};

const Graph = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);

  // Track changes for saving
  const [originalEdges, setOriginalEdges] = useState([]);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [savingChanges, setSavingChanges] = useState(false);

  const handleLogout = () => {
    logout();
  };

  // Load graph data
  const loadGraphData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all topics
      const topics = await apiService.getTopics();

      // Convert topics to nodes with better positioning
      const nodeList = topics.map((topic, index) => {
        // Use stored position or calculate a better default position
        let position = topic.position;
        if (!position || (position.x === 0 && position.y === 0)) {
          // Create a circular layout for topics without positions
          const angle = (2 * Math.PI * index) / topics.length;
          const radius = Math.min(200 + topics.length * 10, 400);
          position = {
            x: Math.cos(angle) * radius,
            y: Math.sin(angle) * radius,
          };
        }

        return {
          id: topic.id,
          position,
          data: {
            label: topic.title,
            description: topic.description,
            nodeType: topic.node_type,
          },
          type: 'default',
          style: {
            background: getNodeColor(topic.node_type),
            border: '2px solid #1a1a1a',
            borderRadius: '8px',
            padding: '10px',
            fontSize: '12px',
            fontWeight: '500',
            color: '#fff',
            minWidth: '120px',
            textAlign: 'center',
          },
        };
      });

      // Fetch edges for each topic and create edge list
      const edgeList = [];
      for (const topic of topics) {
        try {
          const topicEdges = await apiService.getTopicEdges(topic.id);

          topicEdges.forEach(edge => {
            edgeList.push({
              id: `${topic.id}-${edge.target_topic_id}`,
              source: topic.id,
              target: edge.target_topic_id,
              type: 'smoothstep',
              animated: true,
              label: edge.relation_type || 'related',
              style: {
                stroke: getEdgeColor(edge.relation_type),
                strokeWidth: 2,
              },
              labelStyle: {
                fontSize: '10px',
                fontWeight: '500',
              },
            });
          });
        } catch (err) {
          console.warn(`Failed to fetch edges for topic ${topic.id}:`, err);
        }
      }

      setNodes(nodeList);
      setEdges(edgeList);
      setOriginalEdges(edgeList); // Store original edges for comparison
      setHasUnsavedChanges(false); // Reset unsaved changes
    } catch (err) {
      console.error('Failed to load graph data:', err);
      setError('Failed to load graph data. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadGraphData();
  }, [loadGraphData]);

  // Handle new edge connections
  const onConnect = useCallback(
    (params) => {
      const newEdge = {
        ...params,
        id: `${params.source}-${params.target}`,
        type: 'smoothstep',
        animated: true,
        label: 'related',
        style: {
          stroke: getEdgeColor('related'),
          strokeWidth: 2,
        },
        labelStyle: {
          fontSize: '10px',
          fontWeight: '500',
        },
      };
      setEdges((eds) => addEdge(newEdge, eds));
      setHasUnsavedChanges(true);
    },
    [setEdges]
  );

  // Handle edge deletion
  const onEdgesDelete = useCallback(
    (edgesToDelete) => {
      setEdges((eds) => eds.filter(edge => !edgesToDelete.find(del => del.id === edge.id)));
      setHasUnsavedChanges(true);
    },
    [setEdges]
  );

  // Detect changes in edges
  useEffect(() => {
    if (originalEdges.length > 0) {
      const currentEdgeIds = edges.map(e => e.id).sort();
      const originalEdgeIds = originalEdges.map(e => e.id).sort();
      const hasChanges = JSON.stringify(currentEdgeIds) !== JSON.stringify(originalEdgeIds);
      setHasUnsavedChanges(hasChanges);
    }
  }, [edges, originalEdges]);

  // Handle node click
  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
  }, []);

  // Close node details
  const closeNodeDetails = useCallback(() => {
    setSelectedNode(null);
  }, []);

  // Save changes to the backend
  const saveChanges = useCallback(async () => {
    if (!hasUnsavedChanges) return;

    setSavingChanges(true);
    try {
      // Find added and removed edges
      const currentEdgeIds = edges.map(e => e.id);
      const originalEdgeIds = originalEdges.map(e => e.id);

      const addedEdges = edges.filter(e => !originalEdgeIds.includes(e.id));
      const removedEdges = originalEdges.filter(e => !currentEdgeIds.includes(e.id));

      // Create new edges
      for (const edge of addedEdges) {
        await apiService.createTopicEdge(edge.source, edge.target, edge.label || 'related');
      }

      // Delete removed edges
      for (const edge of removedEdges) {
        await apiService.deleteTopicEdge(edge.source, edge.target);
      }

      // Update original edges to current state
      setOriginalEdges(edges);
      setHasUnsavedChanges(false);
    } catch (err) {
      console.error('Failed to save changes:', err);
      setError('Failed to save changes. Please try again.');
    } finally {
      setSavingChanges(false);
    }
  }, [edges, originalEdges, hasUnsavedChanges]);

  // Discard changes and reload from server
  const discardChanges = useCallback(() => {
    loadGraphData();
  }, [loadGraphData]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading knowledge graph...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={loadGraphData}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Retry
          </button>
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
                <Link to="/graph" className="bg-blue-100 text-blue-700 px-3 py-2 rounded-md text-sm font-medium">
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

      {/* Graph Container */}
      <div className="h-[calc(100vh-4rem)] w-full">
        <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onEdgesDelete={onEdgesDelete}
        onNodeClick={onNodeClick}
        fitView
        snapToGrid
        snapGrid={[20, 20]}
      >
        <Background color="#f1f5f9" />
        <Controls />
        <MiniMap
          nodeColor={(node) => node.style?.background || '#6b7280'}
          nodeStrokeWidth={3}
          zoomable
          pannable
        />

        {/* Legend Panel */}
        <Panel position="top-right" className="bg-white rounded-lg shadow-lg p-4 m-4 max-w-xs">
          <h3 className="font-semibold text-gray-800 mb-3">Knowledge Graph</h3>

          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Node Types</h4>
            <div className="space-y-1 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ background: '#3b82f6' }}></div>
                <span>Concept</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ background: '#10b981' }}></div>
                <span>Skill</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ background: '#f59e0b' }}></div>
                <span>Project</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ background: '#8b5cf6' }}></div>
                <span>Resource</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded" style={{ background: '#ef4444' }}></div>
                <span>Goal</span>
              </div>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Relationships</h4>
            <div className="space-y-1 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-4 h-0.5" style={{ background: '#ef4444' }}></div>
                <span>Prerequisite</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-0.5" style={{ background: '#3b82f6' }}></div>
                <span>Follows</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-0.5" style={{ background: '#10b981' }}></div>
                <span>Similar</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-0.5" style={{ background: '#6b7280' }}></div>
                <span>Related</span>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-gray-200">
            <button
              onClick={loadGraphData}
              className="w-full px-3 py-1.5 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Refresh Graph
            </button>
          </div>
        </Panel>

        {/* Save Changes Panel */}
        {hasUnsavedChanges && (
          <Panel position="top-left" className="bg-yellow-50 border border-yellow-200 rounded-lg shadow-lg p-4 m-4 max-w-sm">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0">
                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-yellow-800 text-sm mb-2">Unsaved Changes</h3>
                <p className="text-yellow-700 text-xs mb-3">
                  You have made changes to the graph connections. Save or discard your changes.
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={saveChanges}
                    disabled={savingChanges}
                    className="flex-1 px-3 py-1.5 text-xs bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {savingChanges ? 'Saving...' : 'Save Changes'}
                  </button>
                  <button
                    onClick={discardChanges}
                    disabled={savingChanges}
                    className="flex-1 px-3 py-1.5 text-xs bg-gray-600 text-white rounded hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Discard
                  </button>
                </div>
              </div>
            </div>
          </Panel>
        )}

        {/* Node Details Modal */}
        {selectedNode && (
          <Panel position="bottom-center" className="bg-white rounded-lg shadow-lg p-4 m-4 max-w-md">
            <div className="flex justify-between items-start mb-3">
              <h3 className="font-semibold text-gray-800">{selectedNode.data.label}</h3>
              <button
                onClick={closeNodeDetails}
                className="text-gray-400 hover:text-gray-600 p-1"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-2 text-sm">
              {selectedNode.data.description && (
                <div>
                  <span className="font-medium text-gray-700">Description:</span>
                  <p className="text-gray-600 mt-1">{selectedNode.data.description}</p>
                </div>
              )}

              <div>
                <span className="font-medium text-gray-700">Type:</span>
                <span className="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                      style={{
                        backgroundColor: getNodeColor(selectedNode.data.nodeType) + '20',
                        color: getNodeColor(selectedNode.data.nodeType)
                      }}>
                  {selectedNode.data.nodeType || 'general'}
                </span>
              </div>

              <div>
                <span className="font-medium text-gray-700">Position:</span>
                <span className="text-gray-600 ml-2">
                  ({Math.round(selectedNode.position.x)}, {Math.round(selectedNode.position.y)})
                </span>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-gray-200">
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    closeNodeDetails();
                    navigate('/topics');
                  }}
                  className="flex-1 px-3 py-1.5 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Edit in Topics
                </button>
                <button
                  onClick={closeNodeDetails}
                  className="px-3 py-1.5 text-xs bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                >
                  Close
                </button>
              </div>
            </div>
          </Panel>
        )}
      </ReactFlow>
      </div>
    </div>
  );
};

export default Graph;