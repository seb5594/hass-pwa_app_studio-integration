# Instalar, emparejar y actualizar una aplicación web

## Enviar un panel a alguien que conoces

Ejemplo. Sebastián crea una aplicación web que muestra las salidas de trenes. Su tío ya utiliza la aplicación complementaria oficial Home Assistant y tiene acceso al panel. Sebastian envía el enlace del navegador vía WhatsApp.

1. En PWA Web-App Studio, abra la aplicación, vaya a Acceso, habilite el inicio de sesión a través de la aplicación complementaria y guarde. Ambas aplicaciones deben llegar al mismo servidor Home Assistant a través de HTTPS.

2. Su invitado abre el enlace WhatsApp en su navegador y elige Iniciar sesión a través de la aplicación complementaria. La aplicación web muestra un código de dispositivo. El huésped puede copiarlo si es necesario.

3. Toque Abrir Home Assistant. Confirma que la aplicación, la cuenta y el código coincidan. Si la página de emparejamiento solicita un código, pegue o ingrese el código que se muestra en la aplicación web. Luego apruebe el inicio de sesión.

4. Vuelve a la pestaña original del navegador. Inicia sesión automáticamente. Si es necesario, toca Verificar aprobación. El código es válido por cinco minutos y para un inicio de sesión.

5. En iPhone o iPad, para iniciar sesión en la copia instalada, primero agregue la página a la pantalla de inicio en Safari. Abra el ícono de la pantalla de inicio e inicie el mismo proceso de aprobación allí.

## Encuentra el estudio

Utilice el equipo de integración, luego abra Studio a través del cuadro de diálogo Home Assistant. Si trabaja con aplicaciones con frecuencia, habilite la entidad de cambio del Panel de la barra lateral en la configuración de integración y actívela para mantener el acceso directo visible.

Para un panel de mantenimiento, agregue una tarjeta de botón que navegue hasta /pwa-app-studio. La entidad del botón opcional Abrir PWA Designer también puede abrirlo en su sesión de administrador activa. Habilite esa entidad primero; Home Assistant lo desactiva de forma predeterminada.

## Diseñar y actualizar un panel de invitados

Por ejemplo, cree un tablero para los visitantes con una tarjeta de información de Wi-Fi y una luz de patio. En Contenido, elija tarjetas individuales y seleccione un ajuste preestablecido o importe una tarjeta existente. Configure el título, entidad o Markdown usando el editor visual y verifique la vista previa del teléfono.

En el paso de la aplicación, configure la versión de la aplicación en 1.1 y guárdela. Un invitado que todavía tiene la aplicación abierta ve un banner de actualización cuando la aplicación detecta la nueva revisión. Al tocar Actualizar aplicación, se recarga la vista y se mantienen el ícono de la pantalla de inicio y la sesión del navegador. Una aplicación abierta más tarde carga la versión actual cuando se conecta.

## Compartir desde Android

Usar enlace compartido en Studio. El cuadro de diálogo nativo se abre cuando la aplicación o el navegador lo proporciona. Si la aplicación complementaria no ofrece API para compartir, abra la página para compartir en el navegador. También puedes copiar el enlace.

[English README](../README.md) · [Deutsch](../README.de.md)
