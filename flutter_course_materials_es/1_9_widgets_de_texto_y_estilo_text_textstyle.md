# 1.9. Widgets de texto y estilo: Text, TextStyle

## Introducción

Para un desarrollador web que se adentra en el mundo de Flutter, comprender cómo manejar el texto y su estilo es fundamental.  Similar a como usas etiquetas HTML como `<p>`, `<h1>`, `<span>` y hojas de estilo CSS para controlar la apariencia del texto en la web, Flutter ofrece el widget `Text` y la clase `TextStyle` para lograr resultados similares. Este conocimiento te permitirá crear interfaces de usuario con texto legible, atractivo y personalizado. Considera el widget `Text` como el equivalente a un elemento HTML para mostrar texto, y `TextStyle` como tu CSS en línea para darle estilo.

## Explicación

En Flutter, el widget `Text` es la herramienta principal para mostrar texto en la pantalla. A diferencia de HTML, donde el texto reside directamente dentro de las etiquetas, en Flutter el texto es una propiedad del widget `Text`.  Piensa en ello como si tuvieras un componente que *sólo* puede mostrar texto.

Para controlar cómo se ve el texto, utilizas la clase `TextStyle`.  `TextStyle` te permite modificar la fuente, el tamaño, el color, el peso (negrita), la altura de la línea, el espaciado entre letras y mucho más.  En lugar de declarar clases CSS, aplicas estos estilos directamente dentro del widget `Text`.  Esencialmente, el `TextStyle` es como un objeto que contiene todas las propiedades de estilo que deseas aplicar a tu texto.

La principal diferencia entre el estilo web tradicional y el estilo en Flutter radica en que los estilos se aplican directamente en el código Flutter, en lugar de en archivos CSS separados.  Esto puede parecer diferente al principio, pero permite una mayor flexibilidad y control granular sobre el estilo de tu aplicación.

Un ejemplo sencillo de cómo mostrar texto en Flutter sería:

```dart
Text('Hola, mundo!')
```

Este código mostrará el texto "Hola, mundo!" con el estilo predeterminado.  Para personalizar su apariencia, usaríamos la propiedad `style` del widget `Text` y le proporcionaríamos un objeto `TextStyle`.

Por ejemplo, para mostrar el mismo texto en negrita y de color azul, haríamos lo siguiente:

```dart
Text(
  'Hola, mundo!',
  style: TextStyle(
    fontWeight: FontWeight.bold,
    color: Colors.blue,
  ),
)
```

Este código ahora mostrará el texto "Hola, mundo!" en negrita y con color azul. Observa cómo el `TextStyle` se define directamente dentro del widget `Text`.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos para solidificar tu comprensión.

Aquí tienes algunos conceptos y código clave relacionados con el uso de texto y estilo en Flutter:

*   El widget `Text`:  el componente fundamental para mostrar texto.
*   La clase `TextStyle`:  permite personalizar la apariencia del texto.
*   Propiedades de `TextStyle`: `fontWeight`, `fontSize`, `color`, `fontFamily`, `letterSpacing`, `wordSpacing`, `height`, `decoration`, etc.

Aquí hay algunos fragmentos de código Flutter que demuestran el uso de `Text` y `TextStyle`:

*   **Ejemplo 1: Texto con tamaño y color personalizados:**

```dart
Text(
  'Este texto es grande y rojo.',
  style: TextStyle(
    fontSize: 24, // Similar a font-size en CSS
    color: Colors.red, // Similar a color en CSS
  ),
)
```

*   **Ejemplo 2: Texto con fuente diferente y espaciado entre letras:**

```dart
Text(
  'Texto con fuente diferente y espaciado.',
  style: TextStyle(
    fontFamily: 'Roboto', // La fuente de letra
    letterSpacing: 2.0, // Espacio entre letras
  ),
)
```

*   **Ejemplo 3: Texto con decoración de subrayado:**

```dart
Text(
  'Este texto está subrayado.',
  style: TextStyle(
    decoration: TextDecoration.underline, // Añade un subrayado
  ),
)
```

*   **Ejemplo 4:  Texto con múltiples estilos combinados:**

```dart
Text(
  'Texto negrita, itálica y azul.',
  style: TextStyle(
    fontWeight: FontWeight.bold, // Pone el texto en negrita
    fontStyle: FontStyle.italic, // Pone el texto en itálica
    color: Colors.blue, // Define el color del texto
  ),
)
```

## Práctica: Preguntas y Respuestas

**Pregunta:** ¿Cómo se declara un widget `Text` básico en Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** `Text('Tu texto aquí')`

**Pregunta:** ¿Qué clase se utiliza para aplicar estilos a un widget `Text`?
**5... 4... 3... 2... 1...**
**Respuesta:** La clase `TextStyle`.

**Pregunta:** ¿Cómo harías para que un texto aparezca en negrita? Menciona la propiedad específica de `TextStyle`.
**5... 4... 3... 2... 1...**
**Respuesta:** Utilizarías la propiedad `fontWeight: FontWeight.bold` dentro de `TextStyle`.

**Pregunta:** ¿Cuál es el propósito de la propiedad `fontSize` dentro de `TextStyle`?
**5... 4... 3... 2... 1...**
**Respuesta:** Define el tamaño de la fuente del texto, similar a `font-size` en CSS.
