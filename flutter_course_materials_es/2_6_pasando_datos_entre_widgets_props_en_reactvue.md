# 2.6. Pasando datos entre Widgets (props en React/Vue) (2.6)

## Introducción

Para un desarrollador web que se adentra en el mundo de Flutter, comprender cómo pasar datos entre widgets es fundamental, tal como lo es la gestión de props en React o Vue. Piénsalo como transferir información a través de atributos HTML, o como el paso de propiedades a un componente reutilizable en JavaScript. En Flutter, esta comunicación se realiza mediante el constructor de un widget. Dominar esta habilidad te permitirá crear interfaces de usuario dinámicas y componentes reutilizables, facilitando la construcción de aplicaciones complejas de manera eficiente.

## Explicación

En Flutter, la transferencia de datos entre widgets se realiza principalmente a través del constructor del widget hijo.  Imagina que tienes un widget padre y un widget hijo. El widget padre puede "enviar" datos al widget hijo al crear una instancia de este último y pasarle valores a través de sus parámetros del constructor. Estos parámetros actúan como los "props" de React o Vue.

Por ejemplo, si tienes un widget `MiTexto` que muestra texto, puedes permitir que el widget padre controle el texto que se muestra pasando un valor de cadena al constructor de `MiTexto`.  De esta forma, el widget `MiTexto` se vuelve más flexible y reutilizable, ya que puede mostrar diferentes textos dependiendo de los datos que reciba.

A diferencia de React o Vue donde los props pueden ser mutables (aunque no se recomienda mutarlos directamente), en Flutter los widgets son inmutables. Esto significa que una vez creados, sus propiedades no pueden cambiar directamente.  Si necesitas cambiar los datos que se muestran, debes reconstruir el widget con los nuevos datos, a través de un cambio de estado en su widget padre, esto se logra a través de `setState`, un concepto que veremos más adelante. Esto ayuda a mejorar el rendimiento y la previsibilidad de la aplicación.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos.

- **Widget personalizado con un constructor que acepta datos.**
- **Uso del widget padre para pasar datos al widget hijo.**

Aquí tienes algunos fragmentos de código útiles:

```dart
import 'package:flutter/material.dart';

class MiTexto extends StatelessWidget {
  final String texto; // Declaración de la propiedad 'texto'

  MiTexto({required this.texto}); // Constructor que recibe el texto. La palabra 'required' significa que este parámetro es obligatorio.

  @override
  Widget build(BuildContext context) {
    return Text(
      texto, // Muestra el texto recibido
      style: TextStyle(fontSize: 20),
    );
  }
}
```

```dart
class MiPagina extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Pasando Datos')),
      body: Center(
        child: MiTexto(texto: '¡Hola desde el Widget Padre!'), // Pasando el texto como argumento
      ),
    );
  }
}
```

```dart
//Un ejemplo de widget que recibe un color
class Cuadrado extends StatelessWidget {
  final Color color;

  Cuadrado({required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 100,
      height: 100,
      color: color,
    );
  }
}

class MiPantalla extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Cuadrados de Colores')),
      body: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          Cuadrado(color: Colors.red), //Un cuadrado rojo
          Cuadrado(color: Colors.blue), //Un cuadrado azul
          Cuadrado(color: Colors.green), //Un cuadrado verde
        ],
      ),
    );
  }
}
```

## Práctica: Preguntas y Respuestas

Ahora, pongamos a prueba lo que hemos aprendido con algunas preguntas y respuestas.

**Pregunta:** ¿Cómo se pasan datos de un widget padre a un widget hijo en Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** A través del constructor del widget hijo. El widget padre crea una instancia del widget hijo y le pasa los datos como argumentos al constructor.

**Pregunta:** ¿Qué palabra clave se usa para indicar que un parámetro en el constructor de un widget es obligatorio?
**5... 4... 3... 2... 1...**
**Respuesta:** La palabra clave `required`.

**Pregunta:** ¿Los widgets en Flutter son mutables o inmutables?
**5... 4... 3... 2... 1...**
**Respuesta:** Los widgets en Flutter son inmutables. Una vez creados, sus propiedades no pueden cambiar directamente.

**Pregunta:** Si necesito cambiar la información mostrada en un widget, ¿qué debo hacer?
**5... 4... 3... 2... 1...**
**Respuesta:**  Debes reconstruir el widget con los nuevos datos, usualmente a través de un cambio de estado en su widget padre.
