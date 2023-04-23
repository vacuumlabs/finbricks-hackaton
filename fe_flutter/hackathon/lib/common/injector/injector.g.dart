// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'injector.dart';

// **************************************************************************
// KiwiInjectorGenerator
// **************************************************************************

class _$Injector extends Injector {
  @override
  void _configureBloc() {
    final KiwiContainer container = KiwiContainer();
    container.registerFactory((c) => HackathonBloc(c<SomeUsecase>()));
  }

  @override
  void _configureUsecase() {
    final KiwiContainer container = KiwiContainer();
    container.registerSingleton((c) => SomeUsecase(c<HackathonRepository>()));
  }

  @override
  void _configureRepository() {}
  @override
  void _configureLocalDatasource() {}
  @override
  void _configureRemoteDatasource() {}
  @override
  void _configureDependencies() {}
}
