import {saveAs} from 'file-saver';

const ImageCard = (props) => {

  const handleDownload = () => {
    saveAs(props.src,props.src.name)
  }
  return (
    <div className="m-4 image-box gap-2 px-4 border-20">
  <div className="slide-box bg-[#F0F0F0] shadow-lg  flex flex-col items-center justify-between rounded-lg transition-transform transform hover:scale-105">
    <div className="text-center p-4 w-full border-box ">

        <img
          className="rounded-lg"
          src={props.src}
          alt={props.alt}
          ></img>
        <span className="font-medium text-xl p-2 text-black ">
          {props.title}
        </span>
          </div>

      </div>
    </div>
  );
};

export default ImageCard;
