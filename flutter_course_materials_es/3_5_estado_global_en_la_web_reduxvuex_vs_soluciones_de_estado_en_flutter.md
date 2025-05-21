# 3.5. Estado global en la web (Redux, Vuex) vs soluciones de estado en Flutter (3.5)

## Introducción

Este tema es crucial para desarrolladores web que se adentran en Flutter, ya que aborda la gestión del estado de la aplicación, un aspecto fundamental en la creación de aplicaciones complejas. En el desarrollo web, frameworks como Redux o Vuex manejan el estado global.  Aquí compararemos estas soluciones con las opciones disponibles en Flutter,  analizando sus similitudes y diferencias. Piensa en el estado global como el "contexto" compartido por todos los componentes de tu aplicación web; en Flutter, también necesitarás una forma de compartir información entre diferentes widgets, sin tener que pasarla manualmente de un widget padre a uno hijo.

## Explicación

En el desarrollo web, a menudo nos encontramos con la necesidad de compartir datos entre diferentes componentes que no están directamente relacionados.  En HTML, podríamos pensar en el DOM como un estado, pero manejarlo directamente con JavaScript puede ser engorroso, especialmente con interacciones complejas. CSS, a través de clases y selectores,  también influye en el estado visual de los elementos.  Cuando construimos aplicaciones web más complejas, frameworks como React, Vue o Angular nos ofrecen formas más estructuradas de gestionar el estado. Redux y Vuex son ejemplos de patrones de gestión de estado que centralizan la información y facilitan su acceso y modificación desde cualquier parte de la aplicación.

Flutter, al igual que los frameworks web, ofrece varias formas de gestionar el estado.  La principal diferencia radica en la naturaleza del framework: Flutter se basa en el concepto de Widgets, que son inmutables. Esto significa que para cambiar la apariencia de un widget, se debe reconstruir.  Para gestionar el estado de manera eficiente, Flutter proporciona mecanismos como `setState`, `Provider`, `Riverpod`, `Bloc` y `GetX`.  `setState` es la forma más sencilla y se usa para actualizaciones locales dentro de un widget.  Para el estado global,  `Provider` y `Riverpod` son alternativas populares que facilitan la inyección de dependencias y la reconstrucción de widgets cuando el estado cambia.  Bloc es otro patrón, generalmente más complejo, que se usa para gestionar el estado de forma reactiva, ideal para aplicaciones más grandes y complejas. GetX es un framework completo que también incluye gestión de estado, navegación y dependencias.

La idea principal es la misma que en la web: tener un lugar centralizado para la información importante, y una forma eficiente de notificar a los componentes (widgets) cuando esa información cambia. En lugar de manipular el DOM directamente, como en JavaScript vanilla, en Flutter, modificamos el estado, lo que a su vez provoca la reconstrucción de la interfaz de usuario.

## Ejemplos

Ahora, veamos algunos ejemplos prácticos.

*   `setState`:  Para actualizaciones locales del widget.
*   `Provider`: Para compartir estado en la jerarquía de widgets.
*   `Riverpod`: Una alternativa a Provider con más seguridad de tipos.
*   `Bloc`: Gestión de estado reactiva para aplicaciones complejas.
*   `GetX`: Un framework completo con gestión de estado, rutas y dependencias.

Aquí tienes algunos fragmentos de código Flutter.

```dart
// Usando setState para un cambio de estado local
class MiWidget extends StatefulWidget {
  @override
  _MiWidgetState createState() => _MiWidgetState();
}

class _MiWidgetState extends State<MiWidget> {
  int _contador = 0;

  void _incrementarContador() {
    setState(() { // Esta función notifica a Flutter para reconstruir el widget.
      _contador++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Ejemplo setState')),
      body: Center(child: Text('Contador: $_contador')),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementarContador,
        child: Icon(Icons.add),
      ),
    );
  }
}
```

```dart
// Usando Provider para compartir datos
import 'package:provider/provider.dart';
import 'package:flutter/material.dart';

// Modelo de datos simple
class ContadorModel extends ChangeNotifier {
  int contador = 0;

  void incrementar() {
    contador++;
    notifyListeners(); // Notifica a los widgets que están escuchando.
  }
}

class ProviderEjemplo extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => ContadorModel(),
      child: Scaffold(
        appBar: AppBar(title: Text('Ejemplo Provider')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text('Contador:'),
              Consumer<ContadorModel>( // Consumer reconstruye solo esta parte del widget.
                builder: (context, contadorModel, child) {
                  return Text(
                    '${contadorModel.contador}',
                    style: Theme.of(context).textTheme.headline4,
                  );
                },
              ),
            ],
          ),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () => Provider.of<ContadorModel>(context, listen: false).incrementar(), // Obtiene el modelo y llama al método.
          child: Icon(Icons.add),
        ),
      ),
    );
  }
}
```

```dart
// Un ejemplo simple de como usar GetX para la gestión de estado:
import 'package:get/get.dart';

class ContadorController extends GetxController {
  var contador = 0.obs; // .obs lo hace observable para GetX

  void incrementar() {
    contador++;
  }
}

class GetXEjemplo extends StatelessWidget {
  final ContadorController controller = Get.put(ContadorController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("GetX Ejemplo"),
      ),
      body: Center(
        child: Obx(() => Text("Contador: ${controller.contador}")), // Obx se reconstruye cuando cambia el valor.
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          controller.incrementar();
        },
        child: Icon(Icons.add),
      ),
    );
  }
}

```

## Práctica: Preguntas y Respuestas

Aquí tienes algunas preguntas para poner a prueba tus conocimientos.

**Pregunta:** ¿Cuál es la principal diferencia entre `setState` y `Provider` en Flutter?
**5... 4... 3... 2... 1...**
**Respuesta:** `setState` se usa para gestionar el estado local dentro de un solo widget, mientras que `Provider` permite compartir el estado entre múltiples widgets en la jerarquía.

**Pregunta:** ¿Qué rol cumple el método `notifyListeners()` en la gestión de estado con `Provider`?
**5... 4... 3... 2... 1...**
**Respuesta:** `notifyListeners()` notifica a todos los widgets que están "escuchando" a un `ChangeNotifier` que el estado ha cambiado, lo que provoca la reconstrucción de esos widgets.

**Pregunta:** ¿Cuál es un framework completo de Flutter que incluye gestión de estado, rutas y dependencias?
**5... 4... 3... 2... 1...**
**Respuesta:** GetX.

**Pregunta:** En Flutter, ¿Por qué es importante usar una solución de gestión de estado, en lugar de simplemente pasar datos manualmente entre Widgets?
**5... 4... 3... 2... 1...**
**Respuesta:** La gestión del estado centralizada mejora la organización del código, facilita el seguimiento de los cambios de datos, y optimiza la reconstrucción de la interfaz de usuario, evitando actualizaciones innecesarias y mejorando el rendimiento. Además, facilita el mantenimiento y la escalabilidad de la aplicación.
