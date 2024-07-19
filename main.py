import cv2
import numpy as np
import pyautogui
import keyboard
import time

pyautogui.FAILSAFE = False  # Enable failsafe mode

skills_found = True  # If true, skills will be used (MORE SLOW)

auto_mode = False
ignore_specific_type = 2

key_to_start = "j"
key_to_force_unignore = "y"
blocks_count = [8, 8]

start_coords = [230, 135]
end_coords = [955, 850]

drag_distance = 75  # also block width

match_threshold = 0.82  # Matching threshold - lower is faster but less accurate

block_padding = 5

basic_block_types = 6  # images b1.png - b6.png

max_zeros_to_fail = 1

# Load block images
block_images = [
    cv2.imread(f"b{i}.png", cv2.IMREAD_COLOR) for i in range(1, basic_block_types + 1)
]


if skills_found:
    skill_images_q = [
        cv2.imread(f"q{i}.png", cv2.IMREAD_COLOR)
        for i in range(1, basic_block_types + 1)
    ]
    skill_images_w = [
        cv2.imread(f"w{i}.png", cv2.IMREAD_COLOR)
        for i in range(1, basic_block_types + 1)
    ]


def captureScreen():
    # Capture a region of the screen
    screen = pyautogui.screenshot(
        region=(
            start_coords[0],
            start_coords[1],
            end_coords[0] - start_coords[0],
            end_coords[1] - start_coords[1],
        )
    )
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    return screen


def matchBlocks(screen):
    block_map = np.zeros(blocks_count, dtype=int)
    block_height = (end_coords[1] - start_coords[1]) // blocks_count[1]
    block_width = (end_coords[0] - start_coords[0]) // blocks_count[0]

    zeros_count = 0
    for i in range(blocks_count[1]):
        for j in range(blocks_count[0]):
            block = screen[
                i * block_height : (i + 1) * block_height,
                j * block_width : (j + 1) * block_width,
            ]
            founded = False
            if skills_found:
                if not founded:
                    for idx, skill_img in enumerate(skill_images_w):
                        res = cv2.matchTemplate(block, skill_img, cv2.TM_CCOEFF_NORMED)
                        if np.max(res) > match_threshold:  # Matching threshold
                            block_map[i, j] = idx + 1
                            founded = True
                            break
                if not founded:
                    for idx, skill_img in enumerate(skill_images_q):
                        res = cv2.matchTemplate(block, skill_img, cv2.TM_CCOEFF_NORMED)
                        if np.max(res) > match_threshold:  # Matching threshold
                            block_map[i, j] = idx + 1
                            founded = True
                            break
            if not founded:
                for idx, block_img in enumerate(block_images):
                    res = cv2.matchTemplate(block, block_img, cv2.TM_CCOEFF_NORMED)
                    if np.max(res) > match_threshold:  # Matching threshold
                        block_map[i, j] = idx + 1
                        founded = True
                        break
            if not founded:
                zeros_count += 1
    if zeros_count > max_zeros_to_fail:
        return None
    return block_map


def apply_move(board, x, y, direction):
    new_board = [row[:] for row in board]
    if direction == "left":
        new_board[x][y], new_board[x][y - 1] = new_board[x][y - 1], new_board[x][y]
    elif direction == "right":
        new_board[x][y], new_board[x][y + 1] = new_board[x][y + 1], new_board[x][y]
    elif direction == "up":
        new_board[x][y], new_board[x - 1][y] = new_board[x - 1][y], new_board[x][y]
    elif direction == "down":
        new_board[x][y], new_board[x + 1][y] = new_board[x + 1][y], new_board[x][y]
    return new_board


