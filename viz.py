import matplotlib.pyplot as plt
import numpy as np

class TimeCluster:
    def __init__(self, time_series, reduced_data, figsize=(16,9)):
        """
        time_series : ndarray
            numpy ndarray of shape (n, 2), where n is the total number of
            points. The array is ordered as (time, data).

        reduced_data : ndarray
            numpy ndarray of the same shape as time_series. The array order
            is arbitrary, probably decided by your dimensionality reduction
            technique.
        """
        if time_series.shape != reduced_data.shape:
            err = ('time_series and reduced_data must have the same dimensions, '
                  f'not {time_series.shape} and {reduced_data.shape}')
            raise ValueError(err)
        self.ts = time_series
        self.X = reduced_data
        self.figsize = figsize

        self.color = 1
        self.brush_size = 0.1
        self.line_style = dict(linestyle='-', color='gray', alpha=0.3)
        self.scatter_style = dict(marker='o', color='none')
        self.label_mask = np.zeros_like(time_series[:,0])
        self.edge_colors = np.array(['C0']*self.ts.shape[0])

    def on_mouse_press(self, event):
        if not event.dblclick or event.inaxes!=self.reduced_axes:
            # Return early if not a double click
            return
        elif event.button == 1:
            # double click of primary mouse button
            self.on_primary_dblclick(event)

        self.update_axes()

    def on_primary_dblclick(self, event):
        x_radius = np.diff(self.reduced_axes.get_xlim())*self.brush_size/2
        y_radius = np.diff(self.reduced_axes.get_ylim())*self.brush_size/2
        ellipse_axis = np.array([x_radius, y_radius]).T

        click_point = np.array([[event.xdata, event.ydata]])
        squared_difference = (self.X - click_point)**2
        selected_points = np.sum(squared_difference/(ellipse_axis**2), axis=1) <= 1

        self.label_mask[selected_points] = self.color
        self.edge_colors[selected_points] = f'C{self.color}'

    def on_key_press(self, event):
        key = event.key
        if not key in ('n', 'm', ',', '.', 'b'):
            # Return early if not one of the keys we listen to
            return
        elif key in ('n', 'm'):
            self.change_color(key)
        elif key in (',', '.'):
            self.change_brush_size(key)
        elif key == 'b':
            self.reset_labels()

        self.update_axes()

    def change_color(self, key):
        if key == 'n':
            self.color += 1
        elif key == 'm':
            self.color -= 1
        self.color = self.color%10

    def change_brush_size(self, key):
        if key == ',':
            self.brush_size *= 2
        elif key == '.':
            self.brush_size /= 2
        # Don't go past the bounds
        self.brush_size = np.clip(self.brush_size, 1/20, 1/5)

    def reset_labels(self):
        self.label_mask = np.zeros_like(self.ts[:,0])
        self.edge_colors = np.array(['C0']*self.ts.shape[0])

    def update_axes(self):
        self.time_scatter.set_edgecolors(self.edge_colors)
        self.reduced_scatter.set_edgecolors(self.edge_colors)
        self.color_text.set_text(f'Color: {self.color}')
        self.color_text.set_color(f'C{self.color}')
        self.brush_text.set_text(f'Brush: {self.brush_size}')
        self.time_axes.redraw_in_frame()
        self.reduced_axes.redraw_in_frame()
        plt.show()

    def set_up_text(self):
        trans = self.reduced_axes.transAxes
        self.color_text = self.reduced_axes.text(-0.1, 0.7, s=f'Color: {self.color}', color=f'C{self.color}', transform=trans)
        self.brush_text = self.reduced_axes.text(-0.1, 0.6, s=f'Brush: {self.brush_size}', transform=trans)

        com ="Commands:\nn color up\nm color down\n, brush up\n. brush down\nb clear"
        self.reduced_axes.text(-0.1, 0.4, s=com, transform=trans)

    def start_viz(self):
        # Set up figure
        fig = plt.figure(figsize=self.figsize, constrained_layout=True)
        gs = fig.add_gridspec(3, 3)
        self.time_axes = fig.add_subplot(gs[0, :])
        self.reduced_axes = fig.add_subplot(gs[1:, :])

        # Plot data
        self.time_axes.plot(*self.ts.T, **self.line_style)
        self.reduced_axes.plot(*self.X.T, **self.line_style)
        self.time_scatter = self.time_axes.scatter(*self.ts.T, edgecolors=self.edge_colors, **self.scatter_style)
        self.reduced_scatter = self.reduced_axes.scatter(*self.X.T, edgecolors=self.edge_colors, **self.scatter_style)
        self.set_up_text()

        # Hook up callbacks
        fig.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        # Show
        plt.show()
