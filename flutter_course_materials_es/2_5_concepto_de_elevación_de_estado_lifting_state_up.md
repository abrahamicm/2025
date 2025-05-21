# 2.5. Concepto de elevación de estado (lifting state up) (2.5)

## Introducción

Para un desarrollador web que se adentra en el mundo de Flutter, comprender el concepto de elevación de estado es crucial, ya que permite crear aplicaciones interactivas y dinámicas. En la web, estamos familiarizados con el DOM y cómo los componentes JavaScript pueden modificar el estado de otros elementos. En Flutter, la elevación de estado es el mecanismo principal para lograr interacciones similares entre widgets, permitiendo que los cambios en un widget influyan en otros. Piénsalo como la versión Flutter de una combinación de eventos, manejo del DOM y, en frameworks más modernos, el flujo de datos unidireccional de React o Vue.

## Explicación

La elevación de estado, o "lifting state up" como se le conoce comúnmente, se refiere al proceso de mover el estado de un widget hijo a un widget padre. ¿Por qué querríamos hacer esto? La razón principal es permitir que varios widgets compartan y modifiquen ese estado.  Imagina una aplicación web con un campo de texto y un botón. El texto ingresado en el campo necesita ser utilizado por el botón para realizar alguna acción. En Flutter, si el estado (el texto ingresado) está contenido solo en el widget del campo de texto, el botón no tendrá acceso a él directamente.

La solución es "elevar" ese estado al padre común de ambos widgets.  El widget padre, ahora poseedor del estado, puede pasarlo a ambos widgets hijos como propiedades (argumentos de constructor o parámetros de función).  Cuando el estado cambia en el widget del campo de texto, el padre actualiza su propio estado y, como resultado, vuelve a renderizar ambos widgets hijos con los nuevos valores.

En esencia, estamos moviendo la fuente de la verdad (el estado) a un lugar más alto en el árbol de widgets, permitiendo que todos los widgets que necesiten acceder a ese estado lo hagan a través de su padre común. Esto asegura la coherencia de la información a través de la aplicación y facilita la gestión de interacciones complejas. Piénsalo como centralizar la gestión de datos en un solo punto.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos para comprender mejor cómo se aplica la elevación de estado en Flutter. Aquí tienes algunos conceptos clave y fragmentos de código.

- **`StatefulWidget`:** La base para manejar estados mutables en Flutter.
- **`setState()`:** Función que notifica al framework que el estado ha cambiado, provocando una reconstrucción del widget.
- **Callbacks (Funciones de Retorno):** Usadas para comunicar eventos desde los widgets hijos al padre.
- **Properties (Propiedades):** Valores pasados desde el widget padre al widget hijo.

Aquí tienes algunos fragmentos de código para ilustrar esto:

```dart
// Widget padre que mantiene el estado.
class ParentWidget extends StatefulWidget {
  const ParentWidget({Key? key}) : super(key: key);

  @override
  _ParentWidgetState createState() => _ParentWidgetState();
}

class _ParentWidgetState extends State<ParentWidget> {
  String _message = 'Mensaje inicial'; // Estado inicial.

  // Función para actualizar el estado desde los widgets hijos.
  void _updateMessage(String newMessage) {
    setState(() {
      _message = newMessage;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ChildWidget(
          message: _message, // Pasando el estado al hijo.
          onMessageChanged: _updateMessage, // Pasando el callback.
        ),
        Text('Mensaje del Padre: $_message'), // Mostrando el estado del padre.
      ],
    );
  }
}
```

```dart
// Widget hijo que recibe el estado y puede modificarlo a través del callback.
class ChildWidget extends StatelessWidget {
  final String message;
  final Function(String) onMessageChanged; // Callback para notificar al padre.

  const ChildWidget({Key? key, required this.message, required this.onMessageChanged}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextField(
      decoration: InputDecoration(labelText: 'Introduce un mensaje'),
      onChanged: (text) {
        onMessageChanged(text); // Llama al callback con el nuevo valor.
      },
      controller: TextEditingController(text: message), // Inicializa el campo de texto con el estado actual.
    );
  }
}
```

En este ejemplo, `ParentWidget` mantiene el estado `_message`. `ChildWidget` es un campo de texto que permite modificar ese mensaje.  Cuando el usuario escribe en el campo de texto, el callback `onMessageChanged` llama a la función `_updateMessage` en el `ParentWidget`, actualizando su estado y provocando una reconstrucción.  El `ParentWidget` luego vuelve a pasar el nuevo valor de `_message` al `ChildWidget` como su propiedad `message`.

## Práctica: Preguntas y Respuestas

Vamos a repasar con algunas preguntas y respuestas para solidificar tu comprensión.

**Pregunta:** ¿Por qué es importante elevar el estado en Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** Permite que múltiples widgets compartan y modifiquen el mismo estado, manteniendo la coherencia de la información.

**Pregunta:** ¿Qué widget se utiliza normalmente para mantener el estado que se va a elevar?
**5... 4... 3... 2... 1...**
**Respuesta:** Un `StatefulWidget`.

**Pregunta:** ¿Cómo un widget hijo comunica un cambio de estado a su widget padre en el patrón de elevación de estado?
**5... 4... 3... 2... 1...**
**Respuesta:** A través de un callback (una función pasada como propiedad).

**Pregunta:** ¿Qué método se llama para notificar a Flutter que el estado ha cambiado, provocando una reconstrucción del widget?
**5... 4... 3... 2... 1...**
**Respuesta:** El método `setState()`.

**Pregunta:** En la web, podríamos usar querySelectors y JavaScript para interactuar con el DOM. ¿Cuál es el equivalente más cercano en Flutter para que un widget hijo afecte visualmente a un widget padre?
**5... 4... 3... 2... 1...**
**Respuesta:** Elevar el estado al widget padre y luego pasar el nuevo estado como propiedades a todos los widgets hijos que necesiten reflejar ese cambio.
