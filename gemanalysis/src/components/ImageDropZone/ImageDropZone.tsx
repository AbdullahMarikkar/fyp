import ShowImage from "./ShowImage";
import DropBox from "./DropBox";
import { useCallback, useState } from "react";
function ImageDropZone() {
  // State, browser FileReader and iterating
  const [images, setImages] = useState<any>([]);
  const onDrop = useCallback((acceptedFiles: any) => {
    acceptedFiles.map((file: any, index: any) => {
      const reader = new FileReader();
      reader.onload = function (e: any) {
        setImages(() => [{ id: index, src: e.target.result }]);
      };
      reader.readAsDataURL(file);
      return file;
    });
  }, []);
  return (
    <div className="App">
      <DropBox onDrop={onDrop} setImage={setImages} image={images} />
      <ShowImage images={images} />
    </div>
  );
}
export default ImageDropZone;
