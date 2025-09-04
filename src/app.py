
import flet as ft
from bot import *
import asyncio

async def main(page: ft.Page):
    page.window.width = 640
    page.window.height = 720
    page.window.resizable = False
    page.window.icon = "icon.ico"
    page.window.center()
    page.title = "alaqubot"
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "jersey":"fonts/Jersey20-Regular.ttf",
        "notosans":"fonts/NotoSans-Regular.ttf",
        "plex medium":"fonts/IBMPlexSans-Medium.ttf",
        "plex bold":"fonts/IBMPlexSans-Bold.ttf"
    }
    
    bot_status = False
    bot = Bot()
    
    def on_chat(msg):
        chat.controls.append(
            ft.Text(f"[CHAT] {msg.user.name}: {msg.text}", font_family="plex medium", color=ft.Colors.GREEN_400)
        )
        page.update()
    
    async def on_ready():
        status_icon.name = ft.Icons.RADIO_BUTTON_ON
        status_icon.color = ft.Colors.GREEN_700
        
        start_button.disabled = False
        
        asyncio.create_task(get_stream())
        
        page.update()

    async def get_stream():
        nonlocal bot_status
        while bot_status:
            info = await bot.get_stream()
            if type(info) == dict:
                stream_status.value = f"Статус: {info["status"]}"
                stream_viewers.value = f"Зрители: {info["viewer_count"]}"
                stream_title.value = f"Заголовок: {info["title"]}"
                stream_game.value = f"Категория: {info["game_name"]}"
                
                first_divider.visible = True
                second_divider.visible = True
                
                bot_message_field.visible = True
                bot_message_button.visible = True
            else:
                stream_status.value = ""
                stream_viewers.value = ""
                stream_title.value = ""
                stream_game.value = ""
                
                first_divider.visible = False
                second_divider.visible = False
                
                bot_message_field.visible = False
                bot_message_button.visible = False
            page.update()
            await asyncio.sleep(60)
            
        
    bot.add_message_callback(on_chat)
    bot.add_ready_callback(on_ready)
    
    async def start(e):
        nonlocal bot_status
        if bot_status == True:
            start_button.text = "Запустить бота"
            status_icon.name = ft.Icons.RADIO_BUTTON_OFF
            status_icon.color = ft.Colors.RED_700
            bot_status = False
            await bot.stop()
        else:
            start_button.text = "Остановить бота"
            start_button.disabled = True
            bot_status = True
            asyncio.create_task(bot.run())
            
        page.update()
        
    async def bot_message(e):
        await bot.send_message(str(bot_message_field.value))
        bot_message_field.value = None
        page.update()
    
    start_button = ft.ElevatedButton("Запустить бота", on_click=start, disabled=False)
    status_icon = ft.Icon(ft.Icons.RADIO_BUTTON_OFF, color=ft.Colors.RED_700)
    
    stream_status = ft.Text(font_family="notosans", size=16,text_align=ft.TextAlign.START)
    stream_viewers = ft.Text(font_family="notosans", size=16, text_align=ft.TextAlign.START)
    stream_title = ft.Text(font_family="notosans", size=16, text_align=ft.TextAlign.START)
    stream_game = ft.Text(font_family="notosans", size=16, text_align=ft.TextAlign.START)
    
    bot_message_field = ft.TextField(label="Message", visible=False, width=120)
    bot_message_button = ft.ElevatedButton("Отправить", on_click=bot_message, visible=False, width=120)
    
    chat = ft.Column(
        controls=[],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    first_divider = ft.Divider(thickness=1, visible=False)
    second_divider = ft.Divider(thickness=1, visible=False)
    
    page.add(
        ft.Row(
            [
                ft.Column(
                    controls=[
                        ft.Text("alaqubot", font_family="jersey", size=50, text_align=ft.TextAlign.CENTER),
                        ft.Divider(thickness=1),
                        ft.Text("ЕГОРЫЧ 7К МУСОР НЕ ИГРОК ДАЖЕ!", font_family="plex medium"),
                        first_divider,
                        stream_status,
                        stream_viewers,
                        second_divider,
                        stream_title,
                        stream_game
                    ],
                    width=200
                ),
                ft.VerticalDivider(thickness=1),
                chat,
                ft.Column(
                    controls=[
                        ft.Column(
                            controls=[
                                bot_message_field,
                                bot_message_button
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            expand=True
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    [
                                        ft.Text("Статус: ", font_family="plex bold"),
                                        status_icon,
                                    ],
                                    alignment=ft.MainAxisAlignment.END
                                ),
                                start_button,
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            expand=True
                        )
                        ],
                    #alignment=ft.MainAxisAlignment.END,
                    #horizontal_alignment=ft.CrossAxisAlignment.END,
                    expand=True
                ),
            ],
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.app(main, assets_dir="assets")