# 3.1. Widgets de desplazamiento: SingleChildScrollView, CustomScrollView (3.1)

## Introducción

Este tema es crucial para cualquier desarrollador web que se adentra en Flutter.  Controlar el desplazamiento es fundamental para crear interfaces de usuario fluidas y usables, especialmente en dispositivos móviles con pantallas de diferentes tamaños.  En la web, estamos acostumbrados a que el navegador gestione el scroll de manera predeterminada cuando el contenido excede la altura de la ventana.  En Flutter, necesitamos explícitamente manejar el desplazamiento con widgets como `SingleChildScrollView` y `CustomScrollView`. Piensa en estos widgets como el equivalente a envolver tu contenido en un `<div>` con `overflow: auto` en CSS, pero con mucho más control y personalización.

## Explicación

En Flutter, cuando el contenido de un widget excede las dimensiones disponibles, necesitamos proporcionar una forma para que el usuario pueda desplazarse y ver todo.  El widget más sencillo para lograr esto es `SingleChildScrollView`.  Imagina que tienes un formulario largo o una lista de elementos que no caben en la pantalla. Envolver ese contenido con `SingleChildScrollView` automáticamente añade la capacidad de desplazamiento vertical (por defecto).

`SingleChildScrollView` es ideal para situaciones simples donde tienes un único bloque de contenido que necesita ser desplazable.  Sin embargo, tiene una limitación importante: carga todo el contenido hijo de golpe, incluso si no es visible inicialmente.  Esto puede ser ineficiente para listas largas o contenidos complejos.

Aquí es donde entra `CustomScrollView`.  `CustomScrollView` ofrece un control mucho más granular sobre el comportamiento del desplazamiento.  En lugar de simplemente envolver un widget, `CustomScrollView` acepta una lista de "slivers". Un sliver es una porción de contenido desplazable que puede tener un comportamiento de desplazamiento específico.  Piensa en `CustomScrollView` como una forma de componer el comportamiento de desplazamiento, permitiéndote crear efectos como barras de herramientas colapsables, listas con encabezados pegajosos y mucho más.

Para un desarrollador web, la flexibilidad de `CustomScrollView` se asemeja a la capacidad de JavaScript de manipular el comportamiento del scroll de un elemento, pero de una manera mucho más declarativa y estructurada.  En lugar de adjuntar event listeners y calcular posiciones, defines las características del desplazamiento mediante widgets predefinidos como `SliverAppBar`, `SliverList`, y `SliverGrid`.

Es importante recordar que, a diferencia del modelo de caja del navegador web, en Flutter la altura de los widgets padre influye en la forma en que sus hijos se renderizan. En ocasiones, es necesario especificar la altura de un widget que contiene el scroll para que funcione correctamente.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos.

Aquí hay algunos conceptos clave:

*   **SingleChildScrollView:** Para desplazamiento simple de un único hijo.
*   **CustomScrollView:** Para control avanzado del desplazamiento con slivers.
*   **SliverAppBar:** Un AppBar que se comporta como un sliver, colapsando al hacer scroll.
*   **SliverList:**  Lista de widgets que se desplaza como un sliver.
*   **SliverGrid:** Cuadrícula de widgets que se desplaza como un sliver.

```dart
// Ejemplo 1: SingleChildScrollView
import 'package:flutter/material.dart';

class SingleChildScrollViewExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('SingleChildScrollView')),
      body: SingleChildScrollView( // Envuelve el contenido para permitir el scroll
        child: Column( // Usamos Column para apilar widgets verticalmente
          children: List.generate(
            20, // Generamos 20 contenedores
            (index) => Container(
              height: 100,
              color: index % 2 == 0 ? Colors.blue[100] : Colors.green[100],
              child: Center(child: Text('Item $index')),
            ),
          ),
        ),
      ),
    );
  }
}
```

```dart
// Ejemplo 2: CustomScrollView con SliverAppBar y SliverList
import 'package:flutter/material.dart';

class CustomScrollViewExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: <Widget>[
          SliverAppBar( // AppBar que se colapsa al hacer scroll
            expandedHeight: 200.0,
            floating: false,
            pinned: true, // Mantener el AppBar fijo en la parte superior
            flexibleSpace: FlexibleSpaceBar(
              title: Text('CustomScrollView Demo'),
              background: Image.network(
                'https://via.placeholder.com/350x200',
                fit: BoxFit.cover,
              ),
            ),
          ),
          SliverList( // Lista de widgets desplazable
            delegate: SliverChildBuilderDelegate(
              (BuildContext context, int index) {
                return Container(
                  height: 50,
                  color: index % 2 == 0 ? Colors.grey[300] : Colors.white,
                  child: Center(child: Text('Item $index')),
                );
              },
              childCount: 50, // Número de elementos en la lista
            ),
          ),
        ],
      ),
    );
  }
}
```

```dart
// Ejemplo 3: CustomScrollView con SliverGrid

import 'package:flutter/material.dart';

class CustomScrollViewGridExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: <Widget>[
          SliverGrid( // Cuadrícula de widgets desplazable
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2, // Dos columnas
            ),
            delegate: SliverChildBuilderDelegate(
              (BuildContext context, int index) {
                return Container(
                  margin: EdgeInsets.all(8.0),
                  decoration: BoxDecoration(
                    color: Colors.orange[100],
                    borderRadius: BorderRadius.circular(10.0),
                  ),
                  child: Center(child: Text('Grid Item $index')),
                );
              },
              childCount: 10, // Número de elementos en la cuadrícula
            ),
          ),
        ],
      ),
    );
  }
}
```

## Práctica: Preguntas y Respuestas

**Pregunta:** ¿Cuándo deberías usar `SingleChildScrollView` en lugar de `CustomScrollView`?
**5... 4... 3... 2... 1...**
**Respuesta:** Cuando tienes un solo bloque de contenido que necesita desplazamiento y la carga inicial de todo el contenido no es un problema de rendimiento.

**Pregunta:** ¿Qué son los "slivers" en el contexto de `CustomScrollView`?
**5... 4... 3... 2... 1...**
**Respuesta:** Son porciones de contenido desplazable que pueden tener comportamientos de desplazamiento específicos.  Piensa en ellos como los bloques de construcción de tu scroll.

**Pregunta:** ¿Cuál es la función del widget `SliverAppBar`?
**5... 4... 3... 2... 1...**
**Respuesta:** Es un `AppBar` que se integra con el comportamiento de desplazamiento de un `CustomScrollView`, permitiendo que se colapse o se mantenga fijo en la parte superior al hacer scroll.

**Pregunta:** ¿Cómo se define el diseño de los elementos dentro de un `SliverGrid`?
**5... 4... 3... 2... 1...**
**Respuesta:** Se usa un `SliverGridDelegate`, como `SliverGridDelegateWithFixedCrossAxisCount`, para controlar el número de columnas y otros aspectos del diseño de la cuadrícula.

**Pregunta:** ¿Cuál es el equivalente web más cercano al comportamiento del `SliverAppBar`?
**5... 4... 3... 2... 1...**
**Respuesta:**  Un elemento `header` con la propiedad CSS `position: sticky` combinado con JavaScript para modificar su apariencia al hacer scroll.  `SliverAppBar` lo hace de forma declarativa en Flutter.
