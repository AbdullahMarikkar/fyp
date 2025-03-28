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
  backgroundColor: "#FFD2A0",
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
        <Typography textAlign="center">This is Result Modal</Typography>
        <ShowImage images={sentImage} />
        <Typography>{message.result}</Typography>

        <Box sx={{ display: "flex", flexDirection: "column" }}>
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
          <Button onClick={handleSubmit}>Submit</Button>
        </Box>
      </Box>
    </Modal>
  );
}

export default ResultModal;
