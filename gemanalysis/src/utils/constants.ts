import { SxProps } from "@mui/material";

export const timeout: number = 60000;

export const commonTextFieldStyle = {
  width: "100%",
  marginBottom: "10px",
  background: "#ffffff",

  "& .MuiOutlinedInput-root": {
    "&.Mui-focused fieldset": {
      borderColor: "gold", // Change border color when focused
    },
    "&.Mui-focused:hover fieldset": {
      borderColor: "gold !important", // Change border color on hover while focused
    },
  },
  "& .MuiFormLabel-root": {
    "&.Mui-focused": {
      color: "gold", // Change label color when focused
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
  backgroundColor: "#505050",
  color: "whitesmoke",
  textAlign: "center",
};

export const gridTableItemStyle: SxProps = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: "#B8B8B8",
  padding: { sm: "2px", xs: "2px" },
};

export const gridTableItemTextStyle: SxProps = {
  fontWeight: 500,
  color: "whitesmoke",
  backgroundColor: "rgba(0,223,255,1)",
  width: "100%",
  height: "100%",
  padding: "5px",
  fontSize: { sm: 20, xs: 10 },
  borderRadius: "5px",
  textAlign: "center",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};
