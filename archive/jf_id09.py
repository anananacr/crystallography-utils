
# -*- coding: utf-8 -*-
"""Class and functions to process data from a Jungfrau 1M detectors."""

__authors__ = ["Matteo Levantino", "Aldo Mozzanica", "Viktoria Hinger",
               "Marco Cammarata"]
__contact__ = "matteo.levantino@esrf.fr"
__licence__ = "MIT"
__copyright__ = "ESRF - The European Synchrotron, Grenoble, France"
__date__ = "13/05/2022"


import time
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import h5py
from tqdm import tqdm
import datastorage as ds


class JungfrauData:

    """
    Class for handling Jungfrau data collected in 'normal' or 'burst' mode."""

    def __init__(self, fnames, hdf5_path="data_f000000000000", nimages=None):
        """

        Parameters
        ----------
        fnames : array-like
            List of files associated to a given image (one for each module).
        hdf5_path : str, optional
            Key associated with the actual images in the input hdf5 files.
        nimages : int or None, optional
            Number of images to be analyzed. If None (optional), all
            images are analyzed.
            If more than one storage cell was used, 'nimages' is interpreted
            as the number of images per storage cell to be analyzed.

        """

        self.fnames = fnames
        self.hdf5_path = hdf5_path
        self.ds = [h5py.File(f) for f in fnames]
        self.nimages = min([ds[hdf5_path].len() for ds in self.ds])
        idx_not_empty = self.ds[0]["detector type"][:] > 0
        self.nimages = np.sum(idx_not_empty)

        self.sc_idx = (self.ds[0]["debug"][idx_not_empty] // 256) % 16
        sc_nimages = [(self.sc_idx == k).sum() for k in range(16)]
        sc_min_nimages = min([n for n in sc_nimages if n != 0])

        if self.nimages > 4600:
            print("")
            print("WARNING: nimages > 4600 !!!!!")
            print("         your script might crash.\n")

        # create storage cell attribute (16 storage cells per module)
        self.sc = []
        for k in range(16):
            self.sc.append([])

        if nimages is None:
            nimages = sc_min_nimages

        for k in tqdm(range(self.nimages)):
            sc_k = self.sc_idx[k]
            if len(self.sc[sc_k]) <= min(sc_min_nimages, nimages):
                self.sc[sc_k].append(self.get_image(k))

    def get_image(self, idx):
        res = np.array([d[self.hdf5_path][idx] for d in self.ds])
        return res

    def get_sc(self, idx):
        """Get all images of a storage cell."""
        res = np.array(self.sc[idx])
        return res

    def __getitem__(self, idx):
        return self.get_sc(idx)

    def __len__(self):
        """Total number of images."""
        return self.nimages


def process_jf_gains(fnames, sc=False, save_fname=None):
    """
    Read and process jungfrau gain maps.

    Processed gain maps can be optionally saved in a single .hdf5 file.

    Parameters
    ----------
    fnames : str or list
        Gain maps filename (.bin) or list of gain maps filenames (one for each
        module in the detector) or list of lists of gain maps filenames (one
        for each storage cell used for each module).
    save_fname : str or None, optional
        Output HDF5 filename. If None (default), data are not saved.

    Returns
    -------
    gains : ndarray(dtype=float, ndim=5)
        Processed gain maps arranged in a (nsc, nmodules, ngains, nrows, ncols)
        numpy array.
        - 'nsc' : number of detector storage cells used in the data collection
        - 'nmodules' : number of detector modules
        - 'ngains' : number of pixel gains
        - 'nrows' : number of pixel rows in each module
        - 'ncols' : number or pixel columns in each module
        For e.g. a Jungfrau 1M operated in burst mode, 'gains' has the shape:
        (16, 2, 3, 512, 1024)

    Notes
    -----
    - If fnames is a list of lists, the storage cells order will be the same
      as that in the lists.

    Example
    -------
    os.listdir("./")
    mylist = os.listdir("./")
    mylist.sort()  # works only if bottom module index is lower than top one
    mylist1 = mylist[:16]
    mylist2 = mylist[16:]
    gains = process_jf_gains([mylist1, mylist2], sc=True)

    """

    nmodules, nsc = 1, 1

    if isinstance(fnames, str):
        fnames = [fnames]

    nmodules = len(fnames)

    if nmodules == 0:
        raise ValueError("'fnames' cannot be an empty list.")

    if all(isinstance(f, list) for f in fnames):
        nsc = min([len(f) for f in fnames])
    elif any(isinstance(f, list) for f in fnames):
        raise ValueError("'fnames' elements must be all str or all lists.")
    else:
        fnames = [[f] for f in fnames]

    gains = np.empty((nsc, nmodules, 3, 512, 1024))

    for j in range(nsc):
        for k in range(nmodules):
            f = fnames[k][j]
            g = np.fromfile(f, dtype=np.float64, count=3*512*1024)
            gains[j, k, :, :, :] = g.reshape(3, 512, 1024)

    if save_fname is not None:
        with h5py.File(save_fname, 'w') as h5file:
            h5file.create_dataset("gains", data=gains)

    return gains


def read_jf_images(folder, basename, file_index=0, sc_index=15,
                   hdf5_path="data_f000000000000", nimages=None):
    """
    Read raw images produced by a Jungfrau 1M detector.

    Parameters
    ----------
    folder : str
        ...
    basename : str
        ...
    file_index : int, optional
        ...
    sc_index : int, optional
        ...
        Default is 15 (default storage cell used when burst is not running).
    hdf5_path : str, optional
        Key associated with the actual images in the input hdf5 files.
        Currently, if only one image per storage cell is collected,
        the images key is "data", otherwise is "data_f000000000000".
        Default is 'data_f000000000000'.
    nimages : int or None, optional
        Number of images to be analyzed. If None (optional), all
        images are analyzed.
        If more than one storage cell was used, 'nimages' is interpreted
        as the number of images per storage cell to be analyzed.

    """

    basename = str(folder) + "/" + basename
    # d0_name = basename + "_d0_f000000000000_%d.h5" % file_index
    # d1_name = basename + "_d1_f000000000000_%d.h5" % file_index
    d0_name = basename + "_d0_f0_%d.h5" % file_index
    d1_name = basename + "_d1_f0_%d.h5" % file_index

    f = ds.read(d0_name, readH5pyDataset=False)

    if hasattr(f, "data"):
        hdf5_path = "data"

    fnames = [d0_name, d1_name]

    out = JungfrauData(fnames, hdf5_path=hdf5_path, nimages=nimages)

    return out


def process_jf_darks(folder, basename, hdf5_path="data_f000000000000",
                     save=False, force=False):
    """
    Read and process jungrau darks.

    Processed darks can be optionally saved in a single .hdf5 file.

    Parameters
    ----------
    folder : str
        Folder where raw darks files are stored. Typically this is something
        like: '/data/visitor/hc5293/id09/20230517/RAW_DATA/darks'.
    basename : str
        Basename of raw darks files. Typically this is something like:
        '20230517_160511_darks_10us'.
        For a Jungfrau 1M, there will be 6 files with the same basename
        (a 'master' and a 'virtual' for each of the 3 gains):
         - 20230517_160511_darks_10us_master_0.h5
         - 20230517_160511_darks_10us_master_1.h5
         - 20230517_160511_darks_10us_master_2.h5
         - 20230517_160511_darks_10us_virtual_0.h5
         - 20230517_160511_darks_10us_virtual_1.h5
         - 20230517_160511_darks_10us_virtual_2.h5
    hdf5_path : str, optional
        Key associated with the actual images in the input hdf5 files.
        Currently, if only one image per storage cell is collected,
        the images key is "data", otherwise is "data_f000000000000".
        Default is 'data_f000000000000'.
    nimages : int or None, optional
        Number of images to be analyzed. If None (optional), all
        images are analyzed.
        If more than one storage cell was used, 'nimages' is interpreted
        as the number of images per storage cell to be analyzed.
    save : bool, optional
        If True, processed darks will be saved as a single hdf5 file.
        The folder used for saving is defined relatively to the input 'folder'
        as "../../PROCESSED_DATA/darks".
        If folder="/data/visitor/hc5293/id09/20230517/RAW_DATA/darks",
        outfolder="/data/visitor/hc5293/id09/20230517/PROCESSED_DATA/darks".
        Default is None.
    force : bool, optional
        If processed dark already exists in 'folder', it will be re-processed
        only if 'force' is True.
        If False (default), the dark will be simply read and returned.

    Returns
    -------
    darks : ndarray(dtype=float, ndim=5)
        Processed darks arranged in a (nsc, nmodules, ngains, nrows, ncols)
        numpy array.
        - 'nsc' : number of detector storage cells used in the data collection
        - 'nmodules' : number of detector modules
        - 'ngains' : number of pixel gains
        - 'nrows' : number of pixel rows in each module
        - 'ncols' : number or pixel columns in each module
        For e.g. a Jungfrau 1M operated in burst mode, 'darks' has the shape:
        (16, 2, 3, 512, 1024)

    """

    folder = pathlib.Path(folder)  # this is something like RAW_DATA/darks
    outfilename = basename + ".h5"
    folder_out = folder.parent.parent / "PROCESSED_DATA/darks"
    folder_out.mkdir(exist_ok=True)
    fout = folder_out / outfilename

    if fout.exists() and not force:
        return ds.read(fout).darks

    darks = []

    t0 = time.time()

    for gain in range(3):

        print("\nReading darks with gain index %d..." % gain)

        data = read_jf_images(folder, basename, hdf5_path=hdf5_path,
                              file_index=gain)

        print("Processing darks with gain index %d..." % gain)

        # counting the (not empty) SC
        nsc = 0
        for d in data:
            if len(d) > 0:
                nsc += 1

        print("Found %d Storage Cells with data" % nsc)

        sc = 0
        if nsc == 1:
            ave_array = np.zeros((1, 2, 512, 1024), dtype=float)
            ave_array[0] = data[15].mean(axis=0)
        else:
            ave_array = np.zeros((16, 2, 512, 1024), dtype=float)
            for d in (data):
                if len(d) > 0:
                    if gain == 0:
                        ave_array[sc] = d.mean(axis=0)
                    else:
                        # storage cell pedestal collection script takes in
                        # g1/g1 200 pedestals per cells:
                        # - 100x (SCx-1 SCx)
                        # - 100x (SCx SCx+1)
                        # We want to use the second 100x, where SC of interest
                        # is first. For the first storage cell (sc=0), we want
                        # to use the first 100x.
                        if sc == 0:
                            ave_array[sc] = d[0:99].mean(axis=0)
                        else:
                            ave_array[sc] = d[100:199].mean(axis=0)
                    sc += 1

        darks.append(ave_array)  # list of np_arrays, one per gain

    print("\nTotal processing time = %f\n" % (time.time()-t0))

    darks = np.asarray(darks)
    # we have: (ngains, nsc, nmodules, nrows, ncols)
    # we want: (nsc, nmodules, ngains, nrows, ncols)
    darks = darks.swapaxes(0, 2)
    darks = darks.swapaxes(0, 1)

    if save:

        print("Saving processed darks...")
        d = ds.DataStorage(darks=darks)
        d.save(fout)

        print("Updating symbolic link for Streamvis viewer...")
        if darks.shape[0] == 1:
            linkname = folder_out / "darks_last.h5"
        else:
            linkname = folder_out / "darks_last_sc.h5"
        print(f"{fout} -> {linkname}")
        linkname.unlink(missing_ok=True)
        linkname.symlink_to(fout)

    return darks


def expand_module_image(img):
    """
    Expand Jungfrau module image according to chips arrangements.

    Parameters
    ----------
    img : (512, 1024) ndarray
        Raw image from a single jungfrau module.

    Returns
    -------
    eimg : (514, 1032) ndarray
        Expanded image.

    """

    if img.shape != (512, 1024):
        raise ValueError("'img' shape must be (512, 1024).")

    eimg = np.zeros((514, 1032), dtype=img.dtype)

    for col in range(4):
        col_orig = slice(1+256*col, 256*(col+1)-1)
        col_new = slice(2+258*col, 258*(col+1)-2)
        eimg[0:255, col_new] = img[0:255, col_orig]
        eimg[259:514, col_new] = img[257:512, col_orig]

    return eimg


def expand_detector_image(img):
    """
    Expand Jungfrau detector image according to modules and chips arrangement.

    Parameters
    ----------
    img : (nmodules, 512, 1024) ndarray
        Raw image.

    Returns
    -------
    eimg: ndarray
        Expanded image.

    """

    nmodules = img.shape[0]
    nrows = (512+2)*nmodules + 2*36
    ncols = 1032
    eimg = np.zeros((nrows, ncols), dtype=img.dtype)

    for n in range(nmodules):
        row_new = slice(n*514+n*36, (n+1)*514+n*36)
        eimg[row_new] = expand_module_image(img[n])

    eimg = eimg[:-36]  # remove empty bottom rows

    return eimg


def correct_detector_image(image, darks, gains):
    """
    Correct Jungfrau detector raw image.

    Corrections are:
    - subtract (gain dependent) darks
    - divide by appropriate gain
    - apply module geometry (space between modules and chips)

    Parameters
    ----------
    image : (nmodules, 512, 1024) ndarray
      Raw image.
    darks : (nmodules, 3, 512, 1024) ndarray
      Dark images.
    gains : (nmodules, 3, 512, 1024) ndarray
      Gain maps.

    Returns
    -------
    cimage : ndarray
       Corrected image.

    """

    cimage = np.empty_like(image, dtype=np.float32)

    for imodule, (module, mdark, mgain) in enumerate(zip(image, darks, gains)):

        where_gain = [
            np.where(module & 2**14 == 0),
            np.where((module & (2**14) > 0) & (module & 2**15 == 0)),
            np.where(module & 2**15 > 0)
        ]

        for ngain in range(3):
            idx = where_gain[ngain]
            cimage[imodule][idx] = module[idx] - mdark[ngain][idx]
            cimage[imodule][idx] /= mgain[ngain][idx]

    cimage = expand_detector_image(cimage)

    return cimage


def correct(image, darks, gains, geometry=True):
    """
    Apply following corrections to a Jungfrau raw image:
    - subtract (gain dependent) darks
    - divide by appropriate gain
    - apply module geometry (space between modules and chips)

    Parameters
    ----------
    image : (nmodules, 512, 1024)-ndarrays
      Raw image.
    darks : (nmodules, 3, 512, 1024)-ndarrays.
      Dark images.
    gains : (nmodules, 3, 512, 1024)-ndarrays
      Gain maps.
    geometry : bool
      If True, the module geometry is applied.

    Returns
    -------
    cimage : 2d-ndarray
       Corrected image.

    """

    cimage = np.empty_like(image, dtype=np.float32)

    imodule = 0

    for imodule, (module, mdark, mgain) in enumerate(zip(image, darks, gains)):

        where_gain = [
            np.where(module & 2**14 == 0),
            np.where((module & (2**14) > 0) & (module & 2**15 == 0)),
            np.where(module & 2**15 > 0)
        ]

        for ngain in range(3):
            idx = where_gain[ngain]
            cimage[imodule][idx] = module[idx] - mdark[ngain][idx]
            cimage[imodule][idx] /= mgain[ngain][idx]

    if geometry:
        cimage = expand_detector_image(cimage)

    return cimage


def process_jf_images(folder, basename, darks, gains, geometry=True,
                      nimages=None, save=False, save_avg=False, plot=False,
                      clim=(0, 1e3)):
    """
    Read raw output from Jungfrau 1M and return array of images.

    Parameters
    ----------
    folder : str
        Folder where raw data files are stored. Typically this is something
        like: '/data/visitor/hc5293/id09/20230517/RAW_DATA/CeO2_01'.
    basename : str
        Basename of raw data files. Typically this is something like:
        'run0001_5us' (normal mode) or 'run0001_sc_5us_7us' (burst mode)
        For a Jungfrau 1M, there will be 4 files with the same basename
         - run0001_sc_5us_7us_d0_f0_0.h5
         - run0001_sc_5us_7us_d1_f0_0.h5
         - run0001_sc_5us_7us_master_0.h5
         - run0001_sc_5us_7us_virtual_0.h5
    darks : ndarray(dtype=float, ndim=5)
        Processed darks.
    gains : ndarray(dtype=float, ndim=5)
        Processed darks.
    geometry : bool, optional
        ...
        Default is True.
    nimages : int or None, optional
        Number of images to be analyzed. If None (optional), all
        images are analyzed.
        If more than one storage cell was used, 'nimages' is interpreted
        as the number of images per storage cell to be analyzed.
    save : bool, optional
        If True, processed images will be saved as a single hdf5 file.
        The folder used for saving is defined relatively to the input 'folder'.
        If folder="/data/visitor/hc5293/id09/20230517/RAW_DATA/Ce_01",
        outfolder="/data/visitor/hc5293/id09/20230517/PROCESSED_DATA/Ce_01".
    plot : bool, optional
        If True, a figure with 16 multiple plots
    clim : tuple, optional
        Color imits used by plot_jf_images().

    Returns
    -------
    imgs : ndarray(dtype=float, ndim=4)
        Processed images arranged in a (nsc, nimages, nrows, ncols)
        numpy array.
        - 'nsc' : number of detector storage cells used in the data collection
        - 'nimages' : number of collected images per storage cell
        - 'nrows' : number of image rows
        - 'ncols' : number or image columns
        If 100 images were collected with a Jungfrau 1M in burst mode and
        'geometry' is True, imgs.shape = (16, 100, 1064, 1032)

    """

    print("\nReading images...")
    data = read_jf_images(folder=folder, basename=basename, nimages=nimages)

    if darks is None:
        raise ValueError("'darks' cannot be None.")

    if gains is None:
        raise ValueError("'gains' cannot be None.")

    # verify number of storace cells in darks and data
    nsc_darks = len(darks)
    nsc_gains = len(gains)
    nsc_data = 0
    for k in range(16):
        data_sc = data[k]
        if len(data_sc) != 0:
            nsc_data += 1

    if nimages is None:
        nimages_sc = [len(d) for d in data]
        if nsc_data == 1:
            nimages = max(nimages_sc)
        else:
            # to catch packet loss in sc mode
            nimages = min(nimages_sc)

    if nsc_darks != nsc_data:
        raise ValueError("number of storage cells in 'data' " +
                         "(%d) and 'darks' (%d) are different."
                         % (nsc_data, nsc_darks))
    if nsc_gains != nsc_data:
        raise ValueError("number of storage cells in 'data' " +
                         "(%d) and 'gains' (%d) are different."
                         % (nsc_data, nsc_gains))
    else:
        print("\nNumber of storage cells detected: %d" % nsc_data)

    print("\nProcessing images over available storage cells...")
    imgs = []
    for k in tqdm(range(16)):
        data_sc = data[k]
        # if len(data_sc) != 0 and not data_sc.all() >= 2**16:
        if len(data_sc) != 0:
            imgs_k = []
            # last_image = min(len(data_sc), nimages)
            for d in tqdm(data_sc[:nimages], leave=False):
                if nsc_data == 1:
                    imgs_k.append(correct(d, darks=darks[0],
                                          gains=gains[0],
                                          geometry=geometry))
                else:
                    imgs_k.append(correct(d, darks=darks[k], gains=gains[k],
                                          geometry=geometry))
            imgs.append(imgs_k)

        if not geometry:
            imgs[k] = [np.vstack((img[0], img[1])) for img in imgs[k]]

    imgs = np.array(imgs)

    if save:
        print("Saving processed images...")
        folder = pathlib.Path(folder)
        folder_out = folder.parent.parent / "PROCESSED_DATA" / folder.parts[-1]
        folder_out.mkdir(exist_ok=True)

        if imgs.shape[0] == 1:
            outfilename = basename + ".npy"
            fout = folder_out / outfilename
            np.save(fout, imgs[0])
        else:
            for k, img in enumerate(imgs):
                outfilename = basename + "_%d.npy" % k
                fout = folder_out / outfilename
                np.save(fout, img)

    if plot:
        folder = pathlib.Path(folder)
        title_str = folder.parts[-1]
        title_str += " - "
        title_str += basename
        plot_jf_images(imgs, clim=clim, title=title_str)

    return imgs


def plot_jf_images(imgs, clim=(0, 1e3), figsize=(11, 9), title=None):
    """
    Plot Jungfrau 1M processed images.

    If images were collected in burst mode, the first image collected with
    each SC is plotted.

    If images were collected in normal mode, the first 16 collected images
    will be plotted.

    """
    fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=figsize)

    if title is not None:
        fig.suptitle(title)

    ax = ax.ravel()

    if imgs.shape[0] == 1:
        imgs = imgs[0]
    else:
        imgs = imgs[:, 0]

    for idx, (a, img) in enumerate(zip(ax, imgs[:16])):
        a.imshow(img, clim=clim)
        a.title.set_text("image #%d" % idx)

    plt.tight_layout()