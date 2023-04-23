import 'package:feature_hackathon/navigation/interaction_navigation.dart';
import 'package:feature_hackathon/presentation/journey/hackathon/bloc/hackathon_bloc.dart';
import 'package:feature_hackathon/presentation/journey/hackathon/login_constants.dart';
import 'package:flutter/material.dart';
import 'package:generic_ui/constants/image_name_constant.dart';
import 'package:generic_ui/widget/loader/loader_progress_indicator.dart';
import 'package:generic_ui/widget/safi_scaffold.dart';
import 'package:generic_ui/widget/story_view/educational_screen.dart';
import 'package:module_common/i18n/i18n_extension.dart';
import 'package:module_common/presentation/bloc/base_bloc.dart';

class HackathonPage extends StatelessWidget {
  final HackathonBloc hackathonBloc;
  final HackathonInteractionNavigation navigation;

  HackathonPage({
    Key? key,
    required this.hackathonBloc,
    required this.navigation,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<HackathonBloc, HackathonState>(
      builder: (context, state) {
        return SafiScaffold(
          body: _buildBody(
            context,
            state,
            () {
              hackathonBloc.add(HackathonForceRefresh());
            },
            () {
              hackathonBloc.add(HackathonShuffle());
            },
          ),
        );
      },
    );
  }
}

Widget _buildBody(
  BuildContext context,
  HackathonState state,
  void Function()? onRefresh,
  void Function()? refreshAction,
) {
  if (state is HackathonReady) {
    final advice =
        state.data[state.index].lambda2Response.replaceAll('\n\n', '\n');
    final List<String> sections = advice.split('\n');
    final List<StoryItemParams> _storyItemParams = [
      StoryItemParams(
        key: const Key('storyItem1'),
        descriptionTitle: 'Spending overview'.i18n(context),
        description: sections.length > 0 ? sections[0] : '',
        imagePath: ImageNameConstant.hackathonStory1,
      ),
      StoryItemParams(
        key: const Key('storyItem2'),
        descriptionTitle: 'Your savings'.i18n(context),
        description: sections.length > 1 ? sections[1] : '',
        imagePath: ImageNameConstant.hackathonStory2,
      ),
      StoryItemParams(
        key: const Key('storyItem3'),
        descriptionTitle: 'Financial advice'.i18n(context),
        description: sections.length > 2 ? sections[2] : '',
        imagePath: ImageNameConstant.hackathonStory3,
        buttonTitle: 'Roger that!'.i18n(context),
      ),
    ];

    final EducationalScreenParams _educationalScreenParams =
        EducationalScreenParams(
      key: const Key('edu'),
      title: HackathonConstants.pageTitle.i18n(context) +
          (state.index > 0 ? ' (${state.index})' : ''),
      storyItemParams: _storyItemParams,
    );

    return EducationalScreen(
      onRefresh: onRefresh,
      educationalScreenParams: _educationalScreenParams,
      closeAction: () {
        Navigator.of(context).pop();
      },
      refreshAction: refreshAction,
    );
  } else {
    return Center(
      child: LoaderProgressIndicator(),
    );
  }
}
