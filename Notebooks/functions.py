import numpy as np
import matplotlib.pyplot as plt

COLORS = ['blue', 'green', 'red', 'black','orange','mediumblue', 'green', 'indianred', 'darkorchid', 'seashell', 'teal', 'darkgrey', 'midnightblue', 'lightslategray', 'cornsilk',
          'seagreen', 'goldenrod', 'turquoise', 'darkorange', 'dimgray', 'lawngreen', 'darkblue', 'lime', 'cadetblue', 'mistyrose', 'mediumorchid', 'mediumseagreen', 'lightyellow', 'mediumspringgreen', 'black', 'darkviolet', 'lightskyblue', 'silver', 'maroon', 'darkkhaki', 'aliceblue', 'gray', 'lightgrey', 'darkslategray', 'magenta', 'palegoldenrod', 'steelblue', 'yellow']
MARKERS = [".","o","o","s","p","*","+","X","|","v","^","H","<",">","1","2","3","x","D","h"] * 5

def load_data(path):
    """
    Load dataset.

    :param path: file path
    :type path: str
    :return: data as numpy arr
    """
    file = open(path, "r")
    data = []
    header = []
    for line in file:
        splitted_line = line.split(",")
        if len(header) == 0:
            splitted_line[-1] = splitted_line[-1].strip()
            header.extend(list(map(str, splitted_line)))
            continue
        data.append(list(map(float, splitted_line)))
    result = np.array(data)
    return result


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


def impedance_plot(data, V=None, SBH=None, CL=None):
    """
    Impedance plot function.

    :param data: input data
    :type data: numpy array
    :param header: input header
    :type header: str list
    :param V: applied voltage
    :type V: float
    :param SBH: sbh weight percent
    :type SBH: float
    :param CL: catalyst loading
    :type CL: float
    :return: None
    """
    voltages = sorted(list(set(data[:, 2])))
    SBHs = sorted(list(set(data[:, 3])))
    loadings = sorted(list(set(data[:, 4])))
    x_plot_data = []
    y_plot_data = []
    if SBH is None:
        filtered_data = data[data[:, 2] == V]
        filtered_data = filtered_data[filtered_data[:, 4] == CL]
        for sbh in SBHs:
            x_plot_data.append(filtered_data[filtered_data[:, 3] == sbh][:, 0])
            y_plot_data.append(filtered_data[filtered_data[:, 3] == sbh][:, 1])
        legend = list(map(lambda x: "SBH: "+format_number(x),SBHs))
        title = "Applied Voltage = {} | Catalyst Loading = {}".format(V, CL)

    elif CL is None:
        filtered_data = data[data[:, 3] == SBH]
        filtered_data = filtered_data[filtered_data[:, 2] == V]
        for loading in loadings:
            x_plot_data.append(filtered_data[filtered_data[:, 4] == loading][:, 0])
            y_plot_data.append(filtered_data[filtered_data[:, 4] == loading][:, 1])
        legend = list(map(lambda x: "Catalyst loading: "+format_number(x),loadings))
        title = "Applied Voltage = {} | SBH = {}".format(V, SBH)

    else:
        filtered_data = data[data[:, 3] == SBH]
        filtered_data = filtered_data[filtered_data[:, 4] == CL]
        for v in voltages:
            x_plot_data.append(filtered_data[filtered_data[:, 2] == v][:, 0])
            y_plot_data.append(filtered_data[filtered_data[:, 2] == v][:, 1])
        legend = list(map(lambda x: "V: "+format_number(x)+"V",voltages))
        title = "SBH = {} | Catalyst Loading = {}".format(SBH, CL)
    
    color = COLORS[:len(legend)]
    marker = MARKERS[:len(legend)]
    x_label = "ZReal(Ohm)"
    y_label = "ZImage(Ohm)"
    
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
