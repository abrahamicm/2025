# 2.9. Rutas con nombre (Named Routes)

## Introducción

Para un desarrollador web que está aprendiendo Flutter, entender las rutas con nombre es crucial para construir aplicaciones con múltiples pantallas, de forma similar a cómo se manejan las URLs en la web. Imagina que cada pantalla de tu aplicación Flutter es como una página web separada, y las rutas con nombre son como las URLs que permiten navegar entre ellas. En lugar de modificar el DOM directamente como en JavaScript, en Flutter utilizaremos las rutas para controlar la navegación y la presentación de contenido en la pantalla.

## Explicación

Las rutas con nombre en Flutter son una forma de definir y manejar la navegación entre diferentes pantallas o widgets de tu aplicación utilizando identificadores únicos. En lugar de depender de la construcción manual de `MaterialPageRoute` cada vez que deseas cambiar de pantalla, defines un mapa de rutas con nombres y, luego, utilizas esos nombres para navegar.

Esto tiene varias ventajas, incluyendo una mejor organización del código, la capacidad de pasar argumentos entre pantallas de forma más sencilla y la centralización de la lógica de navegación. Piensa en ello como la gestión de enlaces con `<a>` en HTML pero de forma programática y con mayor control.

En Flutter, definimos las rutas con nombre dentro de la propiedad `routes` de nuestro `MaterialApp`. Cada entrada en este mapa asocia un nombre de ruta (un `String`) a un `WidgetBuilder`, que es una función que construye el widget que se mostrará cuando se navegue a esa ruta.

Por ejemplo, puedes tener una ruta llamada `/home` que muestra la pantalla principal de la aplicación, y otra ruta llamada `/details` que muestra los detalles de un elemento seleccionado. Para navegar de la pantalla principal a la pantalla de detalles, simplemente utilizas el nombre de la ruta `/details`.

La función `Navigator.pushNamed(context, '/details')` es la clave aquí. Similar a `window.location.href` en JavaScript,  `pushNamed` nos permite dirigirnos a una ruta específica dentro de nuestra aplicación. La diferencia fundamental es que en Flutter controlamos *cómo* se realiza la transición entre las pantallas, pudiendo añadir animaciones o lógica personalizada.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos para entender mejor cómo funcionan las rutas con nombre en Flutter.

Aquí tienes algunos códigos clave relacionados con este tema:

*   `MaterialApp`:  El widget que define la estructura base de la aplicación y donde se configuran las rutas.
*   `Navigator.pushNamed(BuildContext context, String routeName)`:  Función para navegar a una ruta con nombre.
*   `Navigator.pop(BuildContext context)`: Función para volver a la ruta anterior. Similar al botón "Atrás" del navegador.
*   `routes`:  Propiedad del `MaterialApp` que define el mapa de rutas con nombre.
*   `WidgetBuilder`: Una función que construye el widget que se mostrará para una ruta específica.

Aquí tienes algunos fragmentos de código:

```dart
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Rutas con Nombre',
      initialRoute: '/', // La ruta inicial de la app
      routes: {
        '/': (context) => HomeScreen(), // La pantalla principal
        '/details': (context) => DetailsScreen(), // La pantalla de detalles
      },
    );
  }
}
```

*Este código define la estructura básica de la aplicación, estableciendo la ruta inicial y las rutas con nombre.*

```dart
class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Pantalla Principal'),
      ),
      body: Center(
        child: ElevatedButton(
          child: Text('Ir a Detalles'),
          onPressed: () {
            // Navega a la ruta '/details'
            Navigator.pushNamed(context, '/details');
          },
        ),
      ),
    );
  }
}
```

*Este ejemplo muestra cómo navegar a otra ruta cuando se presiona un botón.*

```dart
class DetailsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Pantalla de Detalles'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text('Aquí están los detalles'),
            ElevatedButton(
              onPressed: () {
                // Regresa a la pantalla anterior
                Navigator.pop(context);
              },
              child: Text('Volver'),
            ),
          ],
        ),
      ),
    );
  }
}
```

*Este código muestra la pantalla de detalles y cómo regresar a la pantalla anterior utilizando `Navigator.pop`.*

```dart
// Pasar argumentos a una ruta con nombre:
Navigator.pushNamed(context, '/details', arguments: 'Datos importantes');
// En DetailsScreen recibir los argumentos:
final args = ModalRoute.of(context)!.settings.arguments as String;
```

*Este ejemplo muestra como pasar argumentos (en este caso un string) a la ruta de detalles y como recuperarlos en la pantalla de detalles.*

## Práctica: Preguntas y Respuestas

Aquí hay algunas preguntas para poner a prueba tu comprensión.

**Pregunta:** ¿Dónde se definen las rutas con nombre en una aplicación Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** Se definen en la propiedad `routes` del widget `MaterialApp`.

**Pregunta:** ¿Qué función se utiliza para navegar a una ruta con nombre específica?
**5... 4... 3... 2... 1...**
**Respuesta:** Se utiliza la función `Navigator.pushNamed()`.

**Pregunta:** ¿Cómo se puede regresar a la pantalla anterior en Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** Se puede regresar utilizando la función `Navigator.pop()`.

**Pregunta:** ¿Cuál es la diferencia clave entre usar rutas con nombre y crear `MaterialPageRoute` directamente?
**5... 4... 3... 2... 1...**
**Respuesta:** Las rutas con nombre ofrecen una mejor organización del código, centralización de la lógica de navegación y facilitan el paso de argumentos entre pantallas. Además, te permiten cambiar rutas en un solo lugar, simplificando el mantenimiento.
