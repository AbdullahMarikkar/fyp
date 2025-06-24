import axiosInstance from "../utils/axiosService";

export const uploadFiles = async ({
  imageSent,
  gemType,
}: {
  imageSent: any;
  gemType: string;
}) => {
  console.log("Image Sent", imageSent);
  const formData = new FormData();
  formData.append("file", imageSent);
  formData.append("gemType", gemType);
  for (let [key, value] of formData.entries()) {
    console.log(`${key}:`, value);
  }
  // formData.append("key", "Your Api key goes here");
  const { data, status } = await axiosInstance.post(`/classify`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  console.log("Status", status);

  return data;
};

export const sendSatisfaction = async ({
  filename,
  result,
  satisfactory,
  gem_type,
}: {
  filename: string;
  result: string;
  satisfactory: string;
  gem_type: string;
}) => {
  console.log(
    "Send Satisfaction Params",
    filename,
    result,
    satisfactory,
    gem_type
  );

  const { data } = await axiosInstance.post("/users/history/save", {
    filename,
    result,
    satisfactory,
    gem_type,
  });

  return data;
};

export const getHistory = async () => {
  const { data } = await axiosInstance.get("/users/history");

  return data;
};

export const deleteHistoryRecord = async ({ id }: { id: number }) => {
  const { data } = await axiosInstance.delete(`/users/history/${id}`);

  return data;
};
