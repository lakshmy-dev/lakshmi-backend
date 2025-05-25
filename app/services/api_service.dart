import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String _baseUrl = 'http://192.168.2.93:8000/'; // If testing on your real Android device, we'll update this.

  static Future<void> saveChat(String userInput, String assistantResponse) async {
    final url = Uri.parse('$_baseUrl/save_input/');

    final body = {
      "user_message": userInput,
      "assistant_response": assistantResponse,
      "timestamp": DateTime.now().toIso8601String(),  // current time
    };

    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(body),
    );

    if (response.statusCode == 200) {
      print('✅ Chat saved successfully.');
    } else {
      print('❌ Failed to save chat. Status: ${response.statusCode}');
      print('🔍 Response body: ${response.body}');
    }
  }
}
