import React, { useEffect, useState } from 'react';

const LoadingBar = ({ load, count }) => {
  const [progress, setProgress] = useState(0);

  const startLoading = () => {
    setProgress(0); // Reset progress

    const interval = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress >= 100) {
          clearInterval(interval);
          return 100; // Ensure progress stays at 100%
        }

        let increment = 50 / count;
        if (count > 10) {
          increment = 2; // Lower increment if there are many images
        }
        return Math.min(oldProgress + Math.floor(increment), 100);
      });
    }, 200); // Adjust the interval timing if needed

    // Ensure it completes after 5 seconds (or adapt this duration)
    setTimeout(() => {
      clearInterval(interval);
      setProgress(100); // Force 100% completion after timeout
    }, 5000);
  };

  // This effect runs when `load` changes, so it starts or stops the loading bar
  useEffect(() => {
    if (load) {
      startLoading();
    } else {
      setProgress(0); // Reset progress if load is false
    }
  }, [load, count]); // Watch `load` and `count` changes

  return (
    <>
      {load && (
        <div className="flex flex-col items-center w-8/12 mx-auto">
          <div className="w-full h-5 bg-gray-300 rounded mt-2">
            <div
              className="h-full bg-blue-500 transition-all duration-200"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      )}
    </>
  );
};

export default LoadingBar;
