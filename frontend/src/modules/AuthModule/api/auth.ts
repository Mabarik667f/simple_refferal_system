import fetchApiV1 from "@/api";

export default async function auth(phone: string) {
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ phone: phone }),
  };

  const response: Response = await fetchApiV1("user/auth/", options);

  const result = await response.json();
  return result;
}
