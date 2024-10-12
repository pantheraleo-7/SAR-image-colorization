import ImageComparison from "./Slider";

function ImageComparisonArray(props) {
  const { image } = props;
  return (
    <>
      {image.map((img, index) => (
        <ImageComparison
          src1={img}
          src2={props.ColorizedImage[index]}
          key={index}
          position={40}
          flag={true}
          index={index}
        />
      ))}
    </>
  );
}

export default ImageComparisonArray;
