import React, { useEffect, useState } from 'react';

const LoadingBar = (props) => {
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0);

  const startLoading = () => {
    setLoading(props.load);
    setProgress(0);

    const interval = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress === 100) {
          clearInterval(interval);
          setLoading(false);
          return 100; // Ensure progress stays at 100%
        }
        let min=50/props.count
        if(props.count>10){
          min=2
        }
        return Math.min(oldProgress + Math.floor(min), 100); // Increment progress by 5
      });
    }, 200); // Change interval timing if needed

    // Clear the interval after 5 seconds
    setTimeout(() => {
      clearInterval(interval);
      setLoading(false);
      setProgress(100); // Ensure it reaches 100%
    }, 5000);
  };
  useEffect(()=>{
    if(loading){
      startLoading()
    }
  },[loading])

  return (
    <>
    <div className="flex flex-col items-center w-full max-w-md mx-auto">
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
