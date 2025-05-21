# 1.5. Conceptos básicos de Dart: Funciones y clases (1.5)

## Introducción

Para un desarrollador web con experiencia en HTML, CSS y JavaScript, entender las funciones y clases en Dart es fundamental para construir aplicaciones Flutter. Piensa en las funciones como las funciones de JavaScript, pero con una sintaxis ligeramente diferente, y en las clases como prototipos de objetos, similares a la forma en que trabajas con objetos en JavaScript, pero con características propias del lenguaje Dart. En HTML, usas elementos para la estructura; en CSS, aplicas estilos; en Flutter, usas widgets creados con clases Dart.  Dominar estos conceptos te permitirá crear widgets personalizados y reutilizables, lo que es esencial en Flutter.

## Explicación

En esta sección, exploraremos las funciones y las clases en Dart, dos conceptos cruciales para entender cómo funciona Flutter.

Las **funciones** en Dart son bloques de código reutilizables que realizan una tarea específica. Al igual que en JavaScript, puedes definir funciones que reciben parámetros y devuelven valores. La sintaxis es un poco diferente: en Dart, especificas el tipo de dato que devuelve la función (o `void` si no devuelve nada).

Aquí tienes un ejemplo simple:

```dart
int sumar(int a, int b) {
  return a + b;
}

void saludar(String nombre) {
  print('Hola, $nombre!');
}
```

En este código, `sumar` es una función que toma dos enteros como entrada y devuelve la suma de ellos. `saludar` es una función que toma una cadena como entrada e imprime un saludo en la consola.  Observa que el uso de `$` para la interpolación de cadenas es similar a JavaScript con las template literals (``).

Las **clases** en Dart son plantillas para crear objetos.  Piensa en ellas como blueprints para construir "cosas".  Cada objeto creado a partir de una clase tiene propiedades (variables) y métodos (funciones) asociados.  Esto es muy similar a la programación orientada a objetos en JavaScript, aunque Dart utiliza una sintaxis más formal.

Aquí tienes un ejemplo sencillo de una clase:

```dart
class Persona {
  String nombre;
  int edad;

  Persona(this.nombre, this.edad);

  void presentarse() {
    print('Hola, mi nombre es $nombre y tengo $edad años.');
  }
}
```

En este ejemplo, `Persona` es una clase con dos propiedades: `nombre` (una cadena) y `edad` (un entero). El constructor `Persona(this.nombre, this.edad)` inicializa estas propiedades cuando se crea un nuevo objeto `Persona`.  El método `presentarse` imprime un mensaje que utiliza las propiedades del objeto.

Para crear un objeto de esta clase, harías lo siguiente:

```dart
void main() {
  Persona persona1 = Persona('Juan', 30);
  persona1.presentarse(); // Imprime: Hola, mi nombre es Juan y tengo 30 años.
}
```

En Flutter, casi todo es un widget, y los widgets son clases Dart. Comprender cómo funcionan las clases te permitirá crear tus propios widgets personalizados y manipular los widgets existentes. Piensa en los componentes de un framework de JavaScript como React o Vue; los widgets de Flutter cumplen una función similar, pero se construyen usando clases Dart.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos para solidificar tu comprensión.

Aquí tienes algunos códigos y conceptos clave relacionados con funciones y clases en Flutter:

*   Definición de funciones con tipos de retorno.
*   Creación de clases con constructores.
*   Uso de métodos dentro de clases.
*   Instanciación de clases para crear objetos.
*   Herencia de clases para reutilizar código.

Aquí tienes algunos fragmentos de código Dart que demuestran el uso correcto:

```dart
// Función que calcula el área de un círculo.
double calcularAreaCirculo(double radio) {
  // Retorna el área del círculo.
  return 3.1416 * radio * radio;
}
```

```dart
// Definición de una clase Rectangulo.
class Rectangulo {
  double ancho;
  double alto;

  // Constructor de la clase.
  Rectangulo(this.ancho, this.alto);

  // Método para calcular el área del rectángulo.
  double calcularArea() {
    return ancho * alto;
  }
}
```

```dart
// Creación de una instancia de la clase Rectangulo.
void main() {
  Rectangulo miRectangulo = Rectangulo(5.0, 10.0); // Crea un objeto Rectangulo con ancho 5 y alto 10.
  double area = miRectangulo.calcularArea(); // Llama al método calcularArea del objeto.
  print('El área del rectángulo es: $area'); // Imprime el área del rectángulo.
}
```

```dart
// Herencia: Clase Cuadrado que hereda de Rectangulo.
class Cuadrado extends Rectangulo {
  Cuadrado(double lado) : super(lado, lado); // Llama al constructor de la clase padre (Rectangulo).
}
```

```dart
void main() {
  Cuadrado miCuadrado = Cuadrado(5.0);
  double area = miCuadrado.calcularArea();
  print('El área del cuadrado es: $area');
}
```

## Práctica: Preguntas y Respuestas

Aquí tienes algunas preguntas de práctica para poner a prueba tu comprensión:

**Pregunta:** ¿Cuál es la palabra clave para definir una función en Dart?
**5... 4... 3... 2... 1...**
**Respuesta:** No hay una palabra clave específica como en JavaScript ("function").  Simplemente se define el tipo de retorno (o `void`), el nombre de la función, y los parámetros.

**Pregunta:** ¿Cómo se crea una instancia de una clase en Dart?
**5... 4... 3... 2... 1...**
**Respuesta:** Se utiliza la palabra clave `new` (opcional, pero común) seguida del nombre de la clase y paréntesis, pasando los argumentos necesarios al constructor: `new MiClase(argumento1, argumento2);` o simplemente `MiClase(argumento1, argumento2);`.

**Pregunta:** ¿Cómo se hereda de una clase padre en Dart?
**5... 4... 3... 2... 1...**
**Respuesta:** Se utiliza la palabra clave `extends` seguida del nombre de la clase padre: `class MiClaseHija extends MiClasePadre { ... }`.

**Pregunta:** ¿Cuál es la función que se ejecuta automáticamente al crear un objeto de una clase?
**5... 4... 3... 2... 1...**
**Respuesta:** El constructor.

**Pregunta:** ¿Cómo se declara una variable dentro de una clase en Dart?
**5... 4... 3... 2... 1...**
**Respuesta:**  Se declara simplemente indicando el tipo y el nombre de la variable dentro del cuerpo de la clase, por ejemplo `String nombre;` o `int edad;`.
