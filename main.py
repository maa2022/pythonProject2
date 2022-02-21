#импорт модулей
from tkinter import *
import time
import random

#создаем переменную со значением истина
Game_Running = True

#размеры игровой области
game_width = 400
game_height = 400
#размер 1 ячейки
snake_item = 20

#цвет змейки
snake_color1 = "black"
snake_color2 = "yellow"

#создаем переменные для виртуальных координат
virtual_game_x = game_width // snake_item
virtual_game_y = game_height // snake_item

#первый элемент змейки по координатам
snake_x = random.randrange(virtual_game_x )
snake_y = random.randrange(virtual_game_y )
#направление движения змейки
snake_x_nav = 0
snake_y_nav = 0

#список для координат элементов змейки
snake_list = []
#размер змейки
snake_size = 5

#создание окна
tk = Tk()
tk.title("Snake")
tk.resizable(0, 0)

#атрибут - окно поверх остальных
tk.wm_attributes("-topmost", 1)

#создание объекта(игровое поле)
canvas = Canvas(tk, width=game_width, height=game_height, bd=0, highlightthickness=0)
canvas.pack()
tk.update()


#цвет еды
present_color1 = "red"
present_color2 = "black"
#список для хранения "еды"
presents_list = []
#количество
presents_size = 5
#заполняем список координатами
for i in range(presents_size):
    x = random.randrange(virtual_game_x)
    y = random.randrange(virtual_game_y)
    id1 = canvas.create_oval(x * snake_item, y * snake_item, x * snake_item + snake_item, y * snake_item + snake_item,
                             fill=present_color2)
    id2 = canvas.create_oval(x * snake_item + 2, y * snake_item + 2, x * snake_item + snake_item - 2,
                             y * snake_item + snake_item - 2, fill=present_color1)
    presents_list.append([x, y, id1, id2])
print(presents_list)


#функция отрисовывания змейки
def snake_paint_item(canvas, x, y):
    global snake_list
    id1 = canvas.create_rectangle(x * snake_item, y * snake_item, x * snake_item + snake_item,
                                  y * snake_item + snake_item, fill=snake_color2)
    id2 = canvas.create_rectangle(x * snake_item + 2, y * snake_item + 2, x * snake_item + snake_item - 2,
                                  y * snake_item + snake_item - 2, fill=snake_color1)
    snake_list.append([x, y, id1, id2])
    # print(snake_list)

snake_paint_item(canvas, snake_x, snake_y)


#проверяем, что не превышен размер змеи
def check_can_we_delete_snake_item():
    if len(snake_list) >= snake_size:
        temp_item = snake_list.pop(0)
        # print(temp_item)
        canvas.delete(temp_item[2])
        canvas.delete(temp_item[3])


#проверяем коррдинаты змеи на наличие в списке с едой
def check_if_we_found_present():
    global snake_size
    for i in range(len(presents_list)):
        if presents_list[i][0] == snake_x and presents_list[i][1] == snake_y:
            # print("found!!!")
            snake_size = snake_size + 1
            canvas.delete(presents_list[i][2])
            canvas.delete(presents_list[i][3])


#функция отвечает за принятие событый
def snake_move(event):
    global snake_x
    global snake_y
    global snake_x_nav
    global snake_y_nav

    if event.keysym == "Up":
        snake_x_nav = 0
        snake_y_nav = -1
        check_can_we_delete_snake_item()
    elif event.keysym == "Down":
        snake_x_nav = 0
        snake_y_nav = 1
        check_can_we_delete_snake_item()
    elif event.keysym == "Left":
        snake_x_nav = -1
        snake_y_nav = 0
        check_can_we_delete_snake_item()
    elif event.keysym == "Right":
        snake_x_nav = 1
        snake_y_nav = 0
        check_can_we_delete_snake_item()
    snake_x = snake_x + snake_x_nav
    snake_y = snake_y + snake_y_nav
    snake_paint_item(canvas, snake_x, snake_y)
    check_if_we_found_present()


#обработка событий
canvas.bind_all("<KeyPress-Left>", snake_move)
canvas.bind_all("<KeyPress-Right>", snake_move)
canvas.bind_all("<KeyPress-Up>", snake_move)
canvas.bind_all("<KeyPress-Down>", snake_move)


#функция прерывания игры
def game_over():
    global Game_Running
    Game_Running = False


#проверка выхода за пределы экрана
def check_if_borders():
    if snake_x > virtual_game_x or snake_x < 0 or snake_y > virtual_game_y or snake_y < 0:
        game_over()


#проверка касанияли змейки самой себя
def check_we_touch_self(f_x, f_y):
    global Game_Running
    if not (snake_x_nav == 0 and snake_y_nav == 0):
        for i in range(len(snake_list)):
            if snake_list[i][0] == f_x and snake_list[i][1] == f_y:
                print("found!!!")
                Game_Running = False


#создаем цикл для постоянного движения змейки
while Game_Running:
    check_can_we_delete_snake_item()
    check_if_we_found_present()
    check_if_borders()
    check_we_touch_self(snake_x + snake_x_nav, snake_y + snake_y_nav)
    snake_x = snake_x + snake_x_nav
    snake_y = snake_y + snake_y_nav
    snake_paint_item(canvas, snake_x, snake_y)
    tk.update_idletasks()
    tk.update()
    #задержка
    time.sleep(1)


#прерывание обработки событий при достижении конца игры
def fun_nothing(event):
    pass
canvas.bind_all("<KeyPress-Left>", fun_nothing)
canvas.bind_all("<KeyPress-Right>", fun_nothing)
canvas.bind_all("<KeyPress-Up>", fun_nothing)
canvas.bind_all("<KeyPress-Down>", fun_nothing)
