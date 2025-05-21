# 2.3. Conceptos de manejo de estado en Flutter (2.3)

## Introducción

El manejo de estado es fundamental en Flutter, tal como lo es en el desarrollo web. Para un desarrollador web con experiencia en HTML, CSS y JavaScript, entender el manejo de estado en Flutter es clave para construir aplicaciones dinámicas e interactivas. En el desarrollo web, manipulamos el DOM con JavaScript para reflejar los cambios en los datos. En Flutter, utilizamos widgets que se reconstruyen cuando los datos subyacentes cambian.  Piensa en los widgets de Flutter como componentes React, y el manejo de estado como una versión más sofisticada de usar `setState` en React.  Sin un manejo de estado adecuado, tu aplicación Flutter sería tan estática como una página HTML sin JavaScript.

## Explicación

En Flutter, el manejo de estado se refiere a cómo administras y propagas los datos dentro de tu aplicación.  Imagina que tienes un contador que muestra un número.  Ese número es el *estado* de tu contador.  Cuando el usuario pulsa un botón, el estado (el número) cambia y la interfaz de usuario debe actualizarse para reflejar ese cambio.

Flutter es un framework declarativo.  Esto significa que describes la apariencia de tu interfaz de usuario en función del estado actual.  Cuando el estado cambia, Flutter automáticamente reconstruye la parte de la interfaz de usuario que depende de ese estado.  Es diferente al manejo directo del DOM en JavaScript, donde tú controlas *cómo* cambiar la interfaz de usuario.  En Flutter, simplemente declaras *qué* quieres que se muestre, y Flutter se encarga del resto.

Hay muchas maneras de manejar el estado en Flutter, desde soluciones simples como `setState` dentro de un `StatefulWidget`, hasta soluciones más complejas como Provider, BLoC/Cubit, Riverpod, o GetX.  La elección de la solución depende de la complejidad de tu aplicación y de tus preferencias personales.

El `StatefulWidget` es un widget cuyo estado puede cambiar a lo largo del tiempo.  Es análogo al uso de variables en JavaScript que actualizan el contenido de la página. Cuando el estado de un `StatefulWidget` cambia, el widget se reconstruye, lo que actualiza la interfaz de usuario.

Es importante entender la diferencia entre widgets *Stateless* y *Stateful*. Un `StatelessWidget` no tiene estado mutable; su apariencia y comportamiento están determinados por sus propiedades (los parámetros que se le pasan). Un `StatefulWidget` tiene estado mutable y puede cambiar su apariencia y comportamiento en respuesta a la interacción del usuario o a otros eventos. Piensa en un `StatelessWidget` como un elemento HTML estático, mientras que un `StatefulWidget` es como un elemento HTML que se actualiza dinámicamente mediante JavaScript.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos.  Aquí tienes algunos fragmentos de código para ilustrar los conceptos que hemos discutido.

```dart
import 'package:flutter/material.dart';

class EjemploBasicoStatefulWidget extends StatefulWidget {
  const EjemploBasicoStatefulWidget({super.key});

  @override
  State<EjemploBasicoStatefulWidget> createState() => _EjemploBasicoStatefulWidgetState();
}

class _EjemploBasicoStatefulWidgetState extends State<EjemploBasicoStatefulWidget> {
  int _conteo = 0; // Estado interno

  void _incrementarConteo() {
    setState(() { // Notifica a Flutter que el estado ha cambiado
      _conteo++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Ejemplo Stateful Widget')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('Has pulsado el botón este número de veces:'),
            Text(
              '$_conteo',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementarConteo,
        tooltip: 'Incrementar',
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

En este ejemplo, `_conteo` es el estado, y `setState` es la función que le dice a Flutter que el estado ha cambiado, lo que provoca una reconstrucción del widget.  Observa cómo `setState` es similar a usar `this.setState` en componentes React basados en clases.

Aquí tienes otro ejemplo que muestra un `StatelessWidget`:

```dart
import 'package:flutter/material.dart';

class MyStatelessWidget extends StatelessWidget {
  const MyStatelessWidget({super.key, required this.texto});

  final String texto;

  @override
  Widget build(BuildContext context) {
    return Text(texto);
  }
}
```

En este caso, el texto del widget `MyStatelessWidget` se establece a través del constructor y no cambia durante la vida útil del widget. Es un widget puramente basado en propiedades.

Un ejemplo más, mostrando cómo pasar estado entre widgets:

```dart
import 'package:flutter/material.dart';

class WidgetPadre extends StatefulWidget {
  const WidgetPadre({super.key});

  @override
  State<WidgetPadre> createState() => _WidgetPadreState();
}

class _WidgetPadreState extends State<WidgetPadre> {
  String mensaje = "Hola desde el padre";

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(mensaje),
        WidgetHijo(mensajePadre: mensaje), // Pasando el estado al hijo
      ],
    );
  }
}

class WidgetHijo extends StatelessWidget {
  const WidgetHijo({super.key, required this.mensajePadre});

  final String mensajePadre;

  @override
  Widget build(BuildContext context) {
    return Text("El mensaje del padre es: $mensajePadre");
  }
}
```

En este ejemplo, el `WidgetPadre` mantiene el estado (el mensaje) y lo pasa al `WidgetHijo` como una propiedad. El `WidgetHijo` es un `StatelessWidget` que simplemente muestra el mensaje que recibe. Esta es una forma básica de compartir estado, pero para aplicaciones más complejas, necesitarás soluciones de manejo de estado más robustas.

## Práctica: Preguntas y Respuestas

**Pregunta:** ¿Cuál es la principal diferencia entre un `StatelessWidget` y un `StatefulWidget`?
**5... 4... 3... 2... 1...**
**Respuesta:** Un `StatelessWidget` no tiene estado mutable, mientras que un `StatefulWidget` sí.

**Pregunta:** ¿Qué función se utiliza para notificar a Flutter que el estado de un `StatefulWidget` ha cambiado?
**5... 4... 3... 2... 1...**
**Respuesta:** `setState()`

**Pregunta:** ¿En Flutter, describe la interfaz de usuario en función de qué?
**5... 4... 3... 2... 1...**
**Respuesta:** Del estado actual.

**Pregunta:** ¿Cómo se pasan datos de un widget padre a un widget hijo?
**5... 4... 3... 2... 1...**
**Respuesta:** A través del constructor del widget hijo, como propiedades.

**Pregunta:** ¿Cómo se reconstruye una interfaz de usuario en Flutter cuando el estado cambia?
**5... 4... 3... 2... 1...**
**Respuesta:** Flutter automáticamente reconstruye la parte de la interfaz de usuario que depende de ese estado.