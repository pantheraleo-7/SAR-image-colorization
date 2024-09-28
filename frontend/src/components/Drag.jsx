import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import './d.css'      /// Add custom styling for the box
import { useState } from "react";
const FileUpload = ({handleImageChange}) => {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const onDrop = useCallback((acceptedFiles) => {
    console.log(acceptedFiles); //testing
    setUploadedFiles(acceptedFiles.map(file=>file.name));
    // Handle file upload logic here
    console.log("sdsd",acceptedFiles)
    handleImageChange(acceptedFiles)

  }, []);
  const handleDropFromOutside = async (e) => {
    // e.preventDefault();
    e.stopPropagation();
    
    // Get the image URL from the drag event
    const imgSrc = e.dataTransfer.getData("text/plain");
    console.log("sd",imgSrc)
    if (imgSrc) {
      // Fetch the image as a Blob from the image URL
      const res=await fetch(imgSrc,{method:'GET'})
      const blob=await res.blob()
      console.log(blob)
      // Set the image source as the drag data
      const file=new File([blob],"dropped-image.jpeg",{type:blob.type})
          setUploadedFiles((prevFiles) => [...prevFiles, file.name]);
          handleImageChange([file]);
          
    }
  }
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': [] },

    multiple: true,
    
  });

  return (
    <div className="upload-box bg-[#F0F0F0] m-10" {...getRootProps()}
    onDrop={handleDropFromOutside}
    onDragOver={(e) => e.preventDefault()} 
    >
      <input {...getInputProps({
        name:'files',
        type:'file',
        // webkitdirectory: 'true', // Allows folder selection
        id:'file',
        className:"pl-70",
      }
      )} />
      {uploadedFiles.length > 0 ? (
        <p className="text-#333333 overflow-auto ">File(s) uploaded: {uploadedFiles.join(", ")}</p> // Display the uploaded file names
      ) : (
        <>
          {isDragActive ? (
            <p className="text-#333333">Drop the folder or images here...</p>
          ) : (
            <>
              <div className="upload-icon ">&#x2193;</div> {/* Optional: Use an SVG icon or custom arrow */}
              <p className="text-#333333">Browse or drag & drop to upload image(s)</p>
            </>
          )}
        </>
      )}
    </div>
  );
};

export default FileUpload;