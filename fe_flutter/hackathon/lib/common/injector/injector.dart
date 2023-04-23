import 'package:data_abstraction/repository/hackathon_repository.dart';
import 'package:feature_hackathon/domain/usecase/some_usecase.dart';
import 'package:feature_hackathon/presentation/journey/hackathon/bloc/hackathon_bloc.dart';
import 'package:kiwi/kiwi.dart';
import 'package:library_injection/annotations.dart';

part 'injector.g.dart';

abstract class Injector {
  static void init() {
    _$Injector()._configure();
  }

  static final T Function<T>([String name]) resolve = KiwiContainer().resolve;

  void _configure() {
    _configureBloc();
    _configureUsecase();
    _configureRepository();
    _configureLocalDatasource();
    _configureRemoteDatasource();
    _configureDependencies();
  }

  @Register.factory(HackathonBloc)
  void _configureBloc();

  @Register.singleton(SomeUsecase)
  void _configureUsecase();

  void _configureRepository();

  void _configureLocalDatasource();

  void _configureRemoteDatasource();

  @Dependencies.dependsOn(SomeUsecase, [HackathonRepository])
  void _configureDependencies();
}
