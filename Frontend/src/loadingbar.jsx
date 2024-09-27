import React, { useState } from 'react';

const LoadingBar = () => {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const startLoading = () => {
    setLoading(true);
    setProgress(0);

    const interval = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress === 100) {
          clearInterval(interval);
          setLoading(false);
          return 100; // Ensure progress stays at 100%
        }
        return Math.min(oldProgress + 5, 100); // Increment progress by 5
      });
    }, 200); // Change interval timing if needed

    // Clear the interval after 5 seconds
    setTimeout(() => {
      clearInterval(interval);
      setLoading(false);
      setProgress(100); // Ensure it reaches 100%
    }, 5000);
  };

  return (
    <>
    <div className="flex flex-col items-center w-full max-w-md mx-auto">
      <button
        onClick={startLoading}
        disabled={loading}
        className={`px-4 py-2 text-white font-semibold rounded ${
            loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
            } transition-colors duration-300`}
      >
        {loading ? 'Loading...' : 'Start Loading'}
      </button>
      {loading && (
          <div className="w-full h-5 bg-gray-300 rounded mt-2">
          <div
            className="h-full bg-blue-500 transition-all duration-200"
            style={{ width: `${progress}%` }}
            ></div>
        </div>
        
    )}
    </div>
   
    </>
  );
};

export default LoadingBar;