def findBestMove(block_map, ignore_specific_type_real):
    def count_matches(board):
        max_length = 0
        rows, cols = board.shape
        # Check horizontal matches
        for r in range(0, rows):
            length = 1
            for c in range(cols - 1, 0, -1):
                if ignore_specific_type_real:
                    if board[r, c] == ignore_specific_type_real:
                        continue
                if board[r, c] == board[r, c - 1]:
                    length += 1
                else:
                    length = 1
                max_length = max(max_length, length)

        # Check vertical matches
        for c in range(0, cols):
            length = 1
            for r in range(rows - 1, 0, -1):
                if ignore_specific_type_real:
                    if board[r, c] == ignore_specific_type_real:
                        continue
                if board[r, c] == board[r - 1, c]:
                    length += 1
                else:
                    length = 1
                max_length = max(max_length, length)

        return max_length

    def make_move(board, x1, y1, x2, y2):
        board_copy = board.copy()
        board_copy[x1, y1], board_copy[x2, y2] = board_copy[x2, y2], board_copy[x1, y1]
        return board_copy

    directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
    best_move = None
    max_matches = 0
    rows, cols = block_map.shape

    for r in range(rows):
        for c in range(cols):
            for direction, (dr, dc) in directions.items():
                nr, nc = r + dr, c + dc
                # Check if the new position is within bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Perform the move
                    new_map = make_move(block_map, r, c, nr, nc)
                    # Check the number of matches after the move
                    matches = count_matches(new_map)
                    if matches > max_matches:
                        max_matches = matches
                        best_move = [r, c, direction]

    return best_move if best_move else None


def dragMove(start_x, start_y, direction):
    # Define the drag distance
    if direction == "up":
        end_x, end_y = start_x, start_y - drag_distance
    elif direction == "down":
        end_x, end_y = start_x, start_y + drag_distance
    elif direction == "left":
        end_x, end_y = start_x - drag_distance, start_y
    elif direction == "right":
        end_x, end_y = start_x + drag_distance, start_y
    else:
        raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")

    # Perform the drag-and-drop action
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.2)  # Duration to make it more natural
    pyautogui.mouseUp()


def findCoordsToMove(x, y):
    x_coord = (
        start_coords[0]
        + (y + 1) * (drag_distance + block_padding * 2)
        - drag_distance / 2
    )
    y_coord = (
        start_coords[1]
        + (x + 1) * (drag_distance + block_padding * 2)
        - drag_distance / 2
    )

    return [x_coord, y_coord]


def resetCursor():
    pyautogui.moveTo(0, 0, duration=0.0)


def resetCursorFail():
    pyautogui.moveTo(0, 100, duration=0.0)


def checkGameOver():
    # gameoverpng = cv2.imread("gameover.png", cv2.IMREAD_COLOR)
    # if gameoverpng is None:
    #     return True
    # res = cv2.matchTemplate(captureScreen(), gameoverpng, cv2.TM_CCOEFF_NORMED)
    # if np.max(res) > match_threshold:
    #     return True
    # return False
    return True


def main():
    ignore_specific_type_real = ignore_specific_type
    # check game over any 20 seconds
    time.sleep(3)
    checkGameOver()
    start_time = time.time()
    while True:
        force_unignore = False
        if keyboard.is_pressed(key_to_force_unignore):
            force_unignore = True
        if keyboard.is_pressed(key_to_start) or auto_mode or force_unignore:
            if force_unignore:
                ignore_specific_type_real = False
            else:
                ignore_specific_type_real = ignore_specific_type
            # Step 1: Capture screen
            screen = captureScreen()

            # Step 2: Determine blocks and build map with blocks
            block_map = matchBlocks(screen)
            if block_map is None:
                if auto_mode:
                    if time.time() - start_time > 30:
                        start_time = time.time()
                        if checkGameOver():
                            pyautogui.click(950, 580)
                            time.sleep(3)
                            pyautogui.click(950, 580)
                            time.sleep(3)
                            pyautogui.click(850, 780)
                            time.sleep(3)
                            pyautogui.click(850, 780)
                            time.sleep(3)
                resetCursorFail()
                continue

            # Step 3: Find all possible moves
            move = findBestMove(block_map, ignore_specific_type_real)
            if move is not None:
                start_time = time.time()
                print("Possible move:", move)
                coords = findCoordsToMove(move[0], move[1])
                dragMove(coords[0], coords[1], move[2])
                resetCursor()


if __name__ == "__main__":
    main()
