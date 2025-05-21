# 1.3. Conceptos básicos de Dart: Variables, tipos de datos y operadores (1.3)

## Introducción

Para los desarrolladores web con experiencia en HTML, CSS y JavaScript que buscan aprender Flutter, comprender los conceptos básicos de Dart es fundamental. Dart es el lenguaje de programación utilizado para crear aplicaciones Flutter.  Si bien JavaScript puede parecer similar al principio, existen diferencias importantes que debemos abordar. Por ejemplo, Dart es un lenguaje fuertemente tipado, a diferencia de JavaScript que es de tipado dinámico. En esta lección, exploraremos las variables, los tipos de datos y los operadores en Dart, estableciendo una base sólida para el desarrollo de Flutter.  Piense en esto como la estructura básica (HTML), el estilo (CSS) y la interactividad (JavaScript) de Flutter, pero ahora todo en un único lenguaje: Dart.

## Explicación

En esta sección, exploraremos las variables, los tipos de datos y los operadores, pilares fundamentales en Dart.

Comencemos con las **variables**.  Una variable es un contenedor para almacenar información.  En Dart, necesitas declarar el tipo de dato que almacenará la variable, aunque puedes usar `var` o `dynamic` para dejar que Dart infiera el tipo.  Esto es diferente de JavaScript, donde puedes declarar variables con `var`, `let` o `const` sin especificar un tipo explícito.

Aquí tienes un ejemplo:

```dart
// Declarando una variable de tipo String
String nombre = "Juan";

// Declarando una variable de tipo int
int edad = 30;

// Declarando una variable booleana
bool esMayorDeEdad = true;

// Usando 'var' para que Dart infiera el tipo (en este caso, String)
var ciudad = "Madrid";

// Usando 'dynamic' para permitir cambiar el tipo de dato de la variable
dynamic valorDinamico = "Un texto";
valorDinamico = 123; // Ahora es un entero
```

Ahora hablemos de los **tipos de datos**.  Dart ofrece una variedad de tipos de datos, incluyendo:

*   `int`: Para números enteros, como 1, 2, 3, -1, etc.
*   `double`: Para números de punto flotante (decimales), como 3.14, 2.71, etc.
*   `String`: Para cadenas de texto, como "Hola mundo".
*   `bool`: Para valores booleanos, que pueden ser `true` (verdadero) o `false` (falso).
*   `List`: Para colecciones ordenadas de elementos.  Piensa en esto como un array en JavaScript.
*   `Map`: Para colecciones de pares clave-valor.  Similar a los objetos en JavaScript.

Finalmente, los **operadores** en Dart son similares a los que se encuentran en JavaScript.  Incluyen:

*   Operadores aritméticos: `+` (suma), `-` (resta), `*` (multiplicación), `/` (división), `%` (módulo).
*   Operadores de asignación: `=` (asignación), `+=` (suma y asignación), `-=` (resta y asignación), etc.
*   Operadores de comparación: `==` (igual a), `!=` (no igual a), `>` (mayor que), `<` (menor que), `>=` (mayor o igual que), `<=` (menor o igual que).
*   Operadores lógicos: `&&` (AND lógico), `||` (OR lógico), `!` (NOT lógico).

## Ejemplos

Ahora, veamos algunos ejemplos prácticos.

- Tipos de Datos Primitivos: `String`, `int`, `double`, `bool`.
- Colecciones: `List`, `Map`.
- Operadores aritméticos: `+`, `-`, `*`, `/`, `%`.
- Operadores lógicos: `&&`, `||`, `!`.

Aquí tienes algunos fragmentos de código:

```dart
// Ejemplo de operaciones aritméticas
int a = 10;
int b = 5;
int suma = a + b; // suma = 15
int resta = a - b; // resta = 5
int multiplicacion = a * b; // multiplicacion = 50
double division = a / b; // division = 2.0  (importante usar double si el resultado no es entero)
int modulo = a % b; // modulo = 0
```

```dart
// Ejemplo de operadores de comparación
int edad = 25;
bool esMayor = edad > 18; // esMayor = true
bool esIgual = edad == 25; // esIgual = true
```

```dart
// Ejemplo de lista
List<String> frutas = ["manzana", "banana", "naranja"]; // Similar a un array en JavaScript
print(frutas[0]); // Imprime "manzana" (el índice empieza en 0)
```

```dart
// Ejemplo de mapa (diccionario)
Map<String, dynamic> persona = {
  "nombre": "Ana",
  "edad": 28,
  "esCasada": false,
};  // Similar a un objeto en JavaScript
print(persona["nombre"]); // Imprime "Ana"
```

```dart
// Ejemplo de concatenación de strings
String saludo = "Hola";
String nombreUsuario = "Carlos";
String mensajeCompleto = saludo + ", " + nombreUsuario + "!"; // Similar a JavaScript
print(mensajeCompleto); // Imprime "Hola, Carlos!"
```

## Práctica: Preguntas y Respuestas

Ahora, pongamos a prueba tus conocimientos con algunas preguntas.

**Pregunta:** ¿Cuál es la principal diferencia entre declarar una variable con `var` y con `String` o `int` en Dart?
**5... 4... 3... 2... 1...**
**Respuesta:**  Al usar `String` o `int`, especificas explícitamente el tipo de dato. Con `var`, Dart infiere el tipo basado en el valor inicial.

**Pregunta:** ¿Qué tipo de dato usarías para representar el precio de un producto?
**5... 4... 3... 2... 1...**
**Respuesta:** `double`, ya que los precios suelen tener decimales.

**Pregunta:** ¿Cómo se declara una lista de números enteros en Dart?
**5... 4... 3... 2... 1...**
**Respuesta:** `List<int> numeros = [1, 2, 3];`

**Pregunta:** ¿Cuál es la diferencia entre `==` y `!=` en Dart?
**5... 4... 3... 2... 1...**
**Respuesta:** `==` compara si dos valores son iguales, mientras que `!=` compara si dos valores son diferentes.

**Pregunta:** ¿Cómo se accede al valor asociado a la clave "nombre" en un mapa llamado `datos`?
**5... 4... 3... 2... 1...**
**Respuesta:**  `datos["nombre"]`.  De manera similar a cómo accedes a las propiedades de un objeto en JavaScript.
