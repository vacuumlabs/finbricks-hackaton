import 'package:data_abstraction/entity/hackathon/something_entity.dart';
import 'package:data_abstraction/repository/hackathon_repository.dart';

class SomeUsecase {
  final HackathonRepository _hackathonRepository;

  SomeUsecase(this._hackathonRepository);

  Future<bool> loadCommand() => _hackathonRepository.loadCommand();

  Future<List<SomethingEntity>> getSomething({bool forceRefresh = false}) =>
      _hackathonRepository.getSomething(forceRefresh: forceRefresh);
}
