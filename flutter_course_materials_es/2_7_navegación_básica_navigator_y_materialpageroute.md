# 2.7. Navegación básica: Navigator y MaterialPageRoute (2.7)

## Introducción

La navegación es fundamental en cualquier aplicación, tanto web como móvil. Para un desarrollador web que se adentra en Flutter, comprender cómo funciona la navegación es esencial para crear interfaces de usuario interactivas y fluidas. En la web, gestionamos la navegación principalmente a través de enlaces HTML (`<a href="...">`) y, a menudo, con manipulación del historial del navegador mediante JavaScript. Flutter ofrece su propio sistema, basado en el `Navigator` y las rutas (usualmente implementadas con `MaterialPageRoute`), que es similar en concepto pero diferente en implementación. Esta lección te guiará a través de los conceptos básicos de la navegación en Flutter, comparándolos cuando sea posible con tus conocimientos de desarrollo web.

## Explicación

En Flutter, la navegación se gestiona principalmente con el widget `Navigator`. Piensa en el `Navigator` como una pila de pantallas, donde cada pantalla es un `Route`.  Cuando "navegas" a una nueva pantalla, estás esencialmente *empujando* un nuevo `Route` a la parte superior de esta pila.  Cuando retrocedes, estás *sacando* la pantalla actual de la pila, revelando la anterior.

Un `Route` es una abstracción de una pantalla o página. Flutter proporciona varios tipos de `Route`, siendo `MaterialPageRoute` el más común. `MaterialPageRoute` proporciona las transiciones visuales típicas de Material Design al navegar entre pantallas.

En la web, tienes URLs que identifican diferentes páginas. En Flutter, aunque puedes implementar conceptos similares para la navegación profunda, inicialmente trabajas con `Route`s definidos dentro de tu aplicación. La analogía más cercana sería pensar en cada `Route` como un componente separado que renderizas en tu SPA (Single Page Application) web.

Para navegar a una nueva pantalla, usas el método `Navigator.push()`.  Para volver a la pantalla anterior, usas `Navigator.pop()`.

Imagina que tienes dos widgets: `PrimeraPantalla` y `SegundaPantalla`. Para navegar de la `PrimeraPantalla` a la `SegundaPantalla`, el código sería similar a este:

```dart
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => SegundaPantalla()),
);
```

`context` es una pieza clave.  Esencialmente, proporciona información sobre la ubicación del widget en el árbol de widgets. `MaterialPageRoute` necesita un `builder` que define el widget que se mostrará en la nueva pantalla.

Para volver a la `PrimeraPantalla` desde la `SegundaPantalla`, usarías:

```dart
Navigator.pop(context);
```

Esto es similar a presionar el botón "Atrás" en un navegador web, solo que lo haces explícitamente en tu código Flutter.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos.

Aquí tienes algunos conceptos clave de Flutter relacionados con la navegación:

*   `Navigator`: El widget que gestiona la pila de rutas.
*   `MaterialPageRoute`:  Un tipo de `Route` con transiciones Material Design.
*   `Navigator.push()`:  Empuja una nueva `Route` a la pila del `Navigator`.
*   `Navigator.pop()`:  Saca la `Route` actual de la pila del `Navigator`.
*   `context`: Proporciona información sobre la ubicación del widget en el árbol de widgets.

Aquí hay algunos fragmentos de código que demuestran el uso correcto:

```dart
// Definición de la Primera Pantalla
class PrimeraPantalla extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Primera Pantalla'),
      ),
      body: Center(
        child: ElevatedButton(
          child: Text('Ir a la Segunda Pantalla'),
          onPressed: () {
            // Navega a la segunda pantalla usando Navigator.push
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => SegundaPantalla()),
            );
          },
        ),
      ),
    );
  }
}
```

```dart
// Definición de la Segunda Pantalla
class SegundaPantalla extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Segunda Pantalla'),
      ),
      body: Center(
        child: ElevatedButton(
          child: Text('Volver a la Primera Pantalla'),
          onPressed: () {
            // Vuelve a la primera pantalla usando Navigator.pop
            Navigator.pop(context);
          },
        ),
      ),
    );
  }
}
```

```dart
// Ejemplo dentro de un Widget personalizado
ElevatedButton(
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => NuevaPantalla()), //Reemplaza NuevaPantalla() con tu widget.
    );
  },
  child: Text('Ir a la Nueva Pantalla'),
)
```

## Práctica: Preguntas y Respuestas

Aquí hay algunas preguntas para poner a prueba tu comprensión:

**Pregunta:** ¿Qué widget gestiona la pila de rutas en Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** El `Navigator`.

**Pregunta:** ¿Qué método se utiliza para agregar una nueva pantalla a la pila de navegación?
**5... 4... 3... 2... 1...**
**Respuesta:** `Navigator.push()`.

**Pregunta:** ¿Qué método se utiliza para volver a la pantalla anterior?
**5... 4... 3... 2... 1...**
**Respuesta:** `Navigator.pop()`.

**Pregunta:** ¿Qué es `MaterialPageRoute`?
**5... 4... 3... 2... 1...**
**Respuesta:** Es un tipo de `Route` que proporciona transiciones visuales de Material Design.

**Pregunta:** ¿Qué rol juega el `context` en la navegación?
**5... 4... 3... 2... 1...**
**Respuesta:** Proporciona información sobre la ubicación del widget en el árbol de widgets, lo cual es necesario para acceder al `Navigator`.