const API_BASE_URL = "http://127.0.0.1:5000";

export async function getOverview() {
  const response = await fetch(`${API_BASE_URL}/overview`);
  if (!response.ok) {
    throw new Error("Failed to fetch overview data");
  }
  return response.json();
}
