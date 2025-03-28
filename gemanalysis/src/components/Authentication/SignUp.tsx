import { Box, Button, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { Formik } from "formik";
import SignUpSchema from "./SignUpSchema";
import { useSignUp } from "../../service/reactQueryFiles/useSignUp";
import LoadingIndicator from "../../utils/LoadingIndication";
import TextFieldUtil from "./TextFieldUtil";

function SignUp() {
  const navigate = useNavigate();
  const { signUpFn, isPending } = useSignUp();

  if (isPending) return <LoadingIndicator />;

  return (
    <Box
      sx={{
        background:
          "linear-gradient(9deg, rgba(2,0,36,0.3585083691679797) 0%, rgba(153,228,141,0.980357108663778) 40%, rgba(0,223,255,1) 92%)",
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
            Sign Up
          </Typography>
          <Formik
            initialValues={{
              email: "",
              username: "",
              mobile: "",
              password: "",
            }}
            onSubmit={(values, { setSubmitting }) => {
              setTimeout(() => {
                console.log(JSON.stringify(values, null, 2));
                signUpFn({ ...values });
                setSubmitting(false);
              }, 400);
            }}
            validationSchema={SignUpSchema}
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
                  <TextFieldUtil
                    label="Enter Your Email"
                    type="email"
                    name="email"
                    values={values.email}
                    errors={errors.email}
                    handleBlur={handleBlur}
                    handleChange={handleChange}
                    touched={touched.email}
                  />

                  <TextFieldUtil
                    label="Enter Your Username"
                    type="text"
                    name="username"
                    values={values.username}
                    errors={errors.username}
                    handleBlur={handleBlur}
                    handleChange={handleChange}
                    touched={touched.username}
                  />

                  <TextFieldUtil
                    label="Enter Your Mobile Number"
                    type="number"
                    name="mobile"
                    values={values.mobile}
                    errors={errors.mobile}
                    handleBlur={handleBlur}
                    handleChange={handleChange}
                    touched={touched.mobile}
                  />
                  <Box
                    sx={{
                      display: "flex",
                      gap: "5px",
                      flexDirection: "column",
                      alignItems: "flex-start",
                    }}
                  >
                    <Typography sx={{ color: "purple" }}>
                      Mobile Number
                    </Typography>
                    <TextField
                      label="Enter Your Password"
                      type="password"
                      name="password"
                      value={values.password}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      sx={{ borderRadius: "20px", border: 1, width: "100%" }}
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
                    onClick={() => navigate("/login")}
                  >
                    Log In
                  </Button>
                  <Button
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

export default SignUp;
