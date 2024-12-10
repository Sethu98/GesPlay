import 'package:flutter/material.dart';
import 'package:dropdown_search/dropdown_search.dart';

import 'constants.dart';

class GameControlsSection extends StatelessWidget {
  final String? gameName;
  final Map<String, String>? controlLayout;

  GameControlsSection(
      {super.key, required this.gameName, required this.controlLayout}) {
    // Read and store controls map
  }

  Widget keyboardKeyDisplay2(String name) {
    return ConstrainedBox(
      constraints: BoxConstraints(minWidth: 90),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.grey[200],
          borderRadius: BorderRadius.circular(8),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.shade500,
              offset: Offset(0, 2),
              blurRadius: 0,
              spreadRadius: 0,
            ),
          ],
        ),
        child: TextField(
          controller: TextEditingController(text: name),
          maxLength: 20,
          textAlign: TextAlign.center,
          decoration: InputDecoration(
            counterText: "",
            filled: true,
            fillColor: Colors.grey[200],
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: BorderSide(
                color: Colors.grey.shade400,
                width: 1,
              ),
            ),
            contentPadding: EdgeInsets.symmetric(
              vertical: 8,
              horizontal: 10,
            ),
            isDense: true,
          ),
        ),
      ),
    );
  }

  Widget keyboardKeyDisplay3(String selectedValue) {
    //, List<String> items, Function(String?) onChanged) {
    var items = ['left', 'right', 'up', 'down', '1', '2', '3', 'Unmapped'];

    return ConstrainedBox(
      constraints: BoxConstraints(minWidth: 90),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.grey[200],
          borderRadius: BorderRadius.circular(8),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.shade500,
              offset: Offset(0, 2),
              blurRadius: 0,
              spreadRadius: 0,
            ),
          ],
        ),
        child: DropdownButtonFormField<String>(
          value: selectedValue,
          items: items.map((String value) {
            return DropdownMenuItem<String>(
              value: value,
              child: Text(value),
            );
          }).toList(),
          onChanged: (value) => {},
          decoration: InputDecoration(
            filled: true,
            fillColor: Colors.grey[200],
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: BorderSide(
                color: Colors.grey.shade400,
                width: 1,
              ),
            ),
            contentPadding: EdgeInsets.symmetric(
              vertical: 8,
              horizontal: 10,
            ),
            isDense: true,
          ),
        ),
      ),
    );
  }

  Widget keyboardKeyDisplay(String selectedValue) {
    //, List<String> items, Function(String?) onChanged) {
    return ConstrainedBox(
      constraints: const BoxConstraints(minWidth: 200),
      child: Container(
        padding: const EdgeInsets.all(5),
        child: DropdownSearch<String>(
          selectedItem: selectedValue,
          items: (__, _) => Constants.KEYBOARD_KEYS,
          popupProps:
              const PopupProps.menu(showSearchBox: true, fit: FlexFit.loose),
          dropdownBuilder: (context, selectedItem) {
            return Center(
              child: Text(
                selectedItem ?? '',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontWeight: selectedItem == 'Unmapped'
                      ? FontWeight.normal
                      : FontWeight.w600,
                  color: selectedItem == 'Unmapped' ? Colors.grey: Colors.black),
              ),
            );
          },
          decoratorProps: DropDownDecoratorProps(
            decoration: InputDecoration(
              filled: true,
              fillColor: Colors.grey[200],
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: BorderSide(
                  color: Colors.grey.shade400,
                  width: 1,
                ),
              ),
              isDense: true,
            ),
          ),
          onChanged: (value) {
            // Handle selection
          },
        ),
      ),
    );
  }

  Widget controlLayoutTable(BuildContext context) {
    final theme = Theme.of(context);
    final List<String> columnNames = ['Gesture', 'Key'];

    // final List<Map<String, dynamic>> data = controlLayout!.entries
    //     .map((entry) => {
    //           'gesture': entry.key,
    //           'key': entry.value,
    //         })
    //     .toList();

    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          gameName!,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 20,
            color: theme.colorScheme.primary,
          ),
        ),
        const SizedBox(height: 15),
        DataTable(
          decoration: BoxDecoration(
            border: Border.all(color: Colors.black),
          ),
          headingRowColor: MaterialStateProperty.resolveWith(
            (states) => theme.colorScheme.inversePrimary,
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
          rows: Constants.GESTURES
              .map(
                (gesture) => DataRow(cells: [
                  DataCell(Text(gesture)),
                  DataCell(
                      keyboardKeyDisplay(controlLayout![gesture] ?? 'Unmapped'))
                ]),
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
                : controlLayoutTable(context),
      ),
    );
  }
}
