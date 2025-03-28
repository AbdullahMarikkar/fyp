import { useMutation } from "@tanstack/react-query";
import { sendSatisfaction } from "../uploadImages";
import { toast } from "react-toastify";

export function useSendSatisfaction() {
  const { mutate: sendSatisfactionFn, isPending } = useMutation({
    mutationFn: sendSatisfaction,
    onSuccess() {
      toast.success("Satisfaction Level Sent Successfully");
    },
    onError() {
      toast.error("Couldn't Send Satisfaction Level");
    },
  });

  return { sendSatisfactionFn, isPending };
}
