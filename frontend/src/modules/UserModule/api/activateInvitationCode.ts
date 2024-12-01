import fetchApiV1 from "@/api";
import Cookies from "js-cookie";
import { authStore } from "@/store/authStore";
import { storeToRefs } from "pinia";

export default async function auth(invitation_code: string) {
  const store = authStore();
  const { userId } = storeToRefs(store);
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${Cookies.get("token")}`,
    },
    body: JSON.stringify({
      invitation_code: invitation_code,
      user: userId.value,
    }),
  };

  const response: Response = await fetchApiV1(
    "user/activate-invitation-code/",
    options,
  );
  return response;
}
