import { apiClient, extractError } from "./client";
import type { ChatMessage } from "../types";

export async function chatWithFile(
  message: string,
  fileContext: string,
  conversationHistory: ChatMessage[]
): Promise<string> {
  try {
    const response = await apiClient.post<{ answer: string }>("/api/chat", {
      message,
      file_context: fileContext,
      conversation_history: conversationHistory,
    });
    return response.data.answer;
  } catch (error) {
    throw new Error(extractError(error, "Chat request failed."));
  }
}
