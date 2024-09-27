import ImageComparison from "./slider";
import ImageCard from "./ImageCard";
const ImageNO= (props) => {
return(
    <div className="image-box gap-10 px-10 sm:m-auto sm:flex   sm:justify-center  ">
    <ImageCard src={props.image} alt={"original image"} title={"Original Image"} />
    <ImageCard src={props.colorizedImage || ""} alt={"Colorized image"} title={"Colorized Image"} 
    element={ <button className="nline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700" >
  </button>}
    />
  </div>
)
  };
  
  export default ImageNO;
  