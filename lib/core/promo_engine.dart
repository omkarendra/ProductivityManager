import 'plugin.dart';
import 'plugin_manager.dart';

class PromoEngine {
  PromoEngine({
    required List<Plugin> plugins,
  }) : _plugins = plugins;

  final List<Plugin> _plugins;
  late final PluginManager _pluginManager;

  bool _started = false;

  bool get isStarted => _started;

List<Plugin> get plugins {
  if (!_started) {
    throw StateError('PromoEngine has not been started');
  }

  return _pluginManager.plugins;
}
  Future<void> start() async {
    if (_started) {
      throw StateError('PromoEngine is already started');
    }

    _pluginManager = PluginManager();

    for (final plugin in _plugins) {
      await _pluginManager.register(plugin);
    }

    _started = true;
  }

  Future<void> stop() async {
    if (!_started) {
      return;
    }

    await _pluginManager.dispose();
    _started = false;
  }

}