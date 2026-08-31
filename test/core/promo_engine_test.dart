import 'package:flutter_test/flutter_test.dart';
import 'package:promo_engine/core/plugin.dart';
import 'package:promo_engine/core/promo_engine.dart';

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
  group('PromoEngine', () {
    test('starts and initializes all plugins', () async {
      final plugin1 = TestPlugin('plugin1');
      final plugin2 = TestPlugin('plugin2');

      final engine = PromoEngine(
        plugins: [plugin1, plugin2],
      );

      await engine.start();

      expect(engine.isStarted, isTrue);
      expect(plugin1.initialized, isTrue);
      expect(plugin2.initialized, isTrue);
      expect(engine.plugins, hasLength(2));
    });

    test('cannot access plugins before engine starts', () {
      final engine = PromoEngine(
        plugins: [TestPlugin('plugin1')],
      );

      expect(
        () => engine.plugins,
        throwsA(isA<StateError>()),
      );
    });

    test('stops and disposes all plugins', () async {
      final plugin1 = TestPlugin('plugin1');
      final plugin2 = TestPlugin('plugin2');

      final engine = PromoEngine(
        plugins: [plugin1, plugin2],
      );

      await engine.start();
      await engine.stop();

      expect(engine.isStarted, isFalse);
      expect(plugin1.disposed, isTrue);
      expect(plugin2.disposed, isTrue);
    });

    test('stopping an already stopped engine does nothing', () async {
      final engine = PromoEngine(plugins: []);

      await engine.stop();

      expect(engine.isStarted, isFalse);
    });

    test('cannot start an already started engine', () async {
      final engine = PromoEngine(plugins: []);

      await engine.start();

      expect(
        () => engine.start(),
        throwsA(isA<StateError>()),
      );
    });
  });
}