import 'dart:async';

import 'package:data_abstraction/entity/hackathon/something_entity.dart';
import 'package:feature_hackathon/domain/usecase/some_usecase.dart';
import 'package:generic_ui/widget/loader/local_loader.dart';
import 'package:module_common/presentation/bloc/base_bloc.dart';

part 'hackathon_event.dart';

part 'hackathon_state.dart';

class HackathonBloc extends Bloc<HackathonEvent, HackathonState>
    with LocalLoadingMixin {
  final SomeUsecase _someUsecase;

  HackathonBloc(
    this._someUsecase,
  ) : super(HackathonState()) {
    on<HackathonSetup>(_onSetup);
    on<HackathonShuffle>(_onShuffle);
    on<HackathonForceRefresh>(_onForceRefresh);
  }

  Future<void> _onSetup(
    HackathonSetup event,
    Emitter<HackathonState> emit,
  ) async {
    final response = await _someUsecase.getSomething();

    emit(HackathonReady(data: response, index: 0));
  }

  Future<void> _onShuffle(
      HackathonShuffle event,
      Emitter<HackathonState> emit,
      ) async {
    final _state = state;
    if (_state is HackathonReady) {
      emit(_state.next());
    }
  }

  Future<void> _onForceRefresh(
      HackathonForceRefresh event,
      Emitter<HackathonState> emit,
      ) async {
    emit(HackathonLoading());
    final response = await _someUsecase.getSomething(forceRefresh: true);
    emit(HackathonReady(data: response, index: 0));
  }
}
