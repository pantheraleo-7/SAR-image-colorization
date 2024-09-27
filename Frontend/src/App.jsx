import { useState, useEffect } from "react";
import FileUpload from "./components/Drag";
import './components/d.css'
import MainCard from "./components/MainCard";
import Footer from "./components/Footer";
import ImageComparison from "./components/slider";
import ImageCard from "./components/ImageCard";
import LoadingBar from "./loadingbar";

function App() {
  //  function base64ToBlob(base64, mimeType) {
  //   // Remove the base64 prefix if it exists
  //   const byteCharacters = atob(base64);
  //   const byteNumbers = new Array(byteCharacters.length);

  //   // Convert each character to a byte number
  //   for (let i = 0; i < byteCharacters.length; i++) {
  //     byteNumbers[i] = byteCharacters.charCodeAt(i);
  //   }
  //   // Convert the byte array to a Uint8Array
  //   const byteArray = new Uint8Array(byteNumbers);

  //   // Create the Blob
  //   return new Blob([byteArray], { type: mimeType });
  // }
  // const [colorizedImageData,setColorizedImageData]=useState([])
  const [flad, setFlad] = useState(true)
  const [image, setImage] = useState([]);
  const [ColorizedImage, setColorizedImage] = useState([]);
  const handleImageChange = (acceptedFiles) => {
    setFlad(false)
    setImage(acceptedFiles.map(file => URL.createObjectURL(file)));
  };

  useEffect(() => {
    if (image) {
      console.log("Selected Image:", image);
    }
  }, [image]);

  const handleImageUpload = async (e) => {
    e.preventDefault();

    let form = document.querySelector('form');
    const formData = new FormData(form);
    console.log("ff", formData.getAll('files'))

    try {
      const api_url = import.meta.env.VITE_API_URL
      setColorizedImage(image);
      const res = await fetch(api_url, {
        method: "POST",
        body: formData,
      });
      if (res.ok) {
        // "data:image/png;base64," is the prefix that specifies the data is a base64-encoded PNG image
        const filear = await res.json();
        let colorizedImageArray = filear.map(
          (e) => "data:image/png;base64," + e
        );
        setColorizedImage(colorizedImageArray);
      } else {
        console.log("Image upload failed");
      }

    } catch (error) {
      console.error("Error uploading image:", error);
    }
  };
  // const f=()=>{
  //   const clipboardItem = new ClipboardItem({ 'image/png': colorizedImageData[0] });
  //  navigator.clipboard.write([clipboardItem])
  // }
  // useEffect(() => {
  //     console.log("Colorized Image Data:", colorizedImageData);
  // }, [colorizedImageData]);

  return (
    <>
    <MainCard />
    <div className="text-white dark:bg-[#E0E0E0]">
    {!(ColorizedImage.length) ?
    (<form
      onSubmit={handleImageUpload}
      method="post"
      encType="multipart/form-data">

      <div id="drag" className=" flex flex-col items-center  ">
        <FileUpload handleImageChange={handleImageChange} />
        <button
          class=" mb-10 text-white bg-[#007BFF] hover: font-medium rounded-lg text-sm px-4 py-2 text-center dark:bg-blue-600 dark:hover:#bg-[#0056b3] dark:focus:ring-blue-800"
          type="submit"
        >
          colorized
        </button> 
      </div>
    </form>): ""}
    <div className="flex m-auto flex-wrap md:flex-nowrap justify-center  w-5/6">
      {image.length ? (image.map((img, index) => {
        if (ColorizedImage[index]) {
          return (
            <ImageComparison src1={img} src2={ColorizedImage[index]} key={index} position={40} flag={true}
            />)
        }
        else {
          return (<ImageCard src={img} alt={"original"} title={"original-image"} />)

        }
      })) : ""}
    </div>
    </div>
    {/* <LoadingBar /> */}
    <Footer />
    </>
  );
}
export default App;