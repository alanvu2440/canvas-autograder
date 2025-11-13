import { useState, useEffect } from "react";

function App() {
  const [backendMessage, setBackendMessage] = useState("");
  const [url, setUrl] = useState("");
  const [urlResponse, setUrlResponse] = useState("");
  const [testCases, setTestCases] = useState([
    { input: "", expected_output: "", points: "" },
  ]);
  const [urlError, setUrlError] = useState("");
  const [report, setReport] = useState(null);
  const [language, setLanguage] = useState("python");
  const [showSignIn, setShowSignIn] = useState(false);

  const testBackend = async () => {
    try {
      const res = await fetch("http://localhost:5001/api/hello");
      const data = await res.json();
      setBackendMessage(data.message);
    } catch (err) {
      console.error("Error calling backend:", err);
      setBackendMessage("Failed to reach backend");
    }
  };

  useEffect(() => {
    if (window.chrome && chrome.storage && chrome.storage.local) {
      chrome.storage.local.get(["submissionUrl"], (result) => {
        if (result.submissionUrl) {
          setUrl(result.submissionUrl);
          setUrlError("");
        } else {
          setUrlError("Could not find a submission URL on this page.");
        }
      });
    } else {
      console.log("error with chrome storage");
    }
  }, []);

  const handleTestCaseChange = (idx, field, value) => {
    const updated = [...testCases];
    updated[idx][field] = value;
    setTestCases(updated);
  };

  const addTestCase = () => {
    setTestCases([
      ...testCases,
      { input: "", expected_output: "", points: "" },
    ]);
  };

  const removeTestCase = (idx) => {
    setTestCases(testCases.filter((_, i) => i !== idx));
  };

  const sendUrl = async () => {
    try {
      const res = await fetch("http://localhost:5001/api/submit-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, test_cases: testCases, language }),
      });
      const data = await res.json();
      setReport(data);
      setUrlResponse("");
    } catch (err) {
      console.error("Error sending URL:", err);
      setReport(null);
      setUrlResponse("Failed to reach backend");
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-8 bg-white shadow-md font-sans">
      <div className="flex justify-end mb-4">
        <button
          onClick={() => setShowSignIn(true)}
          className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-900 transition"
        >
          Sign In
        </button>
      </div>
      {showSignIn && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded shadow-lg p-6 w-80">
            <h2 className="text-lg font-bold mb-4">Sign In</h2>
            <input
              type="text"
              placeholder="Username"
              className="w-full border border-gray-300 rounded px-3 py-2 mb-2"
              disabled
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full border border-gray-300 rounded px-3 py-2 mb-4"
              disabled
            />
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded w-full mb-2"
              disabled
            >
              Sign In
            </button>
            <button
              onClick={() => setShowSignIn(false)}
              className="text-gray-500 hover:text-gray-700 w-full"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
      <img
        src="/canvas-autograder-logo.png"
        alt="Canvas Autograder Logo"
        className="mx-auto mb-2 max-h-24 max-w-xs object-contain p-0"
      />

      <label className="block mb-2 font-semibold text-gray-700">Language</label>
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="w-full border border-gray-300 rounded px-3 py-2 mb-2"
      >
        <option value="python">Python</option>
        <option value="java">Java</option>
        <option value="cpp">C++</option>
      </select>

      <h3 className="text-lg font-semibold mb-2 text-gray-700">Submit a URL</h3>
      <input
        type="text"
        placeholder="Paste a link here..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="w-full border border-gray-300 rounded px-3 py-2 mb-2"
      />

      <h3 className="text-lg font-semibold mb-2 text-gray-700">Test Cases</h3>
      {testCases.map((tc, idx) => (
        <div key={idx} className="flex gap-2 mb-2 items-center">
          <input
            type="text"
            placeholder="Input"
            value={tc.input}
            onChange={(e) => handleTestCaseChange(idx, "input", e.target.value)}
            className="border border-gray-300 rounded px-2 py-1 w-1/3"
          />
          <input
            type="text"
            placeholder="Expected Output"
            value={tc.expected_output}
            onChange={(e) =>
              handleTestCaseChange(idx, "expected_output", e.target.value)
            }
            className="border border-gray-300 rounded px-2 py-1 w-2/3"
          />
          <input
            type="number"
            min="1"
            placeholder="Points"
            value={tc.points}
            onChange={(e) =>
              handleTestCaseChange(idx, "points", e.target.value)
            }
            className="border border-gray-300 rounded px-2 py-1 w-2/6"
          />
          <button
            onClick={() => removeTestCase(idx)}
            className="text-red-500 hover:text-red-700"
            disabled={testCases.length === 1}
          >
            ✕
          </button>
        </div>
      ))}

      <div className="flex flex-col gap-4 mb-4">
        <button
          onClick={addTestCase}
          className="bg-blue-500 text-white px-2 py-1 rounded"
        >
          Add Test Case
        </button>
        <button
          onClick={sendUrl}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
        >
          Submit
        </button>
      </div>

      {report && (
        <div className="mt-6">
          <div className="bg-green-100 border border-green-300 rounded p-4 mb-4">
            <h4 className="text-lg font-bold text-green-700 mb-2">
              Score Report
            </h4>
            <div className="flex gap-6 items-center">
              <span className="text-green-800 font-semibold">
                Earned Points: {report.score.earned_points}
              </span>
              <span className="text-green-800 font-semibold">
                Total Points: {report.score.total_points}
              </span>
              <span className="text-green-800 font-semibold">
                Percentage: {report.score.percentage}%
              </span>
            </div>
            {report.last_commit_date && (
              <div className="mt-2 text-blue-700 font-semibold">
                Last Commit Date:{" "}
                {new Date(report.last_commit_date).toLocaleString()}
              </div>
            )}
          </div>
          <table className="w-full border border-gray-300 rounded mb-4 text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="border px-2 py-1">Input</th>
                <th className="border px-2 py-1">Expected Output</th>
                <th className="border px-2 py-1">Actual Output</th>
                <th className="border px-2 py-1">Points</th>
                <th className="border px-2 py-1">Passed</th>
              </tr>
            </thead>
            <tbody>
              {report.results.map((tc, idx) => (
                <tr
                  key={idx}
                  className={tc.passed ? "bg-green-50" : "bg-red-50"}
                >
                  <td className="border px-2 py-1">{tc.input}</td>
                  <td className="border px-2 py-1">{tc.expected_output}</td>
                  <td className="border px-2 py-1">{tc.output}</td>
                  <td className="border px-2 py-1 text-center">{tc.points}</td>
                  <td className="border px-2 py-1 text-center">
                    {tc.passed ? (
                      <span className="text-green-600 font-bold">✔</span>
                    ) : (
                      <span className="text-red-600 font-bold">✘</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {report.message && (
            <div className="text-gray-600 text-xs">{report.message}</div>
          )}
        </div>
      )}

      {urlResponse && (
        <pre className="bg-gray-50 border border-gray-200 rounded p-3 mt-4 text-sm whitespace-pre-wrap">
          {urlResponse}
        </pre>
      )}

      {urlError && (
        <div style={{ color: "red", marginBottom: "1rem" }}>{urlError}</div>
      )}
    </div>
  );
}

export default App;
