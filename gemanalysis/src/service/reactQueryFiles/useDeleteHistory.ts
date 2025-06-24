import { useMutation } from "@tanstack/react-query";
import { toast } from "react-toastify";
import { deleteHistoryRecord } from "../uploadImages";

export function useDeleteHistory() {
  const { mutate: deleteHistoryFn, isPending } = useMutation({
    mutationFn: deleteHistoryRecord,
    onSuccess() {
      toast.success("History Record Deleted Successfully");
    },
    onError() {
      toast.error("Record Deletion Failed, Please Try again");
    },
  });

  return { deleteHistoryFn, isPending };
}
