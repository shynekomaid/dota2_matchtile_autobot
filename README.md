# dota2_matchtile_autobot
Will found moves and perform it (crownfall3)

# Dota 2 Crownfall 3 Matchtile Game Solver

This repository contains a solver for the Dota 2 Crownfall 3 Matchtile game. The solver automates the process of matching tiles in the game using computer vision and automation libraries.

`Note: optimized for fullHd and max video settings, for another cases you may need to regenerate images`

## Disclaimer

IMPORTANT DISCLAIMER

This software is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

USE AT YOUR OWN RISK

This solver is intended for educational and entertainment purposes only. Using automation tools in games may violate the terms of service of the game. By using this software, you acknowledge that you understand the risks involved, including but not limited to potential bans, account suspension, or other penalties imposed by the game developers or publishers.

THE AUTHOR IS NOT LIABLE

The author of this software is not responsible for any consequences resulting from the use of this software. If you are banned or otherwise penalized for using this software, the author is not liable and will not provide any form of compensation or assistance.

NO WARRANTY

The software is provided without any warranty of any kind. The author does not guarantee that the software will function correctly, be error-free, or meet your specific requirements. Any reliance you place on the software is strictly at your own risk.

MODIFICATION AND REDISTRIBUTION

You are free to modify and redistribute this software, provided that the original author is credited, and this disclaimer remains intact in all copies and derivatives.

USE RESPONSIBLY

Please use this software responsibly and ethically. Do not use it to gain an unfair advantage over other players or to disrupt the gaming experience for others.

By using this software, you agree to the terms of this disclaimer. If you do not agree to these terms, do not use the software.


## Table of Contents
- [Discplaimer](#disclaimer)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)

## Installation

To install the necessary dependencies, ensure you have Python 3 installed and run the following command:

```bash
pip install opencv-python numpy pyautogui keyboard Pillow
```

## Usage

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/dota2-crownfall3-solver.git
    cd dota2-crownfall3-solver
    ```

2. Place the images (`b1.png` to `w6.png`) in the same directory as the script (if you has another screen resolution, also you need adjust click coords in code).

3. Run the solver script:
    ```bash
    cd dota2_matchtile_autobot && python main.py
    ```

4. The script will start in an idle state. Press the key specified in `key_to_start` (default is 'j') to start the solver.

5. To force unignore specific blocks, press the key specified in `key_to_force_unignore` (default is 'y').

## Options

- `skills_found`: If set to `True`, skills will be used, making the process slower. The default is `True`.

- `auto_mode`: If set to `True`, the solver will run in auto mode (no key press required; due hardest animation will make move only one time in 2-3 seconds, usually score is 5-10k). The default is `False`.

- `ignore_specific_type`: Specifies the type of block to ignore. The default is `2`. Ignoring QoP points will help manually stack Swap - most crazy and terrible own weapon.

- `key_to_start`: The key to press to start the solver. The default is 'j'.

- `key_to_force_unignore`: The key to press to force unignore specific blocks. The default is 'y'.

- `blocks_count`: Specifies the number of blocks in the grid. The default is `[8, 8]`.

- `start_coords`: The starting coordinates of the grid. The default is `[230, 135]`.

- `end_coords`: The ending coordinates of the grid. The default is `[955, 850]`.

- `drag_distance`: The distance to drag when matching tiles. The default is `75` (which is also the block width).

- `match_threshold`: The threshold for matching blocks. Lower values are faster but less accurate. The default is `0.82`.

- `block_padding`: The padding between blocks. The default is `5`.

- `basic_block_types`: The number of basic block types (images `b1.png` to `b6.png`). The default is `6`.

- `max_zeros_to_fail`: The maximum number of zeros allowed before the solver fails. The default is `1`.

Feel free to modify these options in the script to suit your needs.
