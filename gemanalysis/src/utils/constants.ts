import { SxProps } from "@mui/material";

export const timeout: number = 60000;

export const commonTextFieldStyle = {
  width: "100%",
  marginBottom: "10px",
  background: "#ffffff",

  "& .MuiOutlinedInput-root": {
    "&.Mui-focused fieldset": {
      borderColor: "rgb(66, 141, 150)", // Change border color when focused
    },
    "&.Mui-focused:hover fieldset": {
      borderColor: "rgb(66, 141, 150) !important", // Change border color on hover while focused
    },
  },
  "& .MuiFormLabel-root": {
    "&.Mui-focused": {
      color: "rgb(66, 141, 150)", // Change label color when focused
    },
  },
};

export const commonCheckBoxStyle = {
  color: "#ffffff",
  "&:hover": { color: "#cccc00" },
  "&.Mui-checked": {
    color: "gold",
  },
};

export const gridTableHeaderStyle: SxProps = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  padding: { sm: "5px", xs: "1px" },
};

export const gridTableHeaderTextStyle: SxProps = {
  fontWeight: 800,
  width: "100%",
  height: "100%",
  fontSize: { sm: 25, xs: 10 },
  padding: "5px",
  borderRadius: "5px",
  backgroundColor: "rgb(26, 33, 92)",
  color: "whitesmoke",
  textAlign: "center",
};

export const gridTableItemStyle: SxProps = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  // backgroundColor: "#B8B8B8",
  padding: { sm: "2px", xs: "2px" },
};

export const gridTableItemTextStyle: SxProps = {
  fontWeight: 550,
  color: "rgb(33, 39, 95)",
  background:
    "linear-gradient(38deg, rgba(188, 201, 202, 0.97) 0%,rgb(161, 227, 203) 29%, #8adaee 93%)",
  width: "100%",
  height: "100%",
  padding: "5px",
  fontSize: { sm: 20, xs: 10 },
  borderRadius: "25px",
  textAlign: "center",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};
