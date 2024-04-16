import attr

@attr.s
class ControlEvent:
    # define your attributes here
    attribute1 = attr.ib()
    attribute2 = attr.ib()


from attr import validate
import flet as ft
from flet import TextField,Checkbox,ElevatedButton,Text,Row,Column
from flet_core.control_event import ControlEvent

def main(page:ft.Page) -> None:
    page.title = 'Signup'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 400
    page.window_width = 400
    page.window_resizable = False

    #Setup filde
    Text_username : TextField = TextField(label="Keyword",text_align=ft.TextAlign.LEFT,width=200)
    button_submit :ElevatedButton = ElevatedButton(text="Select",width=200,disabled=True)


    def submit(e:ControlEvent) ->None:
        print('Username:',Text_username.value)


        page.clean()
        page.add(
            Row(
                controls=[Text(value=f'Welcome:{Text_username.value}',size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    Text_username.on_change = validate
    button_submit.on_click = submit


    page.add(
        Row(
            controls=[
                Column(
                    [Text_username,
                     button_submit]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

if __name__=='__main__':
    ft.app(target=main)
