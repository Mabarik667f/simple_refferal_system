import fetchApiV1 from "@/api";
import Cookies from "js-cookie";

export default async function verifyCode(code: string) {
  const formData: Object = {
    code: code,
    phone: Cookies.get("phone"),
  };
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ...formData }),
  };

  const response: Response = await fetchApiV1("user/verify-code/", options);
  return response;
}
