import React from "react";
import "./d.css";
import firstImage from '/assets/a.jpeg';
import secondImage from '/assets/b.jpeg';
import thirdImage from '/assets/c.jpeg';
import { Splide, SplideSlide } from '@splidejs/react-splide';
import '@splidejs/splide/dist/css/splide.min.css';

const MainCard = () => {
  const handleDragStart = async (e, imgSrc) => {
    e.preventDefault(); // Prevent default behavior for drag events
    console.log(imgSrc);
    
    try {
      const res = await fetch(imgSrc, { method: 'GET' });
      if (!res.ok) throw new Error('Network response was not ok');
      
    
      e.dataTransfer.setData("text/plain", `http://localhost/assets/${imgSrc}`);
    } catch (error) {
      console.error("Error fetching the image:", error);
    }
  };

  const imagesHeader = [
    {
      "name": firstImage,
      "caption": "Drag the slider to see image transformation.",
      "description": "SAR Imaging for Precise Terrain Mapping"
    },
    {
      "name": secondImage,
      "caption": "Drag the slider to see image transformation.",
      "description": "Monitor Environmental Changes with SAR Data"
    },
    {
      "name": thirdImage,
      "caption": "Drag the slider to see image transformation.",
      "description": "SAR for Disaster Management and Monitoring"
    },
    {
      "name": firstImage,
      "caption": "Drag the slider to see image transformation.",
      "description": "Enhanced Image Analysis with SAR Technology"
    }
  ];

  return (
    <div className="bg-[#ffffff] relative ">
      <section className="w-full bg-white dark:bg-[#2A2D3E] ">
        <Splide
          options={{
            width: "100%",
            gap: '1rem',
            arrows: true,
            drag: true,
          }}
        >
          {imagesHeader.map((image, index) => (
            <SplideSlide key={index}>
              <div className="img relative">
                <img
                  src={image.name}
                  alt={image.description} // Improved alt text
                  draggable="true"
                  onDragStart={(e) => handleDragStart(e, image.name)}
                  className="w-full h-auto" // Add class for responsive image
                />
                <div className="ml-5 text-white absolute bottom-11">
                  <h2 className="text-3xl font-semibold">{image.description}</h2>
                  <h4>{image.caption}</h4>
                </div>
              </div>
            </SplideSlide>
          ))}
        </Splide>
      </section>
    </div>
  );
};

export default MainCard;
