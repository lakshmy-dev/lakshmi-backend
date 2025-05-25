import 'package:supabase_flutter/supabase_flutter.dart';

class SupabaseService {
  // 🟢 Replace with your actual values
  static const String supabaseUrl = 'https://mrtsqsebaxylsdrgyxmi.supabase.co';
  static const String supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ydHNxc2ViYXh5bHNkcmd5eG1pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4ODQzNjksImV4cCI6MjA2MzQ2MDM2OX0.Wz9MRQipN-CtiRQh_qdLGLiYIdg7OIszQmu8lnFbB2c';

  static SupabaseClient get client => Supabase.instance.client;

  /// Sign up with email + password
  static Future<AuthResponse> signUp(String email, String password) async {
    try {
      final response = await client.auth.signUp(
        email: email,
        password: password,
        emailRedirectTo: 'https://lakshmy.ai/signedup.html', // ✅ updated here
      );

      print('✅ Signup Success');
      print('User ID: ${response.user?.id}');
      print('Session: ${response.session}');
      return response;
    } catch (e) {
      print('❌ Signup Error: $e');
      rethrow;
    }
  }

  /// Sign in with email + password
  static Future<AuthResponse> signIn(String email, String password) async {
    return await client.auth.signInWithPassword(email: email, password: password);
  }

  /// Sign in using Google (OAuth)
  static Future<void> signInWithGoogle() async {
    try {
      final res = await client.auth.signInWithOAuth(
        Provider.google,
        redirectTo: 'https://lakshmy.ai/signedup.html',
      );
      print("✅ Google OAuth launched");
    } catch (e) {
      print("❌ Google OAuth Error: $e");
      rethrow;
    }
  }

  /// Guest session — optional tracking
  static Future<void> startGuestSession() async {
    // Optional: store a UUID locally and use it to tag guest users
  }

  /// Sign out
  static Future<void> signOut() async {
    await client.auth.signOut();
  }

  /// Get current user (or null if not signed in)
  static User? get currentUser => client.auth.currentUser;

  /// Returns true if no user is signed in (guest mode)
  static bool get isGuest => currentUser == null;
}