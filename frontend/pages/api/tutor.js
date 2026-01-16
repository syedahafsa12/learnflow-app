// API route to connect with the backend tutor services
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { query, userId, service } = req.body;

  try {
    let backendResponse;

    // Determine which backend service to call based on the service parameter
    switch(service) {
      case 'triage':
        // Call triage agent to determine which specialist to use
        backendResponse = await axios.post('http://localhost:8000/triage', {
          query: query,
          user_id: userId || 'anonymous'
        });
        break;

      case 'concepts':
        // Call concepts agent
        backendResponse = await axios.post('http://localhost:8001/explain', {
          concept: query,
          difficulty_level: 'intermediate',
          user_context: { user_id: userId || 'anonymous' }
        });
        break;

      case 'debug':
        // Call debug agent
        backendResponse = await axios.post('http://localhost:8003/debug', {
          error_message: query,
          user_context: { user_id: userId || 'anonymous' }
        });
        break;

      case 'exercise':
        // Call exercise agent
        backendResponse = await axios.post('http://localhost:8004/generate', {
          topic: query,
          difficulty: 'beginner',
          user_context: { user_id: userId || 'anonymous' }
        });
        break;

      case 'progress':
        // Call progress agent
        if (query === 'get') {
          backendResponse = await axios.get(`http://localhost:8005/progress/${userId || 'anonymous'}`);
        } else {
          backendResponse = { data: { message: 'Invalid progress query' } };
        }
        break;

      default:
        return res.status(400).json({ message: 'Invalid service specified' });
    }

    res.status(200).json({
      success: true,
      data: backendResponse.data
    });
  } catch (error) {
    console.error('Error calling backend service:', error.message);
    res.status(500).json({
      success: false,
      error: 'Failed to communicate with backend service',
      details: error.message
    });
  }
}