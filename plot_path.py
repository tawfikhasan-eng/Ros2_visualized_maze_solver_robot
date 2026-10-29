
import ast
import sys

import matplotlib.pyplot as plt


def load(path):
    global xs, ys
    xs, ys = [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = ast.literal_eval(line)
            xs.append(float(p['x']))
            ys.append(float(p['y']))
            
    return xs, ys


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'pose.data'
    load(path)

    plt.figure(figsize=(7, 7))
    plt.plot(xs, ys, '-o', markersize=2, linewidth=1.5, label='The Path')
    plt.scatter(xs[0], ys[0], c='green', s=80, label='Start')
    plt.scatter(xs[-1], ys[-1], c='red', s=80, label='End')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('Robot path in the maze')
    plt.axis('equal')
    plt.grid(True, alpha=0.4)
    plt.legend()
    plt.savefig('path.png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    main()
