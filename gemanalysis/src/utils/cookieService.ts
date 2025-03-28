import Cookie, { CookieSetOptions } from "universal-cookie";

const cookieOptions: CookieSetOptions = {
  path: "/",
  sameSite: "lax",
  secure: false,
  domain: "localhost",
};

const cookies = new Cookie();

export const getAccessToken = (): string => {
  return cookies.get("accessToken") as string;
};

export const getEmail = (): string => {
  return cookies.get("email") as string;
};

export const setAccessTokenToCookie = (accessToken: string): void => {
  cookies.set("accessToken", accessToken, cookieOptions);
};

export const removeAccessTokenFromCookie = (): void => {
  cookies.remove("accessToken", cookieOptions);
};

// export const getRefreshToken = (): string => {
//   return cookies.get("refreshToken") as string;
// };
// export const setRefreshTokenToCookie = (refreshToken: string): void => {
//   cookies.set("refreshToken", refreshToken, cookieOptions);
// };
// export const removeRefreshTokenFromCookie = (): void => {
//   cookies.remove("refreshToken", cookieOptions);
// };
