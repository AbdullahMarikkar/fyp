import { Box } from "@mui/material";
import Image from "./Image";
const ShowImage = ({ images }: any) => {
  const show = (image: any) => {
    return (
      <Box>
        <Image image={image} />
      </Box>
    );
  };
  return (
    <Box
      className="container"
      sx={{
        display: "flex",
        justifyContent: "center",
        borderRadius: "30px",
        flexWrap: "wrap",
        width: "80%",
        margin: "auto",
        padding: "20px",
      }}
    >
      {images.map(show)}
    </Box>
  );
};
export default ShowImage;
