import { Box, Typography, TextField } from "@mui/material";

function TextFieldUtil({
  values,
  handleChange,
  handleBlur,
  errors,
  touched,
  type,
  label,
  name,
}: {
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
      <Typography sx={{ color: "purple" }}>Username</Typography>
      <TextField
        label={label}
        type={type}
        name={name}
        value={values}
        onChange={handleChange}
        onBlur={handleBlur}
        sx={{ borderRadius: "20px", border: 1, width: "100%" }}
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
