import 'dart:convert';

import 'package:http/http.dart' as http;
import 'dart:developer';

class ApiEndpoints {
  static const BASE_URL = "http://127.0.0.1:5000/api";
  static const LAYOUT_ENDPOINT = 'layout';
  static const GAMES_LIST = 'games-list';
  static const UPDATE_CONTROLS = 'update-controls';
  static const ADD_GAME = 'add-game';
}

class Api {
  static Future<Map<String, dynamic>> get(String endpoint,
      {Map<String, String>? queryParams}) async {
    try {
      final uri = Uri.parse('${ApiEndpoints.BASE_URL}/$endpoint')
          .replace(queryParameters: queryParams);
      final response = await http.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
        },
      );

      log("Got response for $endpoint - ${response.statusCode}: "); // ${response.body}");

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load data: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  static Future<Map<String, dynamic>> post(String endpoint,
      {Map<String, dynamic>? body}) async {
    try {
      final uri = Uri.parse('${ApiEndpoints.BASE_URL}/$endpoint');
      final response = await http.post(
        uri,
        headers: {
          'Content-Type': 'application/json',
        },
        body: body != null ? json.encode(body) : null,
      );

      log("Got response $endpoint - - ${response.statusCode}"); //: ${response.body}");

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to post data: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  static Future<Map<String, dynamic>> getLayout(String game) async {
    return Api.get('${ApiEndpoints.LAYOUT_ENDPOINT}/$game');
  }

  static Future<Map<String, dynamic>> getGamesList() async {
    return Api.get(ApiEndpoints.GAMES_LIST);
  }

  static Future<Map<String, dynamic>> addGame(String gameName) async {
    return Api.post(ApiEndpoints.ADD_GAME, body: {'game': gameName});
  }

  static Future<Map<String, dynamic>> updateControls(
      String gameName, String gesture, String newKey) async {
    return Api.post(ApiEndpoints.UPDATE_CONTROLS,
        body: {'game': gameName, 'gesture': gesture, 'new_key': newKey});
  }
}
