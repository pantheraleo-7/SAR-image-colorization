import React, { useEffect, useRef } from "react";
import saveAs from 'file-saver';
import { ReactCompareSlider, ReactCompareSliderImage } from "react-compare-slider";

const ImageComparison = (props) => {
  const reactCompareSliderRef = useRef(null); // Create a ref for the slider

  const handleDownload = () => {
    saveAs(props.src2, `colorized${(props.index)+1}.png`);
  };

  useEffect(() => {
    const fireTransition = async () => {
      await new Promise(resolve => setTimeout(() => {
        reactCompareSliderRef.current?.setPosition(90);
        resolve(true);
      }, 750));
      await new Promise(resolve => setTimeout(() => {
        reactCompareSliderRef.current?.setPosition(10);
        resolve(true);
      }, 750));
      await new Promise(resolve => setTimeout(() => {
        reactCompareSliderRef.current?.setPosition(30);
        resolve(true);
      }, 750));
    };
    if (props.flag) {
      console.log(props.flag)
      fireTransition(); // Trigger the transition if the images are different
    }
  }, []); // Run this effect once on mount

  return (
    <div className="m-4 image-box1 gap-2 ">
      <div className=" slide-box1 bg-[#F0F0F0] shadow-lg mb-10 flex flex-col justify-between rounded-lg transition-transform transform hover:scale-105">
        <div className=" text-center p-4 w-full  ">
          <ReactCompareSlider
            changePositionOnHover={true}
            ref={reactCompareSliderRef}
            style={{ width: "100%", height: "300px", flexGrow: 1 }}
            itemOne={<ReactCompareSliderImage src={props.src1} />}
            itemTwo={<ReactCompareSliderImage src={props.src2} />}
            position={props.position}
            className="compare-slider"
            transition="700ms cubic-bezier(.17,.67,.83,.67)"
          />
          <div className=" flex justify-center mt-5 gap-5">
            <div className="w-3/4 font-semibold text-lg ml-7  text-gray-900">
          {props.index+1}.colorized.png
            </div>
          <div className="w-full h-full  flex items-center border-box">
          <button
            className="bg-[#28A745]  flex justify-center text-white font-medium rounded-lg   border-box"
            onClick={handleDownload}
          >
          <svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  id="download"
  width="100%"
  height="100%"
  
  style={{ maxWidth: "30px",fill:"white"}}  // Dynamic max sizes for responsiveness
>
  <g>
    <path d="M25,19a1,1,0,0,0-1,1v5H8V20a1,1,0,0,0-2,0v5.14A1.93,1.93,0,0,0,8,27H24a1.93,1.93,0,0,0,2-1.86V20A1,1,0,0,0,25,19Z"></path>
    <path d="M15.27,20.68l0,0a1.2,1.2,0,0,0,.26.18l0,0h0A1,1,0,0,0,16,21a1,1,0,0,0,.38-.08l.12-.07a1.13,1.13,0,0,0,.18-.12l0,0,0,0,5-5.38a1,1,0,1,0-1.46-1.37L17,17.45V6a1,1,0,0,0-2,0V17.45l-3.27-3.52a1,1,0,1,0-1.46,1.37Z"></path>
  </g>
</svg>

          </button>
        </div>
        </div>
        </div>
       
      </div>
    </div>

  );
};

export default ImageComparison;
