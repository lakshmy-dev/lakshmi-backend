import 'dart:convert';
import 'package:http/http.dart' as http;

class SemanticService {
  static const String _baseUrl = 'http://192.168.2.94:8000'; // Local backend

  static Future<List<Map<String, dynamic>>> getTagsFromText(String inputText) async {
    try {
      final url = Uri.parse('$_baseUrl/semantic/match');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'user_input': inputText}),
      );

      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body);
        final matches = decoded['matches'] as List<dynamic>;

        return matches.map((m) {
          return {
            'tag': m['tag'] ?? '',
            'score': (m['score'] ?? 0.1).toDouble(),
            'category': m['category'] ?? 'unknown',
          };
        }).toList();
      } else {
        print('❌ Semantic API failed with status: ${response.statusCode}');
      }
    } catch (e) {
      print('❌ Error calling semantic API: $e');
    }

    return [];
  }
}
