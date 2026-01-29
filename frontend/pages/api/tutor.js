// LearnFlow Multi-Agent System API
// Handles routing to different specialized agents with advanced features

import axios from 'axios';

// For server-side environment variables in Next.js
const GROQ_API_KEY = process.env.GROQ_API_KEY;

// Struggle detection algorithm
const detectStruggle = (message, userHistory, responseTime) => {
  const struggleIndicators = [
    'help', 'stuck', 'confused', 'don\'t understand', 'error', 'not working',
    'why', 'how come', 'doesn\'t make sense', 'lost', 'frustrated', 'give up'
  ];

  const lowerMsg = message.toLowerCase();
  const indicatorsFound = struggleIndicators.filter(indicator => lowerMsg.includes(indicator));

  // Check if user is asking same question multiple times
  const repeatedQuestions = userHistory.filter(msg =>
    msg.toLowerCase().includes(lowerMsg) || lowerMsg.includes(msg.toLowerCase())
  ).length > 1;

  // Check response time (if too slow, might indicate confusion)
  const slowResponse = responseTime > 30000; // 30 seconds

  const struggleScore = Math.min(
    1,
    (indicatorsFound.length * 0.3) +
    (repeatedQuestions ? 0.4 : 0) +
    (slowResponse ? 0.3 : 0)
  );

  return {
    isStruggling: struggleScore > 0.5,
    score: struggleScore,
    indicators: indicatorsFound,
    requiresIntervention: struggleScore > 0.7
  };
};

// Agent determination logic
const determineAgent = (message) => {
  const lowerMsg = message.toLowerCase();

  // Concept explanation requests
  if (lowerMsg.includes('what is') || lowerMsg.includes('explain') ||
      lowerMsg.includes('how does') || lowerMsg.includes('concept') ||
      lowerMsg.includes('difference between')) {
    return 'concepts';
  }

  // Debugging requests
  if (lowerMsg.includes('error') || lowerMsg.includes('not working') ||
      lowerMsg.includes('bug') || lowerMsg.includes('fix') ||
      lowerMsg.includes('traceback') || lowerMsg.includes('exception')) {
    return 'debug';
  }

  // Exercise/quiz requests
  if (lowerMsg.includes('practice') || lowerMsg.includes('exercise') ||
      lowerMsg.includes('quiz') || lowerMsg.includes('test') ||
      lowerMsg.includes('problem') || lowerMsg.includes('challenge')) {
    return 'exercise';
  }

  // Progress tracking
  if (lowerMsg.includes('progress') || lowerMsg.includes('how am i doing') ||
      lowerMsg.includes('my stats') || lowerMsg.includes('track')) {
    return 'progress';
  }

  // Code review requests
  if (lowerMsg.includes('review') || lowerMsg.includes('check my code') ||
      lowerMsg.includes('feedback') || lowerMsg.includes('analyze my code')) {
    return 'code-review';
  }

  // Default to triage for general questions
  return 'triage';
};

