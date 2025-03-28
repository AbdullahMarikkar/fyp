import {
  Box,
  Button,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { useDropzone } from "react-dropzone";
import ResultModal from "../ResultModal/ResultModal";
import { uploadImageMutation } from "../../service/reactQueryFiles/useUploadImage";
const getColor = (props: any) => {
  if (props.isDragAccept) {
    return "#00e676";
  }
  if (props.isDragReject) {
    return "#ff1744";
  }
  if (props.isFocused) {
    return "#2196f3";
  }
  return "#eeeeee";
};

const gemStones = [
  {
    value: "ruby",
    name: "Ruby",
  },
  {
    value: "blueSapphire",
    name: "Blue Sapphire",
  },
  {
    value: "yellowSapphire",
    name: "Yellow Sapphire",
  },
  {
    value: "greenSapphire",
    name: "Green Sapphire",
  },
  {
    value: "pinkSapphire",
    name: "Pink Sapphire",
  },
];

const DropBoxContainer = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "40px",
  borderWidth: "2px",
  borderRadius: "10px",
  borderColor: (props: any) => getColor(props),
  borderStyle: "dashed",
  backgroundColor: "#EFB6C8",
  color: "black",
  fontWeight: "bold",
  fontSize: "1.4rem",
  outline: "none",
  transition: "border 0.24s ease-in-out",
};

export interface SuccessResult {
  result: string;
  filename: string;
  gemType: string;
}

function DropBox({
  onDrop,
  setImage,
  image,
}: {
  onDrop: any;
  setImage: any;
  image: any;
}) {
  const [gemType, setGemType] = useState("");
  const [imageSent, setImageSent] = useState([]);
  const [resultModalState, setResultModalState] = useState(false);
  const [successMessage, setSuccessMessage] = useState<SuccessResult>({
    result: "",
    filename: "",
    gemType: "",
  });

  const {
    getRootProps,
    getInputProps,
    open,
    isDragAccept,
    isFocused,
    isDragReject,
  } = useDropzone({
    accept: {
      "image/png": [".png"],
      "image/jpg": [".jpeg", ".jpg"],
    },
    onDrop,
    noClick: true,
    noKeyboard: true,
  });

  function closeResultModalState() {
    setResultModalState(false);
    setGemType("");
    setImage([]);
  }

  // const lists = acceptedFiles.map((list) => (
  //   <li key={list.path}>
  //     {list.path} - {list.size} bytes
  //   </li>
  // ));

  const uploadImageFunction = uploadImageMutation();
  const uploadFiles = () => {
    uploadImageFunction.mutate(
      { imageSent, gemType: gemType },
      {
        onSuccess(data: { result: string; filename: string; gemType: string }) {
          console.log("Data", data);
          setSuccessMessage(data);
          setResultModalState(true);
          setGemType("");
        },
      }
    );
  };

  const handleFile = (e: any) => {
    setImageSent(e.target.files[0]);
  };

  const handleChange = (event: SelectChangeEvent) => {
    setGemType(event.target.value as string);
  };
  return (
    <>
      <Box
        className="dropbox"
        sx={{
          textAlign: "center",
          padding: "20px",
          width: "90%",
          margin: "auto",
          marginTop: "20px",
          backgroundColor: "#EFB6C8",
          borderRadius: "10px",
        }}
      >
        <Box sx={{ marginBottom: "20px" }}>
          <InputLabel id="demo-simple-select-label" sx={{ fontSize: "18px" }}>
            Gemstone Type
          </InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={gemType}
            label="Gemstone Type"
            onChange={handleChange}
            sx={{ minWidth: "200px" }}
          >
            {gemStones.map((gem, i) => {
              return (
                <MenuItem value={gem.name} key={i}>
                  {gem.name}
                </MenuItem>
              );
            })}

            {/* <MenuItem value={20}>Twenty</MenuItem>
            <MenuItem value={30}>Thirty</MenuItem> */}
          </Select>
        </Box>
        <Box
          sx={DropBoxContainer}
          className="dropbox"
          {...getRootProps({ isDragAccept, isFocused, isDragReject })}
        >
          <input
            {...getInputProps({
              onChange: handleFile,
            })}
          />
          <Typography sx={{ color: "#8174A0" }}>
            Drag 'n' drop an Image
          </Typography>
          <Button
            type="button"
            className="btn"
            onClick={open}
            style={{
              padding: "15px",
              backgroundColor: "#FFD2A0",
              color: "#8174A0",
              borderRadius: "10px",
              border: "none",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            Click to select file
          </Button>
        </Box>
      </Box>

      {/* <aside>
        {lists.length > 0 && (
          <Typography sx={{ fontWeight: "bold" }}>List</Typography>
        )}
        <Typography>{lists}</Typography>
      </aside> */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          paddingTop: "20px",
        }}
      >
        <Button
          className="upload-btn"
          onClick={() => uploadFiles()}
          variant="contained"
          disabled={image.length === 0 || gemType === ""}
          sx={{ backgroundColor: "#FFD2A0", color: "#8174A0", margin: "10px" }}
        >
          Upload Images
        </Button>
        <Button
          onClick={() => setImage([])}
          disabled={image.length === 0}
          sx={{ backgroundColor: "red", color: "white", margin: "10px" }}
        >
          Remove Image
        </Button>
      </Box>
      <ResultModal
        open={resultModalState}
        close={closeResultModalState}
        sentImage={image}
        message={successMessage}
      />
    </>
  );
}
export default DropBox;
