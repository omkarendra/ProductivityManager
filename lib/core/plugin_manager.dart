import 'plugin.dart';

class PluginManager {
  final List<Plugin> _plugins = [];

  List<Plugin> get plugins => List.unmodifiable(_plugins);

  Future<void> register(Plugin plugin) async {
    if (_plugins.any((p) => p.id == plugin.id)) {
      throw StateError('Plugin already registered: ${plugin.id}');
    }

    await plugin.initialize();
    _plugins.add(plugin);
  }

  Future<void> unregister(String pluginId) async {
    final index = _plugins.indexWhere((p) => p.id == pluginId);

    if (index == -1) {
      return;
    }

    final plugin = _plugins[index];
    await plugin.dispose();
    _plugins.removeAt(index);
  }
  Future<void> dispose() async {
    for (final plugin in _plugins.reversed) {
      await plugin.dispose();
    }

    _plugins.clear();
  }
}