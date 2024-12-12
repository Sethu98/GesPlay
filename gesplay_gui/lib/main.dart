import 'package:flutter/material.dart';
import 'package:gesplay_gui/api.dart';
import 'package:gesplay_gui/games_list.dart';

import 'controls_section.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gesplay',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Gesplay'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String? _selectedGame;
  Map<String, String>? _currentGameLayout;

  Future<void> _setSelectedGame(String game) async {
    print(game);
    if (game == _selectedGame) {
      return;
    }

    Api.setCurrentGame(game);

    Map<String, dynamic> response = await Api.getLayout(game);
    Map<String, String>? layout;
    if (response['success']) {
      layout = Map<String, String>.from(response['data']);
    }

    setState(() {
      _selectedGame = game;
      _currentGameLayout = layout;
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        backgroundColor: theme.colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Row(
          children: [
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(10),
                margin: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.grey.shade300)),
                child: Center(
                  child: GamesList(setSelectedGame: _setSelectedGame),
                ),
              ),
            ),
            const SizedBox(width: 3),
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(10),
                margin: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.grey.shade300)),
                child: Center(
                  child: GameControlsSection(
                      gameName: _selectedGame,
                      controlLayout: _currentGameLayout),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
