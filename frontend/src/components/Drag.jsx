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
    handleImageChange(acceptedFiles)

  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': [] },
    multiple: true,
    
  });

  return (
    <div className="upload-box bg-[#F0F0F0] m-10" {...getRootProps()}>
      <input {...getInputProps({
        name:'files',
        type:'file',
        // webkitdirectory: 'true', // Allows folder selection
        id:'file',
        className:"pl-70",
      }
      )} />
      {uploadedFiles.length > 0 ? (
        <p className="text-#333333">File(s) uploaded: {uploadedFiles.join(", ")}</p> // Display the uploaded file names
      ) : (
        <>
          {isDragActive ? (
            <p className="text-#333333">Drop the folder or images here...</p>
          ) : (
            <>
              <div className="upload-icon ">&#x2193;</div> {/* Optional: Use an SVG icon or custom arrow */}
              <p className="text-#333333">Choose a Image(s) or drag it here.</p>
            </>
          )}
        </>
      )}
    </div>
  );
};

export default FileUpload;