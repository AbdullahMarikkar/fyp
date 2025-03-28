import { useMutation } from "@tanstack/react-query";
import { toast } from "react-toastify";
import { signup } from "../authenticate";

export function useSignUp() {
  const { mutate: signUpFn, isPending } = useMutation({
    mutationFn: signup,
    onSuccess() {
      toast.success("User Signed Up Successfully");
    },
    onError() {
      toast.error("Sign Up Failed, Please Try again");
    },
  });

  return { signUpFn, isPending };
}
