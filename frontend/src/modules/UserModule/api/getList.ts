import fetchApiV1 from "@/api";
import Cookies from "js-cookie";

export default async function getList() {
  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${Cookies.get("token")}`,
    },
  };

  const response: Response = await fetchApiV1("user/list/", options);

  const result = await response.json();
  let res: Array<string> = [];
  for (let obj of result) {
    res.push(obj["phone"]);
  }
  return res;
}
