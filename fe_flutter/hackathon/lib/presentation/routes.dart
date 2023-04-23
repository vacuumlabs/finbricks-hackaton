import 'package:feature_hackathon/common/injector/injector.dart';
import 'package:feature_hackathon/navigation/interaction_navigation.dart';
import 'package:feature_hackathon/presentation/journey/hackathon/bloc/hackathon_bloc.dart';
import 'package:feature_hackathon/presentation/journey/hackathon/hackathon_page.dart';
import 'package:flutter/material.dart';
import 'package:generic_ui/theme/theme_data.dart';
import 'package:module_common/presentation/bloc/base_bloc.dart';

abstract class Routes {
  static String hackathonPage = 'hackathonPage';

  static Map<String, WidgetBuilder> get all {
    return {
      hackathonPage: (ctx) {
        final hackathonBloc = Injector.resolve<HackathonBloc>();
        final navigation = Injector.resolve<HackathonInteractionNavigation>();
        return BlocProvider(
          create: (ctx) => hackathonBloc..add(HackathonSetup()),
          child: HackathonPage(
            navigation: navigation,
            hackathonBloc: hackathonBloc,
          ),
        ).wrapWithSafiTheme;
      },
    };
  }
}
