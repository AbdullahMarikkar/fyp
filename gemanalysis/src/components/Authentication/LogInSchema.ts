import * as Yup from "yup";

const LogInSchema = Yup.object().shape({
  //   firstName: Yup.string()
  //     .min(2, "Too Short!")
  //     .max(50, "Too Long!")
  //     .required("Required"),
  //   lastName: Yup.string()
  //     .min(2, "Too Short!")
  //     .max(50, "Too Long!")
  //     .required("Required"),
  email: Yup.string()
    .email("Invalid email Format")
    .required("Email is Required"),
  password: Yup.string().min(8, "Too Short!").required("Password is Required"),
});

export default LogInSchema;
