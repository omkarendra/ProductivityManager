import 'package:flutter_test/flutter_test.dart';
import 'package:promo_engine/core/plugin.dart';
import 'package:promo_engine/core/plugin_manager.dart';

class TestPlugin implements Plugin {
  TestPlugin(this._id);

  final String _id;

  bool initialized = false;
  bool disposed = false;

  @override
  String get id => _id;

  @override
  String get name => 'Test Plugin';

  @override
  String get version => '1.0.0';

  @override
  Future<void> initialize() async {
    initialized = true;
  }

  @override
  Future<void> dispose() async {
    disposed = true;
  }
}

void main() {
  group('PluginManager', () {
    test('registers and initializes a plugin', () async {
      final manager = PluginManager();
      final plugin = TestPlugin('test');

      await manager.register(plugin);

      expect(plugin.initialized, isTrue);
      expect(manager.plugins, contains(plugin));
    });

    test('rejects duplicate plugin IDs', () async {
      final manager = PluginManager();

      await manager.register(TestPlugin('test'));

      expect(
        () => manager.register(TestPlugin('test')),
        throwsA(isA<StateError>()),
      );
    });

    test('unregisters and disposes a plugin', () async {
      final manager = PluginManager();
      final plugin = TestPlugin('test');

      await manager.register(plugin);
      await manager.unregister('test');

      expect(plugin.disposed, isTrue);
      expect(manager.plugins, isEmpty);
    });

    test('rejects unregistering an unknown plugin', () async {
      final manager = PluginManager();

      expect(
        () => manager.unregister('unknown'),
        throwsA(isA<StateError>()),
      );
    });

    test('disposes all plugins', () async {
      final manager = PluginManager();

      final first = TestPlugin('first');
      final second = TestPlugin('second');

      await manager.register(first);
      await manager.register(second);

      await manager.dispose();

      expect(first.disposed, isTrue);
      expect(second.disposed, isTrue);
      expect(manager.plugins, isEmpty);
    });
  });
}