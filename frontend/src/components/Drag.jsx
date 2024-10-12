import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import "./style.css"; // Add custom styling for the box

const FileUpload = ({ handleImageChange }) => {
  const [uploadedFiles, setUploadedFiles] = useState([]);

  // // Function to handle files dropped directly
  // const handleDropFromOutside = async (e) => {
  //   e.preventDefault();

  //   // Get the image URL from the drag event
  //   const imgSrc = e.dataTransfer.getData("text/plain");
  //   console.log("Dropped image URL:", imgSrc);

  //   if (imgSrc) {
  //     try {
  //       // Fetch the image as a Blob from the image URL
  //       const res = await fetch(imgSrc, { method: "GET" });
  //       if (!res.ok) throw new Error("Network response was not ok");
  //       const blob = await res.blob();

  //       // Create a File object
  //       const file = new File([blob], "dropped-image.jpeg", {
  //         type: blob.type,
  //       });

  //       // Update the state and call the handler
  //       setUploadedFiles((prevFiles) => [...prevFiles, file.name]);
  //       handleImageChange([file]);
  //     } catch (error) {
  //       console.error("Error fetching the image:", error);
  //     }
  //   }
  // };

  const onDrop = useCallback(
    (acceptedFiles) => {
      console.log("Files accepted:", acceptedFiles); // testing
      setUploadedFiles(acceptedFiles.map((file) => file.name));
      handleImageChange(acceptedFiles);
    },
    [handleImageChange],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    multiple: true,
  });

  return (
    <div
      className="upload-box bg-[#F0F0F0] m-10"
      {...getRootProps()}
      // onDrop={handleDropFromOutside} // Handle drops from outside
      // onDragOver={(e) => e.preventDefault()} // Prevent default behavior for drag events
    >
      <input
        {...getInputProps({
          name: "files",
          type: "file",
          id: "file",
          className: "pl-70",
        })}
      />
      {uploadedFiles.length > 0 ? (
        <p className="text-#333333 overflow-auto ">
          File(s) uploaded: {uploadedFiles.join(", ")}
        </p> // Display the uploaded file names
      ) : (
        <>
          {isDragActive ? (
            <p className="text-#333333">Drop the folder or images here...</p>
          ) : (
            <>
              <div className="upload-icon ">&#x2193;</div>{" "}
              {/* Optional: Use an SVG icon or custom arrow */}
              <p className="text-#333333">
                Browse or drag & drop to upload image(s)
              </p>
            </>
          )}
        </>
      )}
    </div>
  );
};

export default FileUpload;
