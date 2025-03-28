import { useMutation } from "@tanstack/react-query";
import { uploadFiles } from "../uploadImages";
import { toast } from "react-toastify";

export function uploadImageMutation() {
  const uploadImageFn = useMutation({
    mutationFn: uploadFiles,
    onSuccess() {
      toast.success("Image Uploaded Successfully");
    },
    onError() {
      toast.error("Image Upload Failed");
    },
  });

  return uploadImageFn;
}
