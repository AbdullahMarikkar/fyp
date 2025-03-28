import { useMutation } from "@tanstack/react-query";
import { toast } from "react-toastify";
import { login } from "../authenticate";

export function useLogin() {
  const { mutate: logInFn, isPending } = useMutation({
    mutationFn: login,
    onSuccess() {
      toast.success("User Logged In Successfully");
    },
    onError() {
      toast.error("Log In Failed, Please Try again");
    },
  });

  return { logInFn, isPending };
}
