import axiosInstance from "../utils/axiosService";

export const login = async ({
  email,
  password,
}: {
  email: string;
  password: string;
}) => {
  console.log(email, password);
  const { data, status } = await axiosInstance.post(`/login`, {
    email,
    password,
  });

  console.log("RESPONSE DATA", data, status);

  return data;
};

export const signup = async ({
  email,
  password,
  username,
  mobile,
}: {
  email: string;
  username: string;
  mobile: string;
  password: string;
}) => {
  console.log(email, username, mobile, password);
  const { data, status } = await axiosInstance.post(`/signup`, {
    email,
    name: username,
    mobile: `${mobile}`,
    password,
  });

  console.log("RESPONSE DATA", data, status);

  return data;
};
