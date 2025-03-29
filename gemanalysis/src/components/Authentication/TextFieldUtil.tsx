import { Box, Typography, TextField } from "@mui/material";
import { commonTextFieldStyle } from "../../utils/constants";

function TextFieldUtil({
  fieldName,
  values,
  handleChange,
  handleBlur,
  errors,
  touched,
  type,
  label,
  name,
}: {
  fieldName: string;
  values: string | undefined;
  handleChange: any;
  handleBlur: any;
  errors: string | undefined;
  touched: boolean | undefined;
  type: string;
  label: string;
  name: string;
}) {
  return (
    <Box
      sx={{
        display: "flex",
        gap: "5px",
        flexDirection: "column",
        alignItems: "flex-start",
      }}
    >
      <Typography sx={{ color: "purple" }}>{fieldName}</Typography>
      <TextField
        label={label}
        type={type}
        name={name}
        value={values}
        onChange={handleChange}
        onBlur={handleBlur}
        sx={commonTextFieldStyle}
      />
      {errors && touched && (
        <Typography sx={{ fontSize: "10px", color: "red" }}>
          {errors}
        </Typography>
      )}
    </Box>
  );
}

export default TextFieldUtil;
