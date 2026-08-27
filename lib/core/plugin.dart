abstract interface class Plugin {
  String get id;
  String get name;
  String get version;

  Future<void> initialize();
  Future<void> dispose();
}