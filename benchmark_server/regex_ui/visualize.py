import base64
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


def plot_result(engine_data):
    entries = []
    for result in  engine_data:
        string = result[0]
        for i, time in enumerate(result[1:]):
            entries.append([i, string, float(time.split(" ms")[0] if time != "Error" else 0.0)])

    df = pd.DataFrame(entries, columns=['Regex', 'String', 'ExecutionTime'])
    pivot_table = df.pivot(index='Regex', columns='String', values='ExecutionTime')

    times = pivot_table.to_numpy()
    regexes = pivot_table.index.tolist()
    strings = pivot_table.columns.tolist()

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xpos, ypos = np.meshgrid(np.arange(times.shape[1]), np.arange(times.shape[0]))
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros_like(xpos)

    dz = times.flatten() 
    dx = dy = np.ones_like(dz)

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

    ax.set_xlabel('String Index')
    ax.set_ylabel('Regex Index')
    ax.set_zlabel('Average Time (s)')

    ax.view_init(elev=30, azim=30)
    x_ticks = np.linspace(0, len(strings) - 1, 8, dtype=int)
    y_ticks = np.linspace(0, len(regexes) - 1, 8, dtype=int)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    # ax.set_xticks(np.arange(len(strings)))
    # ax.set_yticks(np.arange(len(regexes)))

    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url