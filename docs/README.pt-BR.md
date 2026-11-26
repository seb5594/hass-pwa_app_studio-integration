# Instalar, emparelhar e atualizar um aplicativo da web

## Envie um painel para alguém que você conhece

Exemplo. Sebastian cria um aplicativo web que mostra as partidas dos trens. Seu tio já usa o aplicativo oficial Home Assistant Companion e tem acesso ao painel. Sebastian envia o link do navegador via WhatsApp.

1. Em PWA Web-App Studio, abra o aplicativo, vá para Access, ative o login por meio do aplicativo Companion e salve. Ambos os aplicativos devem acessar o mesmo servidor Home Assistant por HTTPS.

2. Seu convidado abre o link WhatsApp em seu navegador e escolhe Fazer login por meio do aplicativo complementar. O aplicativo da web exibe um código de dispositivo. O hóspede pode copiá-lo, se necessário.

3. Toque em Abrir Home Assistant. Confirme se o aplicativo, a conta e o código correspondem. Se a página de emparelhamento solicitar um código, cole ou insira o código mostrado no aplicativo da web. Em seguida, aprove o login.

4. Volte para a guia original do navegador. Ele faz login automaticamente. Se necessário, toque em Verificar aprovação. O código é válido por cinco minutos e para um login.

5. No iPhone ou iPad, para fazer login na cópia instalada, primeiro adicione a página à tela inicial do Safari. Abra o ícone da tela inicial e inicie o mesmo processo de aprovação lá.

## Encontre o estúdio

Use o equipamento de integração e abra o Studio através da caixa de diálogo Home Assistant. Se você trabalha com aplicativos com frequência, ative a entidade de alternância do painel da barra lateral nas configurações de integração e ative-a para manter o atalho visível.

Para um painel de manutenção, adicione um cartão de botão que navega para /pwa-app-studio. A entidade opcional do botão Open PWA Designer também pode abri-lo em sua sessão de administrador ativa. Habilite essa entidade primeiro; Home Assistant o desativa por padrão.

## Projetar e atualizar um painel de convidados

Por exemplo, crie um painel para visitantes com um cartão de informações de Wi-Fi e uma luz de pátio. Em Conteúdo, escolha cartões individuais e selecione uma predefinição ou importe um cartão existente. Defina o título, entidade ou Markdown usando o editor visual e verifique a visualização do telefone.

Na etapa App, defina a versão do App como 1.1 e salve. Um convidado que ainda esteja com o aplicativo aberto verá um banner de atualização quando o aplicativo detectar a nova revisão. Tocar em Atualizar aplicativo recarrega a visualização e mantém o ícone da tela inicial e a sessão do navegador. Um aplicativo aberto posteriormente carrega a versão atual quando conectado.

## Compartilhar do Android

Use o compartilhamento de link no Studio. A caixa de diálogo nativa é aberta quando o aplicativo ou navegador a fornece. Se o aplicativo complementar não oferecer API de compartilhamento, abra a página de compartilhamento no navegador. Você também pode copiar o link.

[English README](../README.md) · [Deutsch](../README.de.md)
