import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class GamesList extends StatefulWidget {
  final Future<void> Function(String game) setSelectedGame;

  const GamesList({super.key, required this.setSelectedGame});

  @override
  State<StatefulWidget> createState() => _GamesListState();
}

class _GamesListState extends State<GamesList> {
  @override
  Widget build(BuildContext context) {
    widget.setSelectedGame("mario");

    return Scaffold(
      appBar: AppBar(
        title: Text("Games list"),
      ),
      body: Text("Much wow"),
    );
  }
}
