import pyqtgraph as pg

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush

from .core_properties import CWTM_ResourceBarLevelColours


class CWTM_ResourceGraphWidget(pg.PlotWidget):
    def __init__(self, parent=None,
                 grid_color='g',
                 percentage=False,
                 show_left_values=False,
                 grid_size_x=4, grid_size_y=16,
                 dotted_grid_lines=False):
        super().__init__(parent)
        self.RESOURCE_GRAPH_WIDGET_SPACING_MAJOR = 1024
        self.RESOURCE_GRAPH_WIDGET_SPACING_MINOR = 256

        self.setBackground('k')

        self.x_grid_pen = pg.mkPen(color=grid_color, width=1)
        self.y_grid_pen = pg.mkPen(color=grid_color, width=1)

        if dotted_grid_lines:
            self.x_grid_pen.setStyle(Qt.DotLine)
            self.y_grid_pen.setStyle(Qt.DotLine)

        plot_item = self.getPlotItem()
        plot_item.hideButtons()

        self.plot_left_axis = plot_item.getAxis("left")
        self.plot_bottom_axis = plot_item.getAxis("bottom")

        self.plot_bottom_axis.setTickSpacing(grid_size_x, grid_size_x)
        self.plot_left_axis.setTickSpacing(grid_size_y, grid_size_y)
        plot_item.showGrid(x=True, y=True, alpha=1)
        self.plot_bottom_axis.setPen(self.x_grid_pen)
        self.plot_left_axis.setPen(self.y_grid_pen)
        self.plot_bottom_axis.setStyle(showValues=False)
        self.plot_left_axis.setStyle(showValues=show_left_values)
        self.plot_left_axis.setTextPen("y")

        if show_left_values:
            self.plot_left_axis.setWidth(75)
            self.plot_left_axis.setTickSpacing(
                major=self.RESOURCE_GRAPH_WIDGET_SPACING_MAJOR, 
                minor=self.RESOURCE_GRAPH_WIDGET_SPACING_MINOR
            )

        self.setMouseEnabled(x=False, y=False)
        self.getPlotItem().setMouseEnabled(x=False, y=False)

        self.getPlotItem().getViewBox().setMenuEnabled(False)

        if percentage:
            self.setYRange(0, 100, padding=0)

    def get_all_data_axes(self, x_range=100):
        return [i for i in range(x_range)], [0 for _ in range(x_range)] # x, y

    def get_equal_tick_spacing(self, n_ticks):
        min_y, max_y = self.viewRange()[1]
        min_y = 0 if min_y < 0 else min_y
        if 0 <= max_y <= 32:
            return []  # or handle appropriately
        
        interval = (max_y - min_y) / n_ticks
        ticks = [min_y + i * interval for i in range(n_ticks + 1)]
        return ticks
            
    def update_plot(self, plot_item, new_value, total_data_x, total_data_y):
        total_data_y.append(new_value)
        total_data_x.append(total_data_x[-1] + 1)

        total_data_y.pop(0)
        total_data_x.pop(0)

        plot_item.setZValue(1)
        plot_item.setData(total_data_x, total_data_y)

class CWTM_ResourceLevelBarWidget(QWidget):
    def __init__(self, bar_parameters, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bar_parameters = bar_parameters

        self.resource_value = 1
        self.total_space  = 1

        self.bar_parameters.x_offset //= self.bar_parameters.offset_factor
        self.bar_parameters.y_offset //= self.bar_parameters.offset_factor

        self.x_offset_progress_bar_1 = self.bar_parameters.x_offset
        self.x_offset_progress_bar_2 = self.x_offset_progress_bar_1 \
                                       + self.bar_parameters.bar_width \
                                       + (self.bar_parameters.bar_width // 10)

        self.primary_bar_colour_filled = None
        self.primary_bar_colour_empty = None
        self.secondary_bar_colour_filled = None
        self.secondary_bar_colour_empty = None

        self.primary_resource_value = None
        self.secondary_resource_value = None
        self.total_space  = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0))

        # Draw primary resource bars
        for x_offset in [self.x_offset_progress_bar_1, self.x_offset_progress_bar_2]:
            self.draw_resource_bar_levels(
                painter, x_offset, 
                self.primary_resource_value,
                self.primary_bar_colour_filled,
                self.primary_bar_colour_empty)

        # Draw secondary resource bars if available
        if self.secondary_bar_colour_filled is not None:
            for x_offset in [self.x_offset_progress_bar_1, self.x_offset_progress_bar_2]:
                self.draw_resource_bar_levels(
                    painter, x_offset, 
                    self.secondary_resource_value,
                    self.secondary_bar_colour_filled,
                    self.secondary_bar_colour_empty,
                    draw_empty_bars=False)

        painter.setPen(self.primary_bar_colour_filled)
        painter.setBrush(self.primary_bar_colour_filled)

        painter.drawText(
            self.x_offset_progress_bar_1 * self.bar_parameters.offset_factor // 4,
            self.bar_parameters.y_offset + self.bar_parameters.total_bars \
            * (self.bar_parameters.bar_height + self.bar_parameters.spacing) + 10,
            f'{self.primary_resource_value} {self.bar_parameters.resource_bar_label}')


    def draw_resource_bar_levels(
        self,  painter: QPainter, current_x_offset: int, resource_value: float, 
        bar_colour_filled: QColor, bar_colour_empty: QColor, *, draw_empty_bars: bool = True) -> None:
        filled_bars = int((resource_value / self.total_space) * self.bar_parameters.total_bars)
        total_current_bars = self.bar_parameters.total_bars if draw_empty_bars else filled_bars

        brush_filled = QBrush(bar_colour_filled)
        pen_filled = QPen(bar_colour_filled)
        brush_empty = QBrush(bar_colour_empty)
        pen_empty = QPen(bar_colour_empty)

        for i in range(total_current_bars):
            if i < filled_bars:
                brush, pen = brush_filled, pen_filled
            else:
                brush, pen = brush_empty, pen_empty

            painter.setBrush(brush)
            painter.setPen(pen)

            rect_y = (
                self.bar_parameters.y_offset 
                + (self.bar_parameters.total_bars - 1 - i) 
                * (self.bar_parameters.bar_height + self.bar_parameters.spacing)
            )
            painter.drawRect(
                current_x_offset, 
                rect_y,
                self.bar_parameters.bar_width,
                self.bar_parameters.bar_height
            )

        painter.setPen(bar_colour_filled)

    def set_resource_value(
        self, primary_resource_value, secondary_resource_value, total_space, 
        primary_bar_colour_filled, primary_bar_colour_empty,
        secondary_bar_colour_filled, secondary_bar_colour_empty):
        self.primary_bar_colour_filled = primary_bar_colour_filled
        self.primary_bar_colour_empty = primary_bar_colour_empty
        self.secondary_bar_colour_filled = secondary_bar_colour_filled
        self.secondary_bar_colour_empty = secondary_bar_colour_empty

        self.primary_resource_value = primary_resource_value
        self.secondary_resource_value = secondary_resource_value
        self.total_space  = total_space
        self.update()  # Request a repaint


class CWTM_QNumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, value, *, label=""):
        super().__init__(value + " " + label)  # Store the string representation
        self.value = float(value) if value else -1
        # Store the numeric value for comparisons

    def __lt__(self, other):
        return self.value < other.value  # Direct comparison with the numeric value

    def text(self):
        return super().text().strip()
