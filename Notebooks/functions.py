import numpy as np
import matplotlib.pyplot as plt

COLORS = ['blue', 'green', 'red', 'black','orange','mediumblue', 'green', 'indianred', 'darkorchid', 'seashell', 'teal', 'darkgrey', 'midnightblue', 'lightslategray', 'cornsilk',
          'seagreen', 'goldenrod', 'turquoise', 'darkorange', 'dimgray', 'lawngreen', 'darkblue', 'lime', 'cadetblue', 'mistyrose', 'mediumorchid', 'mediumseagreen', 'lightyellow', 'mediumspringgreen', 'black', 'darkviolet', 'lightskyblue', 'silver', 'maroon', 'darkkhaki', 'aliceblue', 'gray', 'lightgrey', 'darkslategray', 'magenta', 'palegoldenrod', 'steelblue', 'yellow']
MARKERS = [".","o","o","s","p","*","+","X","|","v","^","H","<",">","1","2","3","x","D","h"] * 5

def load_data(path, is_header=False):
    """
    Load dataset.

    :param path: file path
    :type path: str
    :param is_header: true if file has header
    :type is_header: bool
    :return: data and header as tuple (numpy array, str list)
    """
    file = open(path, "r")
    data = []
    header = []
    for line in file:
        splitted_line = line.split(",")
        if is_header:
            splitted_line[-1] = splitted_line[-1].strip()
            header.extend(list(map(str, splitted_line)))
            is_header = False
            continue
        data.append(list(map(float, splitted_line)))
    result = np.array(data)
    return (result, header)


def format_number(num):
    """
    Removing trailing zeros.

    :param num: input number
    :type num: float
    :return: formatted number as str
    """
    str_num = str(num)
    if "." in str_num:
        splitted_num = str_num.split(".")
        if int(splitted_num[-1]) == 0:
            return "".join(splitted_num[:-1])
        else:
            return str_num
    else:
        return str_num


def plot_func(
        x,
        y,
        title,
        x_label,
        y_label,
        color='green',
        legend=[],
        marker=[],
        linewidth=3,
        multi=False):
    """
    Plot function.

    :param x: x-axis data
    :type x: list or numpy array
    :param y: y-axis data
    :type y: list or numpy array
    :param title: plot title
    :type title: str
    :param x_label: x-axis label
    :type x_label: str
    :param y_label: y-axis label
    :type y_label: str
    :param color: plot color
    :type color: str or list
    :param legend: plot legends
    :type legend: list
    :param marker : data marker
    :type marker: list
    :param linewidth: plot line width
    :type linewidth: int
    :param multi: multi plot flag
    :type multi: bool
    :return: None
    """
    plt.figure()
    plt.grid()
    if multi:
        for index, y_item in enumerate(y):
            plt.plot(x[index], y_item, color=color[index], marker=marker[index], linewidth=linewidth)
    else:
        plt.plot(x, y, color=color, linewidth=linewidth)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if len(legend) != 0:
        plt.legend(legend)
    plt.show()


def impedance_plot(data, SBH, catalyst_loading, header=None):
    """
    Impedance plot function.

    :param data: input data
    :type data: numpy array
    :param SBH: sbh weightpercent
    :type SBH: float
    :param catalyst_loading: catalyst loading
    :type catalyst_loading: float
    :param header: input header
    :type header: list
    :return: None
    """
    voltage_col = 2
    sbh_col = 3
    load_col = 4
    if len(header) > 0:
        voltage_col = header.index('applied_voltage')
        sbh_col = header.index('sbh_weight_percent')
        load_col = header.index('catalyst_loading')
    voltages = sorted(list(set(data[:, voltage_col])))
    x_plot_data = []
    y_plot_data = []
    filtered_data = data[data[:, sbh_col] == SBH]
    filtered_data = filtered_data[filtered_data[:, load_col] == catalyst_loading]
    for v in voltages:
        x_plot_data.append(filtered_data[filtered_data[:, voltage_col] == v][:, 0])
        y_plot_data.append(filtered_data[filtered_data[:, voltage_col] == v][:, 1])
    legend = list(map(lambda x: "V: "+format_number(x)+"V",voltages))
    color = COLORS[:len(legend)]
    marker = MARKERS[:len(legend)]
    x_label = "ZReal(Ohm)"
    y_label = "ZImage(Ohm)"
    title = "SBH = {} | Catalyst Loading = {}".format(SBH, catalyst_loading)

    plot_func(
        x_plot_data,
        y_plot_data,
        title=title,
        x_label=x_label,
        y_label=y_label,
        color=color,
        legend=legend,
        marker=marker,
        multi=True)


def polarization_plot(data, RH, P, NP=None, MC=None):
    """
    Polarization plot function.

    :param data: input data
    :type data: numpy array
    :param RH: Relative humidity (RH%)
    :type RH: float
    :param P: Pressure (psi)
    :type P: float
    :param NP: Nafion percent
    :type NP: float
    :param MC: Membrane compression
    :type MC: float
    :return: None
    """
    filtered_data = data[data[:, 4] == RH]
    filtered_data = filtered_data[filtered_data[:, 3] == P]
    title = "RH: {}% , P: {}psig".format(str(RH), str(P))
    if NP is not None :
        filtered_data = filtered_data[filtered_data[:, 6] == NP]
        title += ", NP: {}".format(str(NP))
    if MC is not None :
        filtered_data = filtered_data[filtered_data[:, 5] == MC]
        title += ", MC: {}".format(str(MC))
    data_I = filtered_data[:, 0]
    data_V = filtered_data[:, 1]
    data_P = filtered_data[:, 2]
    color1 = COLORS[0]
    color2 = COLORS[1]
    x_label = "Current density (mA/cm2 )"
    y_label_1 = "Cell voltage (V)"
    y_label_2 = "Power density (mW/cm2)"

    plot_func(
        data_I,
        data_V,
        title=title,
        x_label=x_label,
        y_label=y_label_1,
        color=color1)
    plot_func(
        data_I,
        data_P,
        title=title,
        x_label=x_label,
        y_label=y_label_2,
        color=color2)
