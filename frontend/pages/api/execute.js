// LearnFlow Code Execution API
// Secure Python code execution with sandboxing

import axios from "axios";

// Backend service mapping
const CODE_EXECUTION_SERVICE =
  process.env.CODE_EXECUTION_SERVICE_URL || "http://localhost:8006/execute";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { code, userId, timeout = 5, memoryLimit = 50 } = req.body;

  if (!code) {
    return res.status(400).json({ error: "Code is required" });
  }

  try {
    // Validate that this is Python code
    if (
      !code.trim().startsWith("import ") &&
      !code.includes("def ") &&
      !code.includes("print(") &&
      !code.includes("for ") &&
      !code.includes("while ") &&
      !code.includes("if ")
    ) {
      return res.status(400).json({ error: "Invalid Python code format" });
    }

    // Call the code execution backend service
    const startTime = Date.now();

    const executionResponse = await axios.post(
      CODE_EXECUTION_SERVICE,
      {
        code,
        user_id: userId || "anonymous",
        timeout: timeout || 5,
        memory_limit: memoryLimit || 50,
      },
      {
        timeout: (timeout || 5) * 2 * 1000, // 2x timeout for safety
      },
    );

    const executionTime = Date.now() - startTime;

    res.status(200).json({
      ...executionResponse.data,
      executionTime,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error("Code execution error:", error);

    // Handle different types of errors
    if (error.response) {
      // Error from backend service
      res.status(error.response.status).json({
        output: "",
        error: error.response.data.error || "Code execution failed",
        execution_time: 0,
        success: false,
        timestamp: new Date().toISOString(),
      });
    } else if (error.request) {
      // Network error
      res.status(503).json({
        output: "",
        error: "Unable to reach code execution service",
        execution_time: 0,
        success: false,
        timestamp: new Date().toISOString(),
      });
    } else {
      // Other errors
      res.status(500).json({
        output: "",
        error: error.message || "Internal server error during code execution",
        execution_time: 0,
        success: false,
        timestamp: new Date().toISOString(),
      });
    }
  }
}
