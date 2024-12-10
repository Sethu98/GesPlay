import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import 'api.dart';

class GamesList extends StatefulWidget {
  final Future<void> Function(String game) setSelectedGame;

  const GamesList({super.key, required this.setSelectedGame});

  @override
  State<StatefulWidget> createState() => _GamesListState();
}

class _GamesListState extends State<GamesList> {
  List<String> games = [];

  @override
  void initState() {
    super.initState();
    fetchGames();
  }

  void fetchGames() async {
    var response = await Api.getGamesList();
    if (!response['success']) {
      return;
    }

    print(response);

    setState(() {
      games = List<String>.from(response['data']);
    });

    if(games.isNotEmpty) {
      widget.setSelectedGame(games[0]);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Games",
          style: TextStyle(color: Colors.black),
        ),
        backgroundColor: theme.colorScheme.inversePrimary,
        foregroundColor: theme.colorScheme.onPrimary,
      ),
      body: Column(
        children: [
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
              ),
              child: ScrollableCardList(items: games, setSelectedGame: widget.setSelectedGame),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: ElevatedButton(
              onPressed: () => {},
              child: const Text("Add game"),
            ),
          )
        ],
      ),
    );
  }
}

class ScrollableCardList extends StatelessWidget {
  final Future<void> Function(String game) setSelectedGame;
  final List<String> items;

  const ScrollableCardList({
    super.key,
    required this.items,
    required this.setSelectedGame
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(8.0),
      itemCount: items.length,
      itemBuilder: (context, index) {
        return Card(
          margin: const EdgeInsets.symmetric(vertical: 8.0),
          child: ListTile(
            title: Text(items[index]),
            trailing: IconButton(
              icon: const Icon(
                Icons.play_arrow_rounded,
                color: Colors.green,
              ),
              onPressed: () {
                setSelectedGame(items[index]);
              },
            ),
          ),
        );
      },
    );
  }
}
