part of 'hackathon_bloc.dart';

abstract class HackathonEvent extends Equatable {
  @override
  List<Object?> get props => [];
}

class HackathonSetup extends HackathonEvent {}

class HackathonShuffle extends HackathonEvent {}

class HackathonForceRefresh extends HackathonEvent {}
