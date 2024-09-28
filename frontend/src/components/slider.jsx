import React, { useEffect, useRef } from "react";
import saveAs from 'file-saver';
import { ReactCompareSlider, ReactCompareSliderImage } from "react-compare-slider";

const ImageComparison = (props) => {
  const reactCompareSliderRef = useRef(null); // Create a ref for the slider

  const handleDownload = () => {
    saveAs(props.src2, "colorized.png");
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
    <div className="m-4 image-box gap-2 px-4">
  <div className=" slide-box bg-[#F0F0F0] shadow-lg mb-10 flex flex-col items-center justify-between rounded-lg transition-transform transform hover:scale-105">
    <div className=" text-center p-4 w-full h-3/5 ">
      <ReactCompareSlider
        ref={reactCompareSliderRef}
      // Set a fixed height for better responsiveness
        itemOne={<ReactCompareSliderImage src={props.src1} />}
        itemTwo={<ReactCompareSliderImage src={props.src2} />}
        position={props.position}
        className="compare-slider"
        transition="700ms cubic-bezier(.17,.67,.83,.67)"
      />
      <span className="font-semibold text-lg p-2 mt-2 text-gray-900">
        Colorized Image
      </span>
    </div>
    <div className="m-4 w-full  flex justify-center">
          <button
            className="bg-[#28A745] text-white font-medium rounded-lg text-sm px-6 py-2 "
            onClick={handleDownload}
          >
            Download
          </button>
        </div>
  </div>
</div>

  );
};

export default ImageComparison;
