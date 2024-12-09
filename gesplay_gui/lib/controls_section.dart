import 'package:flutter/material.dart';
import 'package:gesplay_gui/api.dart';

class GameControlsSection extends StatelessWidget {
  final String? gameName;
  final Map<String, String>? controlLayout;

  GameControlsSection({super.key, required this.gameName, required this.controlLayout}) {
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

    final List<Map<String, dynamic>> data = controlLayout!.entries
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
          style: const TextStyle(
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
        child: gameName == null
            ? const Text("No game selected")
            : controlLayout == null
                ? const Text(
                    "Layout not found",
                  )
                : controlLayoutTable(),
      ),
    );
  }
}
