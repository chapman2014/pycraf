from astropy import units as u
from pycraf import pathprof, conversions as cnv


def plot_atten_map(lons, lats, total_atten):

    import matplotlib.pyplot as plt

    vmin, vmax = -5, 195
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_axes((0., 0., 1.0, 1.0))
    cbax = fig.add_axes((0., 0., 1.0, .02))
    cim = ax.imshow(
        total_atten,
        origin='lower', interpolation='nearest', cmap='inferno_r',
        vmin=vmin, vmax=vmax,
        extent=(lons[0], lons[-1], lats[0], lats[-1]),
        )
    cbar = fig.colorbar(
        cim, cax=cbax, orientation='horizontal'
        )
    ax.set_aspect(abs(lons[-1] - lons[0]) / abs(lats[-1] - lats[0]))
    cbar.set_label(r'Path propagation loss')
    ctics = np.arange(30, 200, 30)
    cbar.set_ticks(ctics)
    cbar.ax.set_xticklabels(map('{:.0f} dB'.format, ctics))
    ax.set_xlabel('Longitude [deg]')
    ax.set_ylabel('Latitude [deg]')

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.show()


lon_tx, lat_tx = 6.88361 * u.deg, 50.52483 * u.deg
map_size_lon, map_size_lat = 0.5 * u.deg, 0.5 * u.deg
map_resolution = 10. * u.arcsec

freq = 1. * u.GHz
omega = 0. * u.percent  # fraction of path over sea
temperature = 290. * u.K
pressure = 1013. * u.hPa
timepercent = 2 * u.percent  # see P.452 for explanation
h_tg, h_rg = 50 * u.m, 10 * u.m
G_t, G_r = 0 * cnv.dBi, 0 * cnv.dBi
zone_t, zone_r = pathprof.CLUTTER.UNKNOWN, pathprof.CLUTTER.UNKNOWN
hprof_step = 100 * u.m

hprof_cache = pathprof.height_profile_data(
    lon_tx, lat_tx,
    map_size_lon, map_size_lat,
    map_resolution=map_resolution,
    zone_t=zone_t, zone_r=zone_r,
    )  # dict-like

atten_maps, eps_pt_map, eps_pr_map = pathprof.atten_map_fast(
    freq,
    temperature,
    pressure,
    h_tg, h_rg,
    timepercent,
    hprof_cache,
    )

lons = hprof_cache['xcoords']
lats = hprof_cache['ycoords']
# index 4 is total loss without clutter/gain included:
total_atten = atten_maps[4]

plot_atten_map(lons, lats, total_atten)