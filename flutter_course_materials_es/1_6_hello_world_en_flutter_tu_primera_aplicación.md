
# 1.6. Hello World en Flutter: Tu primera aplicación

## Introducción

Para un desarrollador web que se aventura en el mundo de Flutter, crear una aplicación "Hello World" es un paso fundamental. Piensa en ello como escribir tu primer HTML, CSS y JavaScript, pero para construir aplicaciones móviles y de escritorio. Entender este ejemplo básico sienta las bases para proyectos más complejos y te familiariza con la estructura y la sintaxis de Flutter. La analogía más directa es la creación de un archivo `index.html` básico con un `<h1>Hello World</h1>` estilizado con CSS y potencialmente interactivo con JavaScript. En Flutter, se transforma en código Dart que utiliza widgets para la interfaz de usuario.

## Explicación

Flutter utiliza un paradigma declarativo para construir interfaces de usuario.  Esto significa que describes _cómo_ quieres que se vea tu interfaz, y Flutter se encarga de renderizarla eficientemente. En el mundo web, esto se asemeja a describir tu HTML y CSS y dejar que el navegador se encargue de mostrarlo. La diferencia clave radica en que en lugar de manipular directamente el DOM (Document Object Model) como lo harías con JavaScript, construyes una jerarquía de widgets.

El widget más básico es `Text`, que, como su nombre indica, muestra texto. Para organizar y dar estilo a estos widgets, se utilizan widgets como `Container`, `Column`, `Row` y `Center`. `Container` es similar a un `div` en HTML, permitiendo agrupar y aplicar estilos a otros widgets.  `Column` y `Row` son como flexbox o grid en CSS, facilitando la disposición de los widgets verticalmente o horizontalmente. `Center` es una forma sencilla de centrar el contenido dentro de su padre, similar a `display: flex; justify-content: center; align-items: center;` en CSS.

El punto de entrada de una aplicación Flutter es la función `main()`.  Dentro de `main()`, típicamente llamas a la función `runApp()` con el widget raíz de tu aplicación. Este widget raíz suele ser un `MaterialApp` o un `CupertinoApp`, que proporcionan un tema visual y estructura básica para tu aplicación, ya sea con un estilo Material Design o iOS, respectivamente. El widget que pasas a `runApp()` es el equivalente a la estructura básica de tu página web.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos para comprender mejor cómo construir una aplicación "Hello World" en Flutter.

Aquí tienes algunos conceptos clave:
*   `main()`: La función principal, el punto de entrada de tu aplicación.
*   `runApp()`: Inicia la aplicación Flutter con un widget dado.
*   `MaterialApp`: Un widget que implementa la estructura básica de la aplicación con Material Design.
*   `Scaffold`: Proporciona la estructura visual básica para las pantallas, como la barra de aplicación, el cuerpo y los botones flotantes.
*   `Center`: Centra su hijo en sí mismo.
*   `Text`: Muestra texto.

Aquí tienes algunos fragmentos de código Flutter:

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      home: Scaffold( // El Scaffold proporciona la estructura básica de la interfaz de usuario
        appBar: AppBar(
          title: const Text('Hello World'),
        ),
        body: const Center( // El Center widget centra su hijo
          child: Text('Hello World!'),
        ),
      ),
    ),
  );
}
```

Otro ejemplo, usando un Container para añadir padding:

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Hello World'),
        ),
        body: Center(
          child: Container(
            padding: const EdgeInsets.all(20.0), // Similar a añadir padding con CSS
            child: const Text('Hello World!'),
          ),
        ),
      ),
    ),
  );
}
```

Un ejemplo mostrando el texto con un estilo específico:

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Hello World'),
        ),
        body: const Center(
          child: Text(
            'Hello World!',
            style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold), //Similar a aplicar estilos CSS
          ),
        ),
      ),
    ),
  );
}
```

## Práctica: Preguntas y Respuestas

**Pregunta:** ¿Qué widget es esencial para proporcionar un tema visual de Material Design a tu aplicación Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** El widget `MaterialApp`.

**Pregunta:** ¿Qué widget se utiliza para mostrar texto en Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** El widget `Text`.

**Pregunta:** ¿Qué widget usarías para agrupar otros widgets y aplicar estilos de manera similar a un `div` en HTML?
**5... 4... 3... 2... 1...**
**Respuesta:** El widget `Container`.

**Pregunta:** ¿Qué función es el punto de entrada de tu aplicación Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** La función `main()`.

**Pregunta:** ¿Qué widget se usa para centrar otro widget en la pantalla?
**5... 4... 3... 2... 1...**
**Respuesta:** El widget `Center`.
