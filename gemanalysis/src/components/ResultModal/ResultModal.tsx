import {
  Typography,
  Box,
  Modal,
  SxProps,
  Button,
  FormControlLabel,
  RadioGroup,
  Radio,
} from "@mui/material";
import ShowImage from "../ImageDropZone/ShowImage";
import { useState } from "react";
import { useSendSatisfaction } from "../../service/reactQueryFiles/useSendSatisfaction";
import { SuccessResult } from "../ImageDropZone/DropBox";

const ModalStyle: SxProps = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  borderRadius: "20px",
  padding: "10px",
  width: "350px",
  height: "350px",
  background:
    "linear-gradient(38deg, rgba(223, 232, 233, 0.97) 0%,rgb(173, 223, 205) 29%, #a7dfed 93%)",
};

function ResultModal({
  open,
  close,
  sentImage,
  message,
}: {
  open: boolean;
  close: () => void;
  sentImage: any;
  message: SuccessResult;
}) {
  const [value, setValue] = useState("neutral");

  const { sendSatisfactionFn } = useSendSatisfaction();
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue((event.target as HTMLInputElement).value);
  };

  const handleSubmit = () => {
    sendSatisfactionFn(
      {
        filename: message.filename,
        gem_type: message.gemType,
        result: message.result,
        satisfactory: value,
      },
      {
        onSuccess() {
          close();
        },
      }
    );
  };

  return (
    <Modal open={open && message.result !== undefined} onClose={handleSubmit}>
      <Box sx={ModalStyle}>
        <Typography
          textAlign="center"
          fontSize={"18px"}
          fontWeight={600}
          color="#31606c"
        >
          Result
        </Typography>
        <ShowImage images={sentImage} />
        <Box
          sx={{
            background:
              "linear-gradient(38deg, rgba(180, 180, 180, 0.97) 0%,rgb(141, 224, 193) 29%, #65cce5 93%)",
            borderRadius: "30px",
          }}
        >
          <Typography textAlign={"center"}>
            {message.result.toUpperCase()}
          </Typography>
        </Box>

        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            padding: "10px",
          }}
        >
          <RadioGroup
            aria-labelledby="demo-controlled-radio-buttons-group"
            name="controlled-radio-buttons-group"
            value={value}
            onChange={handleChange}
          >
            <Box sx={{ display: "flex", justifyContent: "center" }}>
              <FormControlLabel
                value="unsatisfied"
                control={<Radio />}
                label="Unsatisfied"
              />
              <FormControlLabel
                value="neutral"
                control={<Radio />}
                label="Neutral"
              />
              <FormControlLabel
                value="Satisfied"
                control={<Radio />}
                label="Satisfied"
              />
            </Box>
          </RadioGroup>
          <Button
            onClick={handleSubmit}
            variant="contained"
            sx={{
              background:
                "linear-gradient(38deg, rgba(151, 141, 141, 0.97) 0%,rgb(93, 189, 154) 29%, #3da4be 93%)",
              borderRadius: "30px",
              width: "50%",
            }}
          >
            Submit
          </Button>
        </Box>
      </Box>
    </Modal>
  );
}

export default ResultModal;
