part of 'hackathon_bloc.dart';

class HackathonState extends Equatable {
  final String? something;

  HackathonState({
    this.something,
  });

  HackathonState.copy({
    required HackathonState srcState,
    int? attemptsLeft,
  }) : this(
          something: srcState.something,
        );

  @override
  List<Object?> get props => [
        runtimeType,
        something,
      ];
}

class HackathonReady extends HackathonState {
  final List<SomethingEntity> data;
  final int index;

  HackathonReady({
    required this.data,
    required this.index,
  });

  HackathonReady next() => HackathonReady(
        data: data,
        index: (index + 1) % data.length,
      );

  @override
  List<Object?> get props => [
    ...super.props,
    data,
    index,
  ];
}

class HackathonLoading extends HackathonState {}
