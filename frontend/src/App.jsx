import { useState, useEffect, Suspense, lazy } from "react";
import FileUpload from "./components/Drag";
import "./components/style.css";
import MainCard from "./components/MainCard";
import Footer from "./components/Footer";
import LoadingBar from "./components/loadingbar";
import ImageCard from "./components/ImageCard";
function App() {
  const ImageComparisonArray = lazy(
    () => import("./components/colorizedImage"),
  );
  const [load, setLoad] = useState(false);
  const [error, seterror] = useState(false);
  const [image, setImage] = useState([]);
  const [ColorizedImage, setColorizedImage] = useState([]);
  const [uploads, setUploads] = useState([]);

  const handleImageChange = (acceptedFiles) => {
    console.log("A", acceptedFiles);
    setUploads(acceptedFiles);
    setImage(acceptedFiles.map((file) => URL.createObjectURL(file)));
    seterror(false)
  };

  useEffect(() => {
    if (image.length > 0) {
      console.log("Selected Image:", image);
    }
  }, [image]);

  const handleImageUpload = async (e) => {
    e.preventDefault();
    if(!uploads.length){
      alert("please enter file")
      return;
    }

    // Start loading
    setLoad(true);

    const formData = new FormData();
    // This adds each file to the FormData object. Using append allows you to add multiple files under the same key
    uploads.forEach((e) => {
      formData.append("files", e);
    });
    console.log("ff", formData.getAll("files"));

    try {
      const api_url = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const res = await fetch(api_url, {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        // "data:image/png;base64," is the prefix that specifies the data is a base64-encoded PNG image
        const filear = await res.json();
        let colorizedImageArray = filear.map(
          (e) => "data:image/png;base64," + e,
        );
        setColorizedImage(colorizedImageArray);
        setUploads([]); // Clear uploads
        seterror(false)
      } else {
        // setLoad(false);
        console.log("Image upload failed");
        seterror(true);
      }
    } catch (error) {
      console.error("Error uploading image:", error);
      seterror(true);
    } finally {
      setLoad(false);
      // Stop loading
      // Stop loading regardless of success or failure
    }
  };
  const handle = () => {

    setImage([]);
    setColorizedImage([]);
  };

  return (
    <>
      <MainCard />
      <div className="text-white dark:bg-[#E0E0E0] flex-1">
        {ColorizedImage.length <= 0 ? (
          <form
            onSubmit={handleImageUpload}
            method="post"
            encType="multipart/form-data"
          >
            <div id="drag" className="flex flex-col items-center ">
              <FileUpload handleImageChange={handleImageChange} />
              <button
                id="color-box"
                className="mb-10 text-white bg-[#007BFF] hover: font-medium rounded-lg text-xl px-4 py-2 text-center dark:bg-blue-600 dark:hover:bg-[#0056b3] dark:focus:ring-blue-800 focus:scale-105" 
                type="submit"
              >
                Colorize
              </button>
            </div>
          </form>
        ) : (
          ""
        )}

<div className="flex flex-wrap justify-center w-full border-box mt-10">
        {ColorizedImage.length ? (
          <button
            className="mb-10 flex item-center justify-center mt-10 w-fit text-white bg-[#007BFF] hover: font-medium rounded-xl px-2  py-2 text-center dark:bg-blue-600 dark:hover:bg-[#0056b3] dark:hover: scale-150"
            onClick={handle}
          >
            <span className="text-bold md:text-sm">
              upload
            </span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 32 32"
              id="upload"
              width="30%"
              height="100%"
              style={{ maxWidth: "30px", maxHeight: "30px", fill: "#ffffff" }}
            >
              <g>
                <path d="M25,19a1,1,0,0,0-1,1v5H8V20a1,1,0,0,0-2,0v5.14A1.93,1.93,0,0,0,8,27H24a1.93,1.93,0,0,0,2-1.86V20A1,1,0,0,0,25,19Z"></path>
                <path d="M16,12.45V22a1,1,0,0,0,2,0V12.45l3.27,3.52a1,1,0,0,0,1.46-1.37l-5-5.38a1,1,0,0,0-1.46,0l-5,5.38a1,1,0,0,0,1.46,1.37Z"></path>
              </g>
            </svg>
          </button>
        ) : (
          ""
        )}
      </div>
        <div className="flex flex-wrap  justify-center w-full border-box">
          {!load && image.length && !ColorizedImage.length && !error
            ? image.map((img, index) => (
              <ImageCard src={img} key={index} title={"original image"} />
            ))
            : ""}

          {error && (
            <div className="error-message text-red-700 font-bold mb-10">
              Image upload failed. Please try again.
            </div>
          )}
          {load && <LoadingBar load={true} count={image.length} />}
          {!load && ColorizedImage.length ? (
            <>
              <Suspense
                fallback={<LoadingBar load={true} count={image.length} />}
              >
                <ImageComparisonArray
                  image={image}
                  ColorizedImage={ColorizedImage}
                  
                />
              </Suspense>
            </>
          ) : null}
        </div>
      </div>
     

      <Footer />
    </>
  );
}

export default App;
