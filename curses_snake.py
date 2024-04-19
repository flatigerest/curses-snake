import curses
from random import randint


def print_border(stdscr, max_y, max_x):
    h = chr(0x2501)
    v = chr(0x2502)
    tl = chr(0x250d)
    tr = chr(0x2511)
    bl = chr(0x2515)
    br = chr(0x2519)
    top = tl + ''.join(h for _ in range(max_x - 2)) + tr
    bottom = bl + ''.join(h for _ in range(max_x - 2)) + br
    stdscr.addstr(0, 0, top)
    stdscr.addstr(max_y - 2, 0, bottom)
    for x in range(1, max_y - 2):
        stdscr.addstr(x, 0, v)
        stdscr.addstr(x, max_x - 1, v)


def main(stdscr):
    max_y, max_x = stdscr.getmaxyx()
    pos_y = int(max_y / 2)
    pos_x = int(max_x / 2)
    current_dir = "r"

    snake_length = 5
    snake_char = "o"
    snake_body = []
    speed = 100
    for x in range(snake_length):
        i = snake_length - x
        snake_body.append((pos_y, pos_x - i))
    snake_body.append((pos_y, pos_x))

    apple_char = '@'
    while True:
        apple_pos = (randint(1, max_y - 3), randint(1, max_x - 2))
        if apple_pos not in snake_body:
            break

    stdscr.nodelay(True)

    while True:
        stdscr.timeout(speed)
        stdscr.clear()
        print_border(stdscr, max_y=max_y, max_x=max_x)
        stdscr.addstr(apple_pos[0], apple_pos[1], apple_char)
        for pos in snake_body:
            stdscr.addstr(pos[0], pos[1], snake_char)

        key = stdscr.getch()
        if key == curses.KEY_UP:
            current_dir = "u"
        elif key == curses.KEY_DOWN:
            current_dir = "d"
        elif key == curses.KEY_RIGHT:
            current_dir = "r"
        elif key == curses.KEY_LEFT:
            current_dir = "l"
        elif key == ord('q'):
            break

        if current_dir == "u":
            pos_y -= 1
            if pos_y < 1:
                break
        elif current_dir == "d":
            pos_y += 1
            if pos_y > max_y - 3:
                break
        elif current_dir == "r":
            pos_x += 1
            if pos_x > max_x - 2:
                break
        elif current_dir == "l":
            pos_x -= 1
            if pos_x < 1:
                break

        pos = (pos_y, pos_x)
        if pos == apple_pos:
            snake_length += 1
            speed = int(0.9 * speed)
            while True:
                apple_pos = (randint(1, max_y - 3), randint(1, max_x - 2))
                if apple_pos not in snake_body:
                    break
        if pos in snake_body:
            break
        snake_body.append(pos)
        if len(snake_body) > snake_length:
            snake_body.pop(0)

        stdscr.refresh()
    stdscr.timeout(-1)
    stdscr.addstr(0, 0, "YOU DIED RIPPPPPP")
    stdscr.getch()



curses.wrapper(main)


'''
TODO:
1. Fix turning back on self ie if going left cannot go right
2. Apple spawned in wall
3. Add score
'''