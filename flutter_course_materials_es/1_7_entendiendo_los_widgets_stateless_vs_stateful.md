# 1.7. Entendiendo los Widgets: Stateless vs Stateful (1.7)

Para desarrolladores web que se están adentrando en el mundo de Flutter, comprender la diferencia entre widgets `Stateless` y `Stateful` es crucial, ya que son la base de la construcción de interfaces de usuario dinámicas. Esto es similar a entender cómo el DOM interactúa con JavaScript para actualizar elementos en una página web, pero en Flutter, todo se construye con widgets, que pueden ser estáticos o dinámicos.

## Explicación

En Flutter, un widget es la unidad básica de construcción de la interfaz de usuario. Piensa en ellos como los elementos HTML que conoces, como `<div>`, `<p>`, `<img>`, etc.  Sin embargo, a diferencia de HTML donde los elementos son principalmente declarativos y estáticos hasta que JavaScript los manipula, los widgets en Flutter tienen la capacidad de ser reactivos desde el principio.

Existen dos tipos principales de widgets: `StatelessWidget` y `StatefulWidget`.

*   **StatelessWidget:** Un `StatelessWidget` es un widget que no tiene estado mutable.  Esto significa que sus propiedades (data) no cambian durante la vida útil del widget.  Piensa en ellos como elementos HTML estáticos, como una etiqueta de texto o una imagen que no se modifican. Son inmutables y dependen únicamente de la información que se les proporciona al crearse. La interfaz gráfica no se reconstruirá si algo cambia en la aplicación. Son ideales para mostrar información estática. En el contexto web, podrías pensarlo como un elemento HTML renderizado una sola vez y que no se actualiza a menos que se vuelva a cargar toda la página.

*   **StatefulWidget:** Un `StatefulWidget`, por otro lado, mantiene un estado que puede cambiar durante la vida útil del widget.  Estos widgets son dinámicos y pueden redibujarse automáticamente cuando su estado cambia. Esto es fundamental para la creación de interfaces de usuario interactivas.  Piensa en un botón que cambia de color al ser presionado, o un formulario que muestra mensajes de validación en tiempo real.  El estado de un `StatefulWidget` se almacena en un objeto `State` separado, lo que permite una gestión más organizada de la información. En el mundo web, esto sería análogo a tener JavaScript interactuando con elementos del DOM para actualizar su contenido, estilos o atributos en respuesta a eventos del usuario o cambios en los datos.

La principal diferencia radica en si el widget necesita recordar información entre las reconstrucciones. Si no, entonces un `StatelessWidget` es suficiente. Si el widget necesita cambiar su apariencia en respuesta a la interacción del usuario o a cambios en los datos, entonces se requiere un `StatefulWidget`.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos para comprender mejor estos conceptos.

Aquí tienes algunos conceptos clave que usaremos:

*   `StatelessWidget`: Widget sin estado mutable.
*   `StatefulWidget`: Widget con estado mutable.
*   `State`: El estado asociado a un `StatefulWidget`.
*   `setState()`: Método para notificar a Flutter que el estado ha cambiado, provocando una reconstrucción de la interfaz de usuario.
*   `build()`: Método que describe la interfaz de usuario del widget.

```dart
// Ejemplo de StatelessWidget:  Un widget de texto estático
import 'package:flutter/material.dart';

class MiTextoEstatico extends StatelessWidget {
  final String texto;

  MiTextoEstatico({Key? key, required this.texto}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Text(texto);
  }
}
```

```dart
// Ejemplo de StatefulWidget: Un contador que se incrementa al presionar un botón.
import 'package:flutter/material.dart';

class MiContador extends StatefulWidget {
  const MiContador({Key? key}) : super(key: key);

  @override
  _MiContadorState createState() => _MiContadorState();
}

class _MiContadorState extends State<MiContador> {
  int _contador = 0;

  void _incrementarContador() {
    // LLamamos a setState para reconstruir el widget con el nuevo valor del contador.
    setState(() {
      _contador++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Text('Contador: $_contador'), // Muestra el valor del contador.
        ElevatedButton(
          onPressed: _incrementarContador, // Llama a la función para incrementar.
          child: const Text('Incrementar'),
        ),
      ],
    );
  }
}
```

En el ejemplo del `StatefulWidget`, el método `setState()` es crucial.  Es la forma en que notificamos a Flutter que el estado del widget ha cambiado y que necesita redibujarse.  Sin `setState()`, el valor de `_contador` se incrementaría, pero la interfaz de usuario no se actualizaría, lo que es análogo a modificar una variable en JavaScript sin actualizar el DOM.

```dart
// Otro ejemplo, un widget que muestra una imagen desde una URL.
import 'package:flutter/material.dart';

class ImagenDesdeInternet extends StatelessWidget {
  final String urlImagen;

  ImagenDesdeInternet({Key? key, required this.urlImagen}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Image.network(urlImagen);
  }
}
```

Este ejemplo de `ImagenDesdeInternet` también es un `StatelessWidget` porque la URL de la imagen no cambia una vez que el widget es creado.

## Práctica: Preguntas y Respuestas

Aquí hay algunas preguntas para practicar lo que hemos aprendido.

**Pregunta:** ¿Cuál es la principal diferencia entre un `StatelessWidget` y un `StatefulWidget`?
**5... 4... 3... 2... 1...**
**Respuesta:** Un `StatelessWidget` no tiene estado mutable, mientras que un `StatefulWidget` sí.

**Pregunta:** ¿Qué método se utiliza para notificar a Flutter que el estado de un `StatefulWidget` ha cambiado?
**5... 4... 3... 2... 1...**
**Respuesta:** El método `setState()`.

**Pregunta:** Da un ejemplo de un widget que sería mejor implementar como un `StatelessWidget`.
**5... 4... 3... 2... 1...**
**Respuesta:** Un widget que muestra un texto estático o una imagen que no cambia.

**Pregunta:** ¿Dónde se almacena el estado de un `StatefulWidget`?
**5... 4... 3... 2... 1...**
**Respuesta:** En un objeto `State` separado, asociado al `StatefulWidget`.