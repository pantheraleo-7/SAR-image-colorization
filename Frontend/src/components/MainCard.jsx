import React from "react";
import "./d.css";

const MainCard = () => {
  const handleDragStart = (e, imgSrc) => {
    console.log("e")
    // Set the image source as the drag data
    e.dataTransfer.setData("text/plain", imgSrc);
  };

  return (
    <div className="bg-[#ffffff] relative ">
      <section className="w-full bg-white dark:bg-[#2A2D3E] md:box-border">
        <div className="img snap-center">
          <img
            src="./assets/a.jpeg"
            alt="adas"
            draggable="true"
            onDragStart={(e) => handleDragStart(e, "./assets/a.jpeg")}
          />
          <div className="ml-12 text-white caption-top absolute bottom-24">
            <h2 className="text-3xl">SAR Images</h2>
          </div>
        </div>
        <div className="img snap-center">
          <img
            src="./assets/c.jpg"
            alt="adas"
            draggable="true"
            onDragStart={(e) => handleDragStart(e, "./assets/c.jpg")}
          />
          <div className="ml-12 text-white caption-top absolute bottom-24">
            <h2 className="text-3xl">SAR Images</h2>
          </div>
        </div>
        <div className="img snap-center">
          <img
            src="./assets/b.jpg"
            alt="adas"
            draggable="true"
            onDragStart={(e) => handleDragStart(e, "./assets/b.jpg")}
          />
          <div className="ml-12 text-white caption-top absolute bottom-24">
            <h2 className="text-3xl">SAR Images</h2>
          </div>
        </div>
        <div className="img snap-center">
          <img
            src="./assets/a.jpeg"
            alt="adas"
            draggable="true"
            onDragStart={(e) => handleDragStart(e, "./assets/a.jpeg")}
          />
          <div className="ml-12 text-white caption-top absolute bottom-24">
            <h2 className="text-3xl w-full">SAR Images</h2>
          </div>
        </div>
      </section>
    </div>
  );
};

export default MainCard;
