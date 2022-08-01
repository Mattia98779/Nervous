// Copyright 2018 The Flutter team. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter/material.dart';
import 'package:flutter_bootstrap_widgets/bootstrap_widgets.dart';
import 'dart:html' as html;

dynamic value1 = "blues";
dynamic value2 = "childrens";

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Welcome to Flutter',
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Interface v1.0'),
        ),
        body: tuttoWidget()
        
      ),
    );
  }
}

Future pars() async{
  String path = ''+value1+'_'+value2;
  print(path);
  final String jsonData = await rootBundle.loadString(path);

  return jsonData;
}

class tuttoWidget extends StatefulWidget {
  const tuttoWidget({Key? key}) : super(key: key);

  @override
  State<tuttoWidget> createState() => _tuttoWidgetState();
}

class _tuttoWidgetState extends State<tuttoWidget> {
  @override
  Widget build(BuildContext context) {
    return Column(
          children: [
          SizedBox(height: 10),
          Container(child: Wrap(spacing:100,
          children:[MyStatefulWidget1(),MyStatefulWidget2(), ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: Stack(
              children: <Widget>[
                Positioned.fill(
                  child: Container(
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: <Color>[
                          Color(0xFF0D47A1),
                          Color(0xFF1976D2),
                          Color(0xFF42A5F5),
                        ],
                      ),
                    ),
                  ),
                ),
                TextButton(
                  style: TextButton.styleFrom(
                    padding: const EdgeInsets.all(16.0),
                    primary: Colors.white,
                    textStyle: const TextStyle(fontSize: 20),
                  ),
                  onPressed: () {setState(() {
                    
                  });},
                  child: const Text('Combina'),
                ),
              ],
            ),
          ),])),
          Divider(color: Colors.blue,),
          Row(children: [Wrap(children: const [
            SizedBox(
                  width: 55.0,
                  height: 42.0,
                  child: Text(
                    "#", style: const TextStyle(fontWeight: FontWeight.bold), textAlign: TextAlign.center,
                    ),
                ),

                SizedBox(
                  width: 400.0,
                  height: 42.0,
                  child: Text(
                    "Title", style: const TextStyle(fontWeight: FontWeight.bold)
                    ),
                ),
                SizedBox(
                  width: 400.0,
                  height: 42.0,
                  child: Text(
                    "Performer", style: const TextStyle(fontWeight: FontWeight.bold)
                    ),
                ),
                SizedBox(
                  width: 800.0,
                  height: 42.0,
                  child: Text(
                    "Spiegazione", style: const TextStyle(fontWeight: FontWeight.bold)
                    ),
                ),
                SizedBox(
                  width: 400.0,
                  height: 42.0,
                  child: Text(
                    "Ascolta su youtube", style: const TextStyle(fontWeight: FontWeight.bold)
                    ),
                )],)] ),
        Container(child: projectWidget(),), ]);
  
  }
}
Widget projectWidget() {
  return FutureBuilder(
    builder: (context, projectSnap) {
      if (!projectSnap.hasData) {
        //print('project snapshot data is: ${projectSnap.data}');
        return Container();
      }

      dynamic s =jsonDecode(projectSnap.data.toString());
      return ListView.builder(
          padding: const EdgeInsets.all(20.0),
          scrollDirection: Axis.vertical,
          shrinkWrap: true,
          itemCount: 10,
          itemBuilder: (BuildContext context, int index) {
            return Column(children: [
              Divider(color: Colors.blue,),
              Row( children: [Wrap(
              children: [
                SizedBox(
                  width: 40.0,
                  height: 42.0,
                  child: Text(
                    (index+1).toString(), style: const TextStyle(fontWeight: FontWeight.bold)
                    ),
                ),
                SizedBox(
                  width: 400.0,
                  height: 42.0,
                  child: Text(
                    s["classifica"][index]["title"]
                    ),
                ),
                SizedBox(
                  width: 400.0,
                  height: 42.0,
                  child: Text(
                    s["classifica"][index]["performer"]
                    ),
                ),
                SizedBox(
                  width: 800.0,
                  height: 42.0,
                  child: Text(
                    s["classifica"][index]["spiegazione"].toString()
                    ),
                ),
                IconButton(onPressed:(){
                  html.window.open('https://www.youtube.com/results?search_query='+s["classifica"][index]["title"]+ " "+ s["classifica"][index]["performer"],"_blank");
                }, icon: const Icon(Icons.volume_up))
                ])],
            ),
            
            ],
            ) ;
          });
    },
    future: pars(),
  );
}


class MyStatefulWidget1 extends StatefulWidget {
  const MyStatefulWidget1({Key? key}) : super(key: key);

  @override
  State<MyStatefulWidget1> createState() => _MyStatefulWidgetState1();
}

class _MyStatefulWidgetState1 extends State<MyStatefulWidget1> {
  String dropdownValue = 'blues';

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      value: dropdownValue,
      icon: const Icon(Icons.arrow_downward),
      elevation: 16,
      style: const TextStyle(color: Colors.blue),
      underline: Container(
        height: 2,
        color: Colors.blueAccent,
      ),
      onChanged: (String? newValue) {
        value1 = newValue;
        setState(() {
          dropdownValue = newValue!;
        });
      },
      items: <String>['blues','childrens','classical','comedy-spoken',
      'country','easy-listening','electronic','folk','international','jazz','latin','new-age',
      'pop-rock','r-b','rap','reggae','stage-screen','vocal','avant-garde']
          .map<DropdownMenuItem<String>>((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value),
        );
      }).toList(),
    );
  }
}

class MyStatefulWidget2 extends StatefulWidget {
  const MyStatefulWidget2({Key? key}) : super(key: key);

  @override
  State<MyStatefulWidget2> createState() => _MyStatefulWidgetState2();
}

class _MyStatefulWidgetState2 extends State<MyStatefulWidget2> {
  String dropdownValue = 'childrens';

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      value: dropdownValue,
      icon: const Icon(Icons.arrow_downward),
      elevation: 16,
      style: const TextStyle(color: Colors.blue),
      underline: Container(
        height: 2,
        color: Colors.blueAccent,
      ),
      onChanged: (String? newValue) {
        value2 = newValue;
        setState(() {
          dropdownValue = newValue!;
        });
      },
      items: <String>['blues','childrens','classical','comedy-spoken',
      'country','easy-listening','electronic','folk','international','jazz','latin','new-age',
      'pop-rock','r-b','rap','reggae','stage-screen','vocal','avant-garde']
          .map<DropdownMenuItem<String>>((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value),
        );
      }).toList(),
    );
  }
}

void apriLink(){


}
