import 'package:flutter/material.dart';

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
  String? _selectedGame = null;

  void _setSelectedGame(String game) {
    setState(() {
      _selectedGame = game;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Row(
          children: [
            Expanded(
              child: Container(
                margin: EdgeInsets.all(10),
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.grey.shade300)),
                child: Center(
                  child: Column(
                    children: [
                      Text("Wow"),
                      FloatingActionButton(
                        onPressed: () => _setSelectedGame,
                        tooltip: 'Increment',
                        child: const Icon(Icons.add),
                      )
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(width: 3),
            Expanded(
              child: Container(
                margin: EdgeInsets.all(10),
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.grey.shade300)),
                child: Center(
                  child: GameControlsSection(gameName: "Mario"),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class GameControlsSection extends StatelessWidget {
  final String? gameName;
  late final Map<String, String> controls;

  GameControlsSection({super.key, required this.gameName}) {
    controls = {};
    // Read and store controls map
  }

  Widget keyboardKeyDisplay(String name) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.grey[200],
        borderRadius: BorderRadius.circular(6),
        border: Border.all(
          color: Colors.grey.shade400,
          width: 1,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.shade500,
            offset: Offset(0, 2),
            blurRadius: 0,
            spreadRadius: 0,
          ),
        ],
      ),
      child: Text(
        name,
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: Colors.black,
        ),
      ),
    );
  }

  Widget controlLayoutTable() {
    final List<String> columnNames = ['Key', 'Gesture'];
    final Map<String, String> mapping = {
      "Pointing_Up": "left",
      "Thumb_Up": "right",
      "Open_Palm": "up",
      "Thumb_Down": "down"
    };

    final List<Map<String, dynamic>> data = mapping.entries
        .map((entry) => {
              'key': entry.value,
              'gesture': entry.key,
            })
        .toList();

    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          gameName!,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 20,
            color: Colors.black,
          ),
        ),
        const SizedBox(height: 15),
        DataTable(
          decoration: BoxDecoration(
            border: Border.all(color: Colors.black),
          ),
          headingRowColor: MaterialStateProperty.resolveWith(
            (states) => Colors.blue[100],
          ),
          dividerThickness: 2,
          border: TableBorder.all(
            color: Colors.black,
            width: 1,
          ),
          columns: columnNames
              .map((columnName) => DataColumn(
                    label: Text(
                      columnName,
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.black,
                      ),
                    ),
                  ))
              .toList(),
          rows: data
              .map(
                (item) => DataRow(
                  cells: columnNames.map((columnName) {
                    String value = item[columnName.toLowerCase()];

                    if (columnName.toLowerCase() == 'key') {
                      return DataCell(keyboardKeyDisplay(value));
                    }

                    return DataCell(Text(value));
                  }).toList(),
                ),
              )
              .toList(),
        )
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child:
            gameName == null ? Text("No game selected") : controlLayoutTable(),
      ),
    );
  }
}
