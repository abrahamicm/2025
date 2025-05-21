# 1.4. Conceptos básicos de Dart: Estructuras de control (if/else, loops) (1.4)

## Introducción

Para un desarrollador web que se adentra en el mundo de Flutter, comprender las estructuras de control en Dart es fundamental. Las estructuras de control, como las sentencias `if/else` y los bucles, son los pilares de la lógica de cualquier aplicación.  Son análogas a cómo usas CSS para controlar el estilo visual de los elementos HTML, pero en Dart controlan el flujo de la ejecución del código. Imagina `if/else` como condiciones CSS basadas en media queries, y los bucles como iterar sobre una lista de elementos con JavaScript. Domina estos conceptos en Dart y estarás bien encaminado para construir aplicaciones Flutter interactivas y dinámicas.

## Explicación

En esta sección, exploraremos las estructuras de control fundamentales en Dart: las sentencias `if/else` y los bucles, tales como `for` y `while`. Estas estructuras te permiten controlar el flujo de ejecución de tu código basándote en ciertas condiciones o repetir un bloque de código varias veces.

Las sentencias `if/else` son la base de la toma de decisiones en Dart. Funcionan de manera muy similar a como lo hacen en JavaScript.  La sentencia `if` evalúa una condición y, si es verdadera, ejecuta un bloque de código. Si la condición es falsa, puedes usar la sentencia `else` para ejecutar un bloque de código alternativo.  También puedes encadenar múltiples condiciones utilizando `else if`.  Piensa en esto como las cascadas de estilos en CSS, donde la regla más específica (o en este caso, la condición verdadera) se aplica.

Por ejemplo, consideremos el siguiente código:

```dart
void main() {
  int edad = 20;

  if (edad >= 18) {
    print("Eres mayor de edad.");
  } else {
    print("Eres menor de edad.");
  }
}
```

En este caso, si la variable `edad` es mayor o igual a 18, se imprimirá "Eres mayor de edad". De lo contrario, se imprimirá "Eres menor de edad".

Los bucles, por otro lado, te permiten repetir un bloque de código varias veces. Dart ofrece varios tipos de bucles, incluyendo `for`, `while` y `do-while`. El bucle `for` es ideal cuando conoces el número de veces que quieres repetir un bloque de código. El bucle `while` continúa ejecutándose mientras una condición sea verdadera. El bucle `do-while` es similar al `while`, pero garantiza que el bloque de código se ejecute al menos una vez.

Similar a cómo en JavaScript puedes iterar sobre un array, en Dart puedes usar bucles para recorrer listas o colecciones de datos. Por ejemplo:

```dart
void main() {
  List<String> colores = ["rojo", "verde", "azul"];

  for (String color in colores) {
    print("El color es: $color");
  }
}
```

Este código itera sobre la lista de colores e imprime cada color en la consola. Esencialmente, esto es lo mismo que harías en JavaScript con un bucle `for...of`.

Entender estas estructuras de control te permitirá crear lógica compleja y dinámica dentro de tus aplicaciones Flutter.  En lugar de simplemente mostrar contenido estático como en HTML, podrás crear interfaces de usuario interactivas que reaccionen a las acciones del usuario y los datos que reciban.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos.

*   Sentencias `if/else` para controlar la visibilidad de un widget basado en el estado de la aplicación.
*   Bucles `for` para generar una lista de widgets dinámicamente.
*   Bucles `while` para realizar operaciones hasta que se cumpla una condición.

Aquí tienes algunos fragmentos de código Flutter cortos y claros que demuestran el uso correcto:

```dart
// Ejemplo 1: Usando if/else para mostrar un mensaje diferente según el usuario ha iniciado sesión o no.
bool isLoggedIn = true;

Widget buildLoginMessage() {
  if (isLoggedIn) {
    return Text("Bienvenido de nuevo!"); // Muestra este mensaje si el usuario ha iniciado sesión.
  } else {
    return Text("Por favor, inicia sesión."); // Muestra este mensaje si el usuario no ha iniciado sesión.
  }
}

// Ejemplo 2: Usando un bucle for para crear una lista de widgets Text.
List<Widget> buildListItems(int itemCount) {
  List<Widget> items = [];
  for (int i = 0; i < itemCount; i++) {
    items.add(Text("Elemento $i")); // Crea un widget Text para cada elemento.
  }
  return items;
}

// Ejemplo 3: Usando un bucle while para simular una carga de datos (un caso de uso común).
Future<void> simulateDataLoading() async {
  int progress = 0;
  while (progress < 100) {
    await Future.delayed(Duration(milliseconds: 100)); // Simula un retardo.
    progress += 10;
    print("Cargando... $progress%");
  }
  print("Carga completa!");
}
```

## Práctica: Preguntas y Respuestas

Ahora, pongamos a prueba tus conocimientos con algunas preguntas de práctica.

**Pregunta:** ¿Cómo se usa la sentencia `if` para ejecutar un bloque de código solo si una variable `edad` es mayor que 18?
**5... 4... 3... 2... 1...**
**Respuesta:** `if (edad > 18) { // Código a ejecutar }`

**Pregunta:** ¿Cuál es la diferencia principal entre un bucle `while` y un bucle `do-while`?
**5... 4... 3... 2... 1...**
**Respuesta:** El bucle `do-while` siempre ejecuta el bloque de código al menos una vez, mientras que el bucle `while` podría no ejecutarlo si la condición es falsa desde el principio.

**Pregunta:** ¿Cómo puedes usar un bucle `for` para iterar sobre una lista de strings en Dart?
**5... 4... 3... 2... 1...**
**Respuesta:** `for (String item in miLista) { // Código a ejecutar }`

**Pregunta:** En Flutter, ¿cómo utilizarías una condición `if/else` para mostrar un widget diferente basado en si la conexión a internet está activa o no?
**5... 4... 3... 2... 1...**
**Respuesta:** Podrías usar un `StreamBuilder` que detecte los cambios en la conectividad, y dentro de su constructor, renderizar un widget para conexión activa y otro para conexión inactiva con `if/else`.

**Pregunta:** Explica con tus palabras cómo se relaciona el concepto de `if/else` con las media queries en CSS, en términos de lógica condicional.
**5... 4... 3... 2... 1...**
**Respuesta:** Tanto `if/else` en Dart como las media queries en CSS permiten aplicar estilos o ejecutar código diferente dependiendo de si se cumplen ciertas condiciones. En CSS, es el tamaño de la pantalla, mientras que en Dart, pueden ser valores de variables o el resultado de expresiones.
