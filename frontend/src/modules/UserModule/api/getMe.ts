import fetchApiV1 from "@/api";
import Cookies from "js-cookie";

export default async function getMe() {
  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${Cookies.get("token")}`,
    },
  };

  const response: Response = await fetchApiV1(`user/me/`, options);

  const result = await response.json();
  return result;
}
