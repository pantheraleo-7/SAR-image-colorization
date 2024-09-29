import ImageComparison from "./slider";
function ImageComparisonArray(props) {
    const { image } = props
    return (
        <>
            {
                image.map((img, index) => (
                    <ImageComparison src1={img} src2={props.ColorizedImage[index]} key={index} position={40} flag={true} />))
            }
        </>


    )
}
export default ImageComparisonArray;