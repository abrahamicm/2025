# 1.10. Widgets de entrada de usuario: Button, TextField (1.10)

## Introducción

Como desarrollador web, estás familiarizado con elementos como `<button>` y `<input type="text">`. En Flutter, controlamos la interacción del usuario a través de widgets. Esta lección te presentará los widgets equivalentes en Flutter: `ElevatedButton`, `TextButton`, `OutlinedButton` (como botones) y `TextField` (para la entrada de texto). Comprender cómo funcionan estos widgets es fundamental para crear interfaces de usuario interactivas en Flutter.  La clave es que la forma en que administras el estado y respondes a los eventos es diferente en Flutter, pero la *idea* es la misma.

## Explicación

En Flutter, los widgets son los bloques de construcción fundamentales de la interfaz de usuario.  Piensa en ellos como los elementos HTML de tu aplicación. Para los botones, Flutter ofrece varias opciones, cada una con un estilo visual diferente.

`ElevatedButton` es similar a un botón con una sombra elevada, lo que le da una apariencia más prominente. Puedes personalizar su apariencia, incluyendo el color, la forma y el texto.

`TextButton` es un botón más simple, sin la sombra elevada. A menudo se usa para acciones menos destacadas o para botones dentro de un diálogo.

`OutlinedButton` es un botón con un borde alrededor del texto. Similar al `TextButton` es menos prominente que el `ElevatedButton`.

Para la entrada de texto, usaremos el widget `TextField`.  Este widget permite a los usuarios ingresar texto, al igual que un `<input type="text">` en HTML. El `TextField` ofrece muchas opciones de personalización, como la validación de entrada, la configuración del teclado que se muestra al usuario y el control del texto ingresado.

Una diferencia crucial con respecto a HTML/JavaScript es que en Flutter, los widgets son inmutables.  Esto significa que no puedes modificarlos directamente después de su creación. En cambio, actualizas el estado de la aplicación, lo que desencadena una reconstrucción del árbol de widgets.  Esta reconstrucción eficiente es lo que hace que las interfaces de Flutter sean rápidas y fluidas.

Para manejar eventos, como cuando un usuario presiona un botón o escribe en un `TextField`, usaremos funciones de callback.  Por ejemplo, el `ElevatedButton` tiene una propiedad `onPressed` que recibe una función a ejecutar cuando se presiona el botón.  Esto es similar al `addEventListener` en JavaScript, pero con una sintaxis más declarativa.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos.

Aquí tienes algunos conceptos clave relacionados con este tema de Flutter:

*   **`ElevatedButton`**: Un botón con elevación.
*   **`TextButton`**: Un botón de texto plano.
*   **`OutlinedButton`**: Un botón con un borde.
*   **`TextField`**: Para la entrada de texto.
*   **`onPressed`**:  Callback que se ejecuta cuando se presiona un botón.
*   **`onChanged`**: Callback que se ejecuta cuando el texto en un `TextField` cambia.
*   **`TextEditingController`**: Controla el texto dentro de un `TextField`. Similar a acceder el valor de un input HTML con `element.value`.

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Ejemplos de Widgets')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              ElevatedButton(
                onPressed: () {
                  print('Botón presionado!');
                },
                child: const Text('Presióname'),
              ),
              const SizedBox(height: 20), // Espacio entre widgets
              TextButton(
                onPressed: () {
                  print('TextButton presionado!');
                },
                child: const Text('Botón de texto'),
              ),
              const SizedBox(height: 20), // Espacio entre widgets
              OutlinedButton(
                onPressed: () {
                  print('OutlinedButton presionado!');
                },
                child: const Text('Botón con borde'),
              ),
              const SizedBox(height: 20),
              // TextField para entrada de texto
              const MyTextField(),
            ],
          ),
        ),
      ),
    ),
  );
}

class MyTextField extends StatefulWidget {
  const MyTextField({super.key});

  @override
  State<MyTextField> createState() => _MyTextFieldState();
}

class _MyTextFieldState extends State<MyTextField> {
  final TextEditingController _controller = TextEditingController(); // Controlador para el TextField

  @override
  void dispose() {
    _controller.dispose(); // Libera recursos cuando el widget se elimina
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: TextField(
        controller: _controller, // Asigna el controlador al TextField
        decoration: const InputDecoration(
          border: OutlineInputBorder(),
          labelText: 'Escribe algo',
        ),
        onChanged: (text) {
          print('Texto ingresado: $text'); // Imprime el texto ingresado
        },
      ),
    );
  }
}
```

En este ejemplo, `ElevatedButton`, `TextButton`, y `OutlinedButton` tienen la propiedad `onPressed` que es una función anónima que imprime un mensaje en la consola.  El `TextField` utiliza un `TextEditingController` para controlar el texto ingresado. La función `onChanged` se llama cada vez que el texto cambia y el texto ingresado se imprime en la consola. Nota que en Flutter necesitaremos hacer uso de un `StatefulWidget` para mantener el valor dentro del `TextField` mientras que, en HTML/JavaScript, el elemento `<input>` mantiene su valor automáticamente.

## Práctica: Preguntas y Respuestas

**Pregunta:** ¿Cuál es la propiedad que se utiliza en un `ElevatedButton` para definir qué sucede cuando se presiona?
**5... 4... 3... 2... 1...**
**Respuesta:** La propiedad `onPressed`.

**Pregunta:** ¿Qué widget utilizas en Flutter para permitir la entrada de texto por parte del usuario?
**5... 4... 3... 2... 1...**
**Respuesta:** El widget `TextField`.

**Pregunta:** ¿Cómo accedes y controlas el texto dentro de un `TextField` en Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** Utilizando un `TextEditingController`.

**Pregunta:** ¿Cuál es la diferencia visual principal entre `ElevatedButton` y `TextButton`?
**5... 4... 3... 2... 1...**
**Respuesta:** `ElevatedButton` tiene una sombra elevada, mientras que `TextButton` es plano.

**Pregunta:** ¿Qué callback usarías si quisieras hacer algo cada vez que el texto en un `TextField` cambia?
**5... 4... 3... 2... 1...**
**Respuesta:** Usarías el callback `onChanged`.