// Route to appropriate agent with fallback mechanisms
const routeToAgent = async (agentType, requestData) => {
  const { message, userId, context } = requestData;

  // Map agent types to local backend services
  const agentServices = {
    'triage': { url: 'http://localhost:8001/triage', port: 8001 },
    'concepts': { url: 'http://localhost:8000/explain', port: 8000 },
    'debug': { url: 'http://localhost:8005/debug', port: 8005 },
    'exercise': { url: 'http://localhost:8002/generate', port: 8002 },
    'progress': { url: `http://localhost:8003/progress/${userId || 'anonymous'}`, port: 8003 },
    'code-review': { url: 'http://localhost:8004/review', port: 8004 }
  };

  const serviceInfo = agentServices[agentType];
  if (!serviceInfo) {
    throw new Error(`Unknown agent type: ${agentType}`);
  }

  // Prepare request data based on agent type
  let requestDataToSend;
  switch(agentType) {
    case 'concepts':
      requestDataToSend = {
        concept: message,
        difficulty_level: context?.difficulty || 'intermediate',
        user_context: { user_id: userId || 'anonymous', ...context }
      };
      break;
    case 'debug':
      requestDataToSend = {
        error_message: message,
        user_context: { user_id: userId || 'anonymous', ...context }
      };
      break;
    case 'exercise':
      requestDataToSend = {
        topic: message,
        difficulty: context?.difficulty || 'beginner',
        user_context: { user_id: userId || 'anonymous', ...context }
      };
      break;
    case 'code-review':
      requestDataToSend = {
        code: message,
        feedback_type: 'comprehensive',
        user_context: { user_id: userId || 'anonymous', ...context }
      };
      break;
    case 'progress':
      // Already handled in URL construction
      requestDataToSend = {};
      break;
    default:
      requestDataToSend = {
        query: message,
        user_id: userId || 'anonymous',
        ...context
      };
  }

  try {
    const startTime = Date.now();
    let response;

    if (agentType === 'progress') {
      // Special handling for GET requests
      response = await axios.get(serviceInfo.url, { timeout: 10000 });
    } else {
      // POST requests for other agents
      response = await axios.post(serviceInfo.url, requestDataToSend, { timeout: 10000 });
    }

    const endTime = Date.now();
    const responseTime = endTime - startTime;

    // Detect struggle in the user's query
    const struggleDetection = detectStruggle(message, context?.history || [], responseTime);

    return {
      response: response.data,
      agentUsed: agentType,
      responseTime,
      struggleDetection,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error(`Error calling ${agentType} agent:`, error.message);

    // Provide a fallback response using direct Groq API call when backend is unavailable
    if (GROQ_API_KEY) {
      try {
        // Using the same approach as the triage agent
        const groqResponse = await fetch("https://api.groq.com/openai/v1/chat/completions", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${GROQ_API_KEY}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            messages: [
              {
                role: "system",
                content: "You are an expert Python programming tutor. Provide helpful, accurate, and educational responses to students learning Python. If the question is about Python programming, give detailed explanations with code examples. If the question is general, provide the best possible answer."
              },
              {
                role: "user",
                content: message
              }
            ],
            model: "llama-3.1-8b-instant",  // Updated to current supported model
            temperature: 0.7,
            max_tokens: 1000
          })
        });

        if (groqResponse.ok) {
          const groqData = await groqResponse.json();
          const groqMessage = groqData.choices[0]?.message?.content || "I can help you with that! Could you provide more details about your Python question?";

          const fallbackResponse = {
            response: {
              message: groqMessage,
              source: "groq-fallback"
            },
            agentUsed: agentType,
            responseTime: Date.now() - Date.now(), // Not accurate, but for structure
            struggleDetection: detectStruggle(message, context?.history || [], 0),
            timestamp: new Date().toISOString()
          };

          console.log(`Using Groq fallback for ${agentType} agent`);
          return fallbackResponse;
        }
      } catch (groqError) {
        console.error('Groq fallback also failed:', groqError.message);
      }
    }

    // If all fallbacks fail, provide a user-friendly message
    const fallbackResponse = {
      response: {
        message: "I'm currently experiencing some technical difficulties connecting to our AI tutors. Let me try to help you directly.",
        source: "fallback",
        details: error.message
      },
      agentUsed: agentType,
      responseTime: Date.now() - Date.now(),
      struggleDetection: detectStruggle(message, context?.history || [], 0),
      timestamp: new Date().toISOString()
    };

    return fallbackResponse;
  }
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { message, userId, context, agentType } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }

  try {
    // Always route through the triage agent which will determine the appropriate specialist
    const selectedAgent = 'triage';

    // Log the request for analytics
    console.log(`Routing to triage agent for message: ${message.substring(0, 50)}...`);

    // Route to the triage agent which handles routing to appropriate specialist
    const result = await routeToAgent(selectedAgent, {
      message,
      userId,
      context
    });

    res.status(200).json({
      agent: result.response?.agent || selectedAgent,  // Use the agent returned by triage, or default to selected
      response: result.response?.response || result.response, // Extract response from triage result
      responseTime: result.responseTime,
      struggleDetection: result.struggleDetection,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Agent routing error:', error);

    // Even if there's an error, try to provide a helpful response
    res.status(500).json({
      error: 'Failed to process request',
      details: error.message,
      fallbackResponse: "I'm sorry, I'm having trouble connecting to the AI tutors right now. Could you try rephrasing your question?",
      timestamp: new Date().toISOString()
    });
  }
}