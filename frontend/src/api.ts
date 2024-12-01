export default async function fetchApiV1(
  endpoint: string,
  options: {
    method: string;
    headers?: object;
    body?: any;
  },
): Promise<Response> {
  try {
    const response = await fetch(`/v1/${endpoint}`, {
      method: options.method,
      headers: {
        ...options.headers,
      },
      body: options.body,
    });

    return response;
  } catch (error) {
    throw error;
  }
}
