import { json } from '@sveltejs/kit';
import { resolveConfig } from 'vite';

export async function POST({ request, fetch }) {
  const query = (await request.json()).question;
  let answer;

  // Local: http://127.0.0.1:8000/api/messages/
  // Backend Server: https://ai-engine-api.onrender.com/api/messages/

  try {
    const response = await fetch("http://127.0.0.1:8000/api/messages/", {
      method: 'POST',
      body: JSON.stringify(query),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      return json('description: Invalid API response coming to frontend server from backend , status: ' + response.statusText + ' ('+response.status+')', { status: 200 });
    } else {
      const data = await response.json(); // Properly handling the JSON response
      // Construct the answer in the required format
      answer = data["output"]["response"]; // Assuming output_text contains the response from your API
      return json(answer, { status: 201 }); // Return the custom answer with status 201
    }
  } catch (error) {
    // Provide error feedback
    return json('description: Error sending API request to backend, status: ' + error.message + ' (status: 500)', { status: 200 });
  }
}