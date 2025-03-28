import { Box, Button, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { Formik } from "formik";
import LogInSchema from "./LogInSchema";
import { useLogin } from "../../service/reactQueryFiles/useLogin";
import { commonTextFieldStyle } from "../../utils/constants";
import LoadingIndicator from "../../utils/LoadingIndication";

function Login() {
  const navigate = useNavigate();
  const { logInFn, isPending } = useLogin();
  // TODO : Increase Model Accuracy by Adding more Data, and Increase the Dataset by Manually Rotating, Resizing current Images
  // TODO : Currently On Page 4 of Natural Sapphire ( No Enhancement)
  // TODO : Implement CICD Pipeline
  // TODO : Create Docker Images and Deploy
  // TODO : Modify UI
  if (isPending) return <LoadingIndicator />;

  return (
    <Box
      sx={{
        background:
          "linear-gradient(45deg, rgba(2,0,36,1) 0%, rgba(141,228,219,1) 31%, rgba(0,212,255,1) 93%)",
        minWidth: "100vh",
        minHeight: "100vh",
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh",
          minWidth: "100vh",
        }}
      >
        <Box
          sx={{
            backgroundColor: "white",
            width: "50%",
            height: "30%",
            borderRadius: "20px",
          }}
        >
          <Typography
            sx={{ color: "purple", fontSize: "25px" }}
            textAlign="center"
          >
            Login
          </Typography>
          <Formik
            initialValues={{ email: "", password: "" }}
            onSubmit={(values, { setSubmitting }) => {
              console.log(JSON.stringify(values, null, 2));
              logInFn(values, {
                onSuccess() {
                  navigate("/");
                },
              });
              setSubmitting(false);
            }}
            validationSchema={LogInSchema}
          >
            {({
              values,
              errors,
              touched,
              handleChange,
              handleBlur,
              handleSubmit,
            }) => (
              <form onSubmit={handleSubmit}>
                <Box
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "10px",
                    margin: "10px",
                  }}
                >
                  <Box
                    sx={{
                      display: "flex",
                      gap: "5px",
                      flexDirection: "column",
                      alignItems: "flex-start",
                    }}
                  >
                    <Typography sx={{ color: "purple" }}>Email</Typography>
                    <TextField
                      label="Enter Your Email"
                      type="email"
                      name="email"
                      value={values.email}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      sx={commonTextFieldStyle}
                    />
                    {errors.email && touched.email && (
                      <Typography sx={{ fontSize: "10px", color: "red" }}>
                        {errors.email}
                      </Typography>
                    )}
                  </Box>
                  <Box
                    sx={{
                      display: "flex",
                      gap: "5px",
                      flexDirection: "column",
                      alignItems: "flex-start",
                    }}
                  >
                    <Typography sx={{ color: "purple" }}>Password</Typography>
                    <TextField
                      label="Enter Your Password"
                      type="password"
                      name="password"
                      value={values.password}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      sx={commonTextFieldStyle}
                    />
                    {errors.password && touched.password && (
                      <Typography sx={{ fontSize: "10px", color: "red" }}>
                        {errors.password}
                      </Typography>
                    )}
                  </Box>
                </Box>

                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: "50px",
                  }}
                >
                  <Button
                    variant="contained"
                    sx={{ margin: "10px", background: "cyan" }}
                    onClick={() => navigate("/signup")}
                  >
                    Sign Up
                  </Button>
                  <Button
                    disabled={
                      (errors.email as unknown as boolean) ||
                      (errors.password as unknown as boolean) ||
                      values.password == "" ||
                      values.email == ""
                    }
                    variant="contained"
                    type="submit"
                    sx={{ margin: "10px" }}
                  >
                    Submit
                  </Button>
                </Box>
              </form>
            )}
          </Formik>
        </Box>
      </Box>
    </Box>
  );
}

export default Login;
