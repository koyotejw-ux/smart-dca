import 'package:flutter/material.dart';

class OneUIScrollView extends StatelessWidget {
  final String title;
  final List<Widget> children;
  final List<Widget>? actions;
  final Widget? floatingActionButton;
  final TextStyle? titleStyle;
  final Color? backgroundColor;

  const OneUIScrollView({
    super.key,
    required this.title,
    required this.children,
    this.actions,
    this.floatingActionButton,
    this.titleStyle,
    this.backgroundColor,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final topPadding = MediaQuery.of(context).padding.top;
    
    return Scaffold(
      backgroundColor: backgroundColor ?? theme.scaffoldBackgroundColor,
      floatingActionButton: floatingActionButton,
      body: CustomScrollView(
        physics: const BouncingScrollPhysics(),
        slivers: [
          SliverAppBar(
            expandedHeight: 200.0,
            floating: false,
            pinned: true,
            snap: false,
            stretch: true,
            backgroundColor: backgroundColor ?? theme.scaffoldBackgroundColor,
            elevation: 0,
            scrolledUnderElevation: 0,
            actions: actions,
            flexibleSpace: FlexibleSpaceBar(
              stretchModes: const [
                StretchMode.zoomBackground,
                StretchMode.fadeTitle,
              ],
              centerTitle: true,
              titlePadding: const EdgeInsets.only(bottom: 16),
              title: LayoutBuilder(
                builder: (context, constraints) {
                  final isCollapsed = constraints.maxHeight <= kToolbarHeight + topPadding + 60;
                  final baseStyle = isCollapsed 
                      ? theme.textTheme.titleLarge! 
                      : theme.textTheme.headlineLarge!;
                  
                  return AnimatedDefaultTextStyle(
                    duration: const Duration(milliseconds: 200),
                    style: (titleStyle ?? baseStyle).copyWith(
                      fontSize: isCollapsed ? 20 : 32,
                      fontWeight: FontWeight.w900,
                    ),
                    child: Text(
                      title,
                      textAlign: TextAlign.center,
                    ),
                  );
                },
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            sliver: SliverList(
              delegate: SliverChildListDelegate(children),
            ),
          ),
          // Bottom padding to ensure last item is visible above FAB or bottom bar
          const SliverToBoxAdapter(
            child: SizedBox(height: 100),
          ),
        ],
      ),
    );
  }
}
