# 1.8. Widgets de diseño básicos: Container, Row, Column (1.8)

## Introducción

Para un desarrollador web que se adentra en el mundo de Flutter, comprender los widgets de diseño básicos como `Container`, `Row` y `Column` es fundamental.  Estos widgets son los cimientos sobre los cuales construirás interfaces de usuario complejas y receptivas. Piensa en el `Container` como el equivalente a un `div` en HTML, permitiéndote envolver y estilizar otros widgets.  `Row` y `Column` son similares a usar `display: flex;` con `flex-direction: row` o `flex-direction: column` en CSS, facilitando la organización horizontal o vertical de elementos. Conocerlos te permitirá traducir tu experiencia en diseño web a Flutter de manera efectiva.

## Explicación

En esta sección, exploraremos estos widgets de diseño básicos en detalle, enfocándonos en sus similitudes y diferencias con los conceptos que ya conoces del desarrollo web.

El widget `Container` es uno de los más versátiles en Flutter.  En esencia, es una caja que puede contener otro widget.  Piensa en él como un `div` en HTML, pero con esteroides.  Puedes controlar su tamaño, agregarle bordes, márgenes, padding, fondos y aplicar transformaciones.  En Flutter, la mayoría de las propiedades de estilo se configuran a través de la propiedad `decoration` del `Container`, que acepta un objeto `BoxDecoration`.  Este objeto te permite definir características como el color de fondo, el borde, la sombra y la forma del contenedor.

El widget `Row` se utiliza para organizar widgets horizontalmente.  Imagina que quieres colocar varios botones uno al lado del otro.  En HTML, podrías usar `display: inline-block` o `flexbox`.  En Flutter, usarías un `Row`.  El `Row` recibe una lista de widgets como hijos a través de la propiedad `children`.  Puedes controlar la alineación de los widgets dentro del `Row` utilizando la propiedad `mainAxisAlignment` para la alineación horizontal y `crossAxisAlignment` para la alineación vertical.  Estas propiedades son análogas a las propiedades `justify-content` y `align-items` de CSS flexbox.

El widget `Column` es similar a `Row`, pero organiza los widgets verticalmente.  Es el equivalente de usar `flex-direction: column` en CSS.  Al igual que `Row`, `Column` recibe una lista de widgets como hijos a través de la propiedad `children`.  También puedes controlar la alineación de los widgets dentro del `Column` utilizando las propiedades `mainAxisAlignment` y `crossAxisAlignment`, que funcionan de manera similar a `Row`, pero invierten la dirección de la alineación principal y cruzada.

La clave para dominar estos widgets es entender cómo funcionan juntos.  A menudo, combinarás `Container` con `Row` y `Column` para crear diseños complejos.  Por ejemplo, puedes usar un `Container` para agregar padding alrededor de un `Row` o `Column`.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos para solidificar tu comprensión.

Aquí tienes algunas frases útiles:

*   `Container`: El "div" de Flutter.
*   `Row`: Organiza widgets horizontalmente.
*   `Column`: Organiza widgets verticalmente.
*   `children`: Propiedad que contiene la lista de widgets hijos.
*   `mainAxisAlignment`: Controla la alineación a lo largo del eje principal.
*   `crossAxisAlignment`: Controla la alineación a lo largo del eje transversal.

```dart
// Un Container simple con un texto en su interior.
Container(
  child: Text('Hola, Mundo!'), // El texto es el hijo del Container.
  padding: EdgeInsets.all(20), // Agrega padding alrededor del texto.
  decoration: BoxDecoration( // Define la apariencia del Container.
    color: Colors.blue, // Color de fondo azul.
  ),
)
```

```dart
// Un Row que contiene dos botones.
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly, // Distribuye los botones uniformemente.
  children: [
    ElevatedButton(onPressed: () {}, child: Text('Botón 1')),
    ElevatedButton(onPressed: () {}, child: Text('Botón 2')),
  ],
)
```

```dart
// Un Column que contiene dos textos.
Column(
  crossAxisAlignment: CrossAxisAlignment.start, // Alinea el texto a la izquierda.
  children: [
    Text('Texto 1'),
    Text('Texto 2'),
  ],
)
```

```dart
// Anidando Container, Row y Column.
Container(
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(color: Colors.grey[200]),
  child: Column(
    children: [
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text('Producto:'),
          Text('Precio: \$19.99'),
        ],
      ),
      SizedBox(height: 8), // Widget para agregar espacio.  Similar a <br> o margin/padding en CSS
      Text('Descripción del producto aquí.'),
    ],
  ),
)
```

## Práctica: Preguntas y Respuestas

Aquí hay algunas preguntas para poner a prueba tu comprensión.

**Pregunta:** ¿Cuál es la propiedad principal que contiene la lista de widgets hijos en un `Row` o `Column`?
**5... 4... 3... 2... 1...**
**Respuesta:** La propiedad `children`.

**Pregunta:** ¿Qué widget usarías en Flutter para crear una caja con un color de fondo y padding alrededor de otro widget?
**5... 4... 3... 2... 1...**
**Respuesta:** El widget `Container`.

**Pregunta:** ¿Cuál es el propósito de `mainAxisAlignment` en un `Row` o `Column`?
**5... 4... 3... 2... 1...**
**Respuesta:** Controla la alineación de los widgets a lo largo del eje principal (horizontal para `Row`, vertical para `Column`).

**Pregunta:** ¿Cómo puedes agregar un espacio vertical entre widgets dentro de un `Column`?
**5... 4... 3... 2... 1...**
**Respuesta:** Puedes usar el widget `SizedBox` con la propiedad `height` o aplicar padding o margin al widget en cuestión.

**Pregunta:** ¿Cómo se compara el widget Container con un elemento HTML común?
**5... 4... 3... 2... 1...**
**Respuesta:** Es similar a un `div` en HTML, permitiendo envolver, estilizar y manipular la disposición de otros widgets.
